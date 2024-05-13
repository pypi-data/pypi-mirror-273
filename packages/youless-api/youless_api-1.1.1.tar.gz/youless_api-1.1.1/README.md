# YouLess Python Data Bridge
[![PyPI version](https://badge.fury.io/py/youless-api.svg)](https://badge.fury.io/py/youless-api)

This package contains support classes to fetch data from the YouLess sensors. The current implementation
supports the following YouLess devices:

* LS120, both the Enologic and the PVOutput firmware
* LS110

Experimental support for authentication was added in v0.15 of the youless-python-bridge.

## Contributing

To request new features or report bugs please use:

    https://github.com/gjong/youless-python-bridge/issues/new

If you want to contribute by creating code yourself then create a fork of the repository and offer the changes in a PR back into this repository.

## Using the python integration

To use the API use the following code:

```python
from youless_api.youless_api import YoulessAPI

if __name__ == '__main__':
    api = YoulessAPI("192.168.1.2")  # use the ip address of the YouLess device
    api.initialize()
    api.update()

    # from this point on on you should be able to access the sensors through the YouLess bridge
    gasUsage = api.gas_meter.value
```

To use authentication please use the snippet below (this is still experimental):

```python
from youless_api.youless_api import YoulessAPI

if __name__ == '__main__':
    api = YoulessAPI("192.168.1.2", "my-user-name", "my-password")  # use the ip address of the YouLess device
    api.initialize()
    api.update()

    # from this point on on you should be able to access the sensors through the YouLess bridge
    gasUsage = api.gas_meter.value
```
