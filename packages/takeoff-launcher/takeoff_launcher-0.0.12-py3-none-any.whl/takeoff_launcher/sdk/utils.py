"""Utility functions for Takeoff SDK"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
import re
import uuid
from pathlib import Path

import docker
import requests

from .schema import TakeoffEnvSetting


def start_container(
    image_name: str,
    container_name: str,
    ports: dict,
    volumes: list,
    environment_vars: dict,
    device_requests: list,
    shm_size: str,
    command: list = None,
    **docker_run_kwargs
):
    """Start a docker container.

    Args:
        image_name (str): image name with tag. example: "takeoff:cpu"
        container_name (str): container name
        ports (dict): port mapping. example: {"3000/tcp": None, "3001/tcp": None}
        volumes (list): volume mapping. example: [path1:path2]
        environment_vars (dict): environment variables. example: {"TAKEOFF_MAX_BATCH_SIZE": 1}
        device_requests (list): device requests. example: [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
        shm_size (str): shm size. example: "4G"
    """
    client = docker.from_env()

    container = client.containers.run(
        image_name,
        detach=True,
        auto_remove=True,
        environment=environment_vars,
        name=container_name,
        device_requests=device_requests,
        volumes=volumes,
        ports=ports,
        shm_size=shm_size,
        command=command,
        **docker_run_kwargs,
    )
    return container


def is_docker_logs_error(container):
    """Check the docker logs for errors

    Args:
        container (docker.models.containers.Container): docker container

    Returns:
        str: traceback if error, None if no error
    """

    # Stream logs from the container
    try:
        logs = container.logs().decode("utf-8")

        # Regular expression to match tracebacks
        traceback_pattern = r"Traceback \(most recent call last\):.*?(?=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z|$)"
        tracebacks = re.findall(traceback_pattern, logs, re.DOTALL)

        # Regular expression to match custom "Takeoff Exception Raise:" errors
        takeoff_exception_pattern = r"TAKEOFF CONTAINER ERROR:.*?(?=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z|$)"
        takeoff_exceptions = re.findall(takeoff_exception_pattern, logs, re.DOTALL)

        # Error handling
        if len(takeoff_exceptions) > 0:
            # Catch custom "Takeoff Exception Raise:" errors
            return takeoff_exceptions[0]
        elif len(tracebacks) > 0:
            # Catch Python tracebacks
            return tracebacks[0]

    except Exception as e:
        return f"Error while reading logs: {e}"

    return None


def is_takeoff_loading(server_url: str, num_readers) -> bool:
    """Check if the Takeoff server is loading.

    Instead of checking `healthz` endpoint, we check the `status` endpoint to see if the server is loading. Because in
    the manifest file, we can have multiple readers, and the `healthz` endpoint only checks if the server is ready, using `status` can check if all readers are ready.

    Args:
        server_url (str): server url
        num_readers (int): number of readers

    Returns:
        bool: True if the server is loading, False if it is ready
    """
    try:
        response = requests.get(server_url + "/status")
        response_json = response.json()

        if len(response_json["live_readers"].keys()) < num_readers:
            return True
        return not response.ok
    except requests.exceptions.ConnectionError:
        return True


def start_takeoff(takeoff_config: TakeoffEnvSetting, **docker_run_kwargs) -> tuple:
    """Start a Takeoff server using the given configuration

    Args:
        takeoff_config (TakeoffEnvSetting): Takeoff configuration

    Returns:
        tuple: (takeoff_port, management_port, openai_port, container)
    """

    image = os.environ.get("TAKEOFF_IMAGE", "tytn/takeoff-pro:0.14.3-gpu")

    random_name = "takeoff_" + str(uuid.uuid4())[:8]

    volumes = [f"{Path.home()}/.takeoff_cache:/code/models"]
    # check if the cache file exists, if it does, mount it to the container
    if os.path.exists(f"{Path.home()}/.takeoff_cache/ssd_cache.json"):
        volumes.append(f"{Path.home()}/.takeoff_cache/ssd_cache.json:/code/ssd_cache.json")

    device_requests = (
        [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])] if takeoff_config.device == "cuda" else None
    )
    environtment_vars = takeoff_config.settings_to_env_vars()

    container = start_container(
        image_name=image,
        container_name=random_name,
        ports={"3000/tcp": None, "3001/tcp": None, "3003/tcp": None, "9090/tcp": None},
        volumes=volumes,
        environment_vars=environtment_vars,
        device_requests=device_requests,
        shm_size="4G",
        **docker_run_kwargs,
    )

    container.reload()
    takeoff_port = container.ports["3000/tcp"][0]["HostPort"]
    management_port = container.ports["3001/tcp"][0]["HostPort"]
    openai_port = container.ports["3003/tcp"][0]["HostPort"]
    prometheus_port = container.ports["9090/tcp"][0]["HostPort"]

    return takeoff_port, management_port, openai_port, prometheus_port, container


def start_takeoff_with_manifest(manifest_path: str, device: str, **docker_run_kwargs) -> tuple:
    """Start a Takeoff server using the given manifest file

    Args:
        manifest_path (str): path to the manifest file
        device (str): device to use. "cpu" or "cuda"

    Returns:
        tuple: (takeoff_port, management_port, openai_port, container)
    """
    image = os.environ.get("TAKEOFF_IMAGE", "tytn/takeoff-pro:0.14.3-gpu")

    random_name = "takeoff_" + str(uuid.uuid4())[:8]
    volumes = [f"{Path.home()}/.takeoff_cache:/code/models", f"{manifest_path}:/code/config.yaml"]
    # check if the cache file exists, if it does, mount it to the container
    if os.path.exists(f"{Path.home()}/.takeoff_cache/ssd_cache.json"):
        volumes.append(f"{Path.home()}/.takeoff_cache/ssd_cache.json:/code/ssd_cache.json")

    device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])] if device == "cuda" else None

    container = start_container(
        image_name=image,
        container_name=random_name,
        ports={"3000/tcp": None, "3001/tcp": None, "3003/tcp": None, "9090/tcp": None},
        volumes=volumes,
        environment_vars={},
        device_requests=device_requests,
        shm_size="4G",
        **docker_run_kwargs,
    )

    container.reload()
    takeoff_port = container.ports["3000/tcp"][0]["HostPort"]
    management_port = container.ports["3001/tcp"][0]["HostPort"]
    openai_port = container.ports["3003/tcp"][0]["HostPort"]
    prometheus_port = container.ports["9090/tcp"][0]["HostPort"]

    return takeoff_port, management_port, openai_port, prometheus_port, container
