# coding: utf8
'''
    pyvantagepro.tests.test_device
    ------------------------------

    The pyvantagepro device test suite.

'''
from __future__ import unicode_literals
import errno
import importlib
import sys
import types


class DummySerialLink(object):
    def __init__(self, *args, **kwargs):
        pass

    def settimeout(self, timeout):
        return timeout


class FakeLink(object):
    def __init__(self, ack, fail_first_write=False):
        self.ack = ack
        self.fail_first_write = fail_first_write
        self.write_calls = 0
        self.open_calls = 0
        self.close_calls = 0

    def write(self, data):
        self.write_calls += 1
        if self.fail_first_write and self.write_calls == 1:
            raise OSError(errno.EPIPE, "Broken pipe")
        return data

    def read(self, size, timeout=None):
        return self.ack

    def open(self):
        self.open_calls += 1

    def close(self):
        self.close_calls += 1


def load_device_module(monkeypatch):
    fake_pylink = types.ModuleType(str('pylink'))
    fake_pylink.link_from_url = lambda url: None
    fake_pylink.SerialLink = DummySerialLink
    monkeypatch.setitem(sys.modules, 'pylink', fake_pylink)
    import pyvantagepro.device as device_module
    return importlib.reload(device_module)


def test_wake_up_reconnects_after_broken_pipe(monkeypatch):
    device_module = load_device_module(monkeypatch)
    monkeypatch.setattr(device_module, 'NoDeviceException',
                        device_module.NoDeviceException)
    monkeypatch.setattr(device_module, 'retry', device_module.retry)
    # Skip retry sleep to keep tests fast.
    monkeypatch.setattr(device_module, 'LOGGER', device_module.LOGGER)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    vp = object.__new__(device_module.VantagePro2)
    vp.link = FakeLink(vp.WAKE_ACK, fail_first_write=True)

    assert vp.wake_up() is True
    assert vp.link.close_calls == 1
    assert vp.link.open_calls == 1


def test_send_reconnects_after_broken_pipe(monkeypatch):
    device_module = load_device_module(monkeypatch)
    # Skip retry sleep to keep tests fast.
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    vp = object.__new__(device_module.VantagePro2)
    vp.link = FakeLink(vp.ACK, fail_first_write=True)

    assert vp.send("GETTIME", vp.ACK) is True
    assert vp.link.close_calls == 1
    assert vp.link.open_calls == 1
