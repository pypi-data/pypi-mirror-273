# Takeoff SDK - Internal

## Table of Contents

- [Takeoff SDK - Internal](#takeoff-sdk---internal)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Getting Started ](#getting-started-)
    - [Installing](#installing)
  - [Usage ](#usage-)
    - [Launch Takeoff](#launch-takeoff)

## About <a name = "about"></a>

The Takeoff SDK library facilitates launching Takeoff within Python. It provides a Pythonic interface, simplifying the process of initiating Takeoff using the docker run command. Essentially, it wraps the dev.sh script, which manages Docker with all necessary environment variables, volume mounting, network configuration, and device settings. This library is specifically designed for an internal team of developers who need to integrate Python applications with the Takeoff Server, offering a quick and straightforward way to start Takeoff in a Python runtime. It also enables running benchmarks and integration tests.

## Getting Started <a name = "getting_started"></a>

### Installing

To get started with the Takeoff SDK Library, you can install it directly using pip:
```
pip install takeoff_launcher
```

Alternatively, if you are working on developing the library, you can install it in editable mode. This allows you to make changes to the library and test them in real-time. Navigate to the `takeoff-launcher` folder and run the following command:
```
pip install -e . 
```

## Usage <a name = "usage"></a>


### Launch Takeoff 


**To quickly launch the Takeoff server with default configurations, use the following script:**

```python
from takeoff_launcher import Takeoff

takeoff = Takeoff(model_name="test_model", device="cuda")
takeoff.start() # this will start a docker with takeoff server in the background
```

**For a more customized setup:**
```python
from takeoff_launcher import Takeoff, TakeoffEnvSetting
config = TakeoffEnvSetting(model_name="test_model", device="cpu", max_batch_size=16)
takeoff = Takeoff.from_config(config)
takeoff.start() # this will start a docker with takeoff server in the background
```

Refer to the `TakeoffEnvSetting` Data Object or [Takeoff Environment Variables Settings](docs/takeoff_env_setting.md) for additional configuration options.


**Launch from a manifest mode:**

```python
from takeoff_launcher import Takeoff

takeoff = Takeoff.from_manifest("path_to_your_manifest.yaml")
takeoff.start() # this will takeoff server using manifest.yaml
```
