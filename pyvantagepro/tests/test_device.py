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
from datetime import datetime

from ..utils import hex_to_bytes


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


class ScriptedLink(object):
    def __init__(self, read_values, fail_on_writes=None):
        self.read_values = list(read_values)
        self.fail_on_writes = set(fail_on_writes or [])
        self.write_calls = 0
        self.open_calls = 0
        self.close_calls = 0

    def write(self, data):
        self.write_calls += 1
        if self.write_calls in self.fail_on_writes:
            raise OSError(errno.EPIPE, "Broken pipe")
        return data

    def read(self, size, timeout=None):
        return self.read_values.pop(0)

    def empty_socket(self):
        return None

    def open(self):
        self.open_calls += 1

    def close(self):
        self.close_calls += 1


class DeadLink(object):
    def __init__(self):
        self.open_calls = 0
        self.close_calls = 0

    def write(self, data):
        raise OSError(errno.EPIPE, "Broken pipe")

    def read(self, size, timeout=None):
        return '\n\r'

    def open(self):
        self.open_calls += 1

    def close(self):
        self.close_calls += 1


class HealthyLink(object):
    def __init__(self, wake_ack):
        self.wake_ack = wake_ack
        self.open_calls = 0
        self.close_calls = 0

    def write(self, data):
        return data

    def read(self, size, timeout=None):
        return self.wake_ack

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
    vp._link_factory = None
    vp._timeout = 10

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
    vp._link_factory = None
    vp._timeout = 10

    assert vp.send("GETTIME", vp.ACK) is True
    assert vp.link.close_calls == 1
    assert vp.link.open_calls == 1


def test_get_current_data_after_gettime_recovers_broken_pipe(monkeypatch):
    device_module = load_device_module(monkeypatch)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Valid GETTIME payload (includes CRC).
    gettime_payload = hex_to_bytes("25 35 0A 07 06 70 60 BA")
    # Valid LOOP payload used in parser tests.
    loop_payload = hex_to_bytes(
        "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF"
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000"
        "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000"
        "0000000000000000000000000000008C00060C610183070A"
        "0D2A3C"
    )

    # Sequence:
    # - gettime wake ACK, gettime send ACK, gettime data
    # - get_current_data wake ACK (after one reconnect), LOOP ACK, LOOP data
    link = ScriptedLink(
        read_values=[
            '\n\r',
            '\x06',
            gettime_payload,
            '\n\r',
            '\x06',
            loop_payload,
        ],
        fail_on_writes={3},  # fail first wake_up write in get_current_data()
    )

    vp = object.__new__(device_module.VantagePro2)
    vp.link = link
    vp._link_factory = None
    vp._timeout = 10
    vp.RevA = False
    vp.RevB = True

    got_time = vp.gettime()
    current_data = vp.get_current_data()

    assert got_time == datetime(2012, 6, 7, 10, 53, 37)
    assert current_data['RainRate'] == 655.35
    assert link.close_calls == 1
    assert link.open_calls == 1


def test_wake_up_recreates_link_when_open_cannot_recover(monkeypatch):
    device_module = load_device_module(monkeypatch)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    created = {'count': 0}

    def factory():
        created['count'] += 1
        return HealthyLink(device_module.VantagePro2.WAKE_ACK)

    vp = object.__new__(device_module.VantagePro2)
    vp.link = DeadLink()
    vp._link_factory = factory
    vp._timeout = 10

    assert vp.wake_up() is True
    assert created['count'] == 1
    assert isinstance(vp.link, HealthyLink)


def test_meta_returns_current_data_variable_names(monkeypatch):
    device_module = load_device_module(monkeypatch)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    loop_payload = hex_to_bytes(
        "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF"
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000"
        "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000"
        "0000000000000000000000000000008C00060C610183070A"
        "0D2A3C"
    )

    link = ScriptedLink(
        read_values=[
            '\n\r',
            '\x06',
            loop_payload,
        ]
    )

    vp = object.__new__(device_module.VantagePro2)
    vp.link = link
    vp._link_factory = None
    vp._timeout = 10
    vp.RevA = False
    vp.RevB = True

    fields = vp.meta()
    assert isinstance(fields, list)
    assert 'Datetime' in fields
    assert 'TempIn' in fields
    assert 'TempOut' in fields
    assert 'RainRate' in fields
    assert 'SunRise' in fields


def test_wake_up_accepts_crlf_ack(monkeypatch):
    device_module = load_device_module(monkeypatch)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    vp = object.__new__(device_module.VantagePro2)
    vp.link = FakeLink('\r\n')
    vp._link_factory = None
    vp._timeout = 10

    assert vp.wake_up() is True


def test_wake_up_accepts_bytes_and_mixed_ack(monkeypatch):
    device_module = load_device_module(monkeypatch)
    import pyvantagepro.utils as utils_module
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    vp = object.__new__(device_module.VantagePro2)
    vp.link = FakeLink(b'\n\x06')
    vp._link_factory = None
    vp._timeout = 10

    assert vp.wake_up() is True
