def test_forward(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.forward()


def test_reverse(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.reverse()


def test_brake(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.brake()


def test_coast(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.coast()


def test_set_outputs(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.set_outputs(out1=0, out2=0)


def test_set_voltage(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.set_voltage(5.06)
    assert drv8830.get_voltage() == 5.06


def test_set_voltage_snap(DRV8830, i2c_dev):
    # Should snap to the nearest available voltage and read back correctly
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.set_voltage(0.82)
    assert drv8830.get_voltage() == 0.80


def test_voltage_out_of_range(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.set_voltage(0)
    assert drv8830.get_voltage() == 0


def test_get_fault(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    assert drv8830.get_fault().current_limit == 0


def test_clear_fault(DRV8830, i2c_dev):
    drv8830 = DRV8830(i2c_dev=i2c_dev)
    drv8830.clear_fault()
