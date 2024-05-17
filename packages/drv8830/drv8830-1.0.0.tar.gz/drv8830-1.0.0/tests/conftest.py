import sys

import pytest
from i2cdevice import MockSMBus


@pytest.fixture(scope='function', autouse=False)
def i2c_dev():
    yield MockSMBus(1)


@pytest.fixture(scope='function', autouse=False)
def DRV8830():
    from drv8830 import DRV8830
    yield DRV8830
    del sys.modules["drv8830"]
