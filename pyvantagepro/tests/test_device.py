# coding: utf8
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.tests.test_device
    # Pedagogical note: this line is part of the step-by-step program flow.
    ------------------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    The pyvantagepro device test suite.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Pedagogical note: this line is part of the step-by-step program flow.
from __future__ import unicode_literals
# Pedagogical note: this line is part of the step-by-step program flow.
import errno
# Pedagogical note: this line is part of the step-by-step program flow.
import importlib
# Pedagogical note: this line is part of the step-by-step program flow.
import json
# Pedagogical note: this line is part of the step-by-step program flow.
import sys
# Pedagogical note: this line is part of the step-by-step program flow.
import types
# Pedagogical note: this line is part of the step-by-step program flow.
from datetime import datetime

# Pedagogical note: this line is part of the step-by-step program flow.
from ..utils import hex_to_bytes


# Pedagogical note: this line is part of the step-by-step program flow.
class DummySerialLink(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, *args, **kwargs):
        # Pedagogical note: this line is part of the step-by-step program flow.
        pass

    # Pedagogical note: this line is part of the step-by-step program flow.
    def settimeout(self, timeout):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return timeout


# Pedagogical note: this line is part of the step-by-step program flow.
class FakeLink(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, ack, fail_first_write=False):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.ack = ack
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.fail_first_write = fail_first_write
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.write_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls = 0

    # Pedagogical note: this line is part of the step-by-step program flow.
    def write(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.write_calls += 1
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.fail_first_write and self.write_calls == 1:
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise OSError(errno.EPIPE, "Broken pipe")
        # Pedagogical note: this line is part of the step-by-step program flow.
        return data

    # Pedagogical note: this line is part of the step-by-step program flow.
    def read(self, size, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.ack

    # Pedagogical note: this line is part of the step-by-step program flow.
    def open(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls += 1

    # Pedagogical note: this line is part of the step-by-step program flow.
    def close(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls += 1


# Pedagogical note: this line is part of the step-by-step program flow.
class ScriptedLink(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, read_values, fail_on_writes=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.read_values = list(read_values)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.fail_on_writes = set(fail_on_writes or [])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.write_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls = 0

    # Pedagogical note: this line is part of the step-by-step program flow.
    def write(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.write_calls += 1
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.write_calls in self.fail_on_writes:
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise OSError(errno.EPIPE, "Broken pipe")
        # Pedagogical note: this line is part of the step-by-step program flow.
        return data

    # Pedagogical note: this line is part of the step-by-step program flow.
    def read(self, size, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.read_values.pop(0)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def empty_socket(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return None

    # Pedagogical note: this line is part of the step-by-step program flow.
    def open(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls += 1

    # Pedagogical note: this line is part of the step-by-step program flow.
    def close(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls += 1


# Pedagogical note: this line is part of the step-by-step program flow.
class DeadLink(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls = 0

    # Pedagogical note: this line is part of the step-by-step program flow.
    def write(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        raise OSError(errno.EPIPE, "Broken pipe")

    # Pedagogical note: this line is part of the step-by-step program flow.
    def read(self, size, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return '\n\r'

    # Pedagogical note: this line is part of the step-by-step program flow.
    def open(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls += 1

    # Pedagogical note: this line is part of the step-by-step program flow.
    def close(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls += 1


# Pedagogical note: this line is part of the step-by-step program flow.
class HealthyLink(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, wake_ack):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_ack = wake_ack
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls = 0

    # Pedagogical note: this line is part of the step-by-step program flow.
    def write(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return data

    # Pedagogical note: this line is part of the step-by-step program flow.
    def read(self, size, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.wake_ack

    # Pedagogical note: this line is part of the step-by-step program flow.
    def open(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.open_calls += 1

    # Pedagogical note: this line is part of the step-by-step program flow.
    def close(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.close_calls += 1


# Pedagogical note: this line is part of the step-by-step program flow.
def load_device_module(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    fake_pylink = types.ModuleType(str('pylink'))
    # Pedagogical note: this line is part of the step-by-step program flow.
    fake_pylink.link_from_url = lambda url: None
    # Pedagogical note: this line is part of the step-by-step program flow.
    fake_pylink.SerialLink = DummySerialLink
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setitem(sys.modules, 'pylink', fake_pylink)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.device as device_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    return importlib.reload(device_module)


# Pedagogical note: this line is part of the step-by-step program flow.
def test_wake_up_reconnects_after_broken_pipe(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(device_module, 'NoDeviceException',
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        device_module.NoDeviceException)
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(device_module, 'retry', device_module.retry)
    # Skip retry sleep to keep tests fast.
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(device_module, 'LOGGER', device_module.LOGGER)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = FakeLink(vp.WAKE_ACK, fail_first_write=True)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.wake_up() is True
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.link.close_calls == 1
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.link.open_calls == 1


# Pedagogical note: this line is part of the step-by-step program flow.
def test_send_reconnects_after_broken_pipe(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Skip retry sleep to keep tests fast.
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = FakeLink(vp.ACK, fail_first_write=True)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.send("GETTIME", vp.ACK) is True
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.link.close_calls == 1
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.link.open_calls == 1


# Pedagogical note: this line is part of the step-by-step program flow.
def test_get_current_data_after_gettime_recovers_broken_pipe(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Valid GETTIME payload (includes CRC).
    # Pedagogical note: this line is part of the step-by-step program flow.
    gettime_payload = hex_to_bytes("25 35 0A 07 06 70 60 BA")
    # Valid LOOP payload used in parser tests.
    # Pedagogical note: this line is part of the step-by-step program flow.
    loop_payload = hex_to_bytes(
        # Pedagogical note: this line is part of the step-by-step program flow.
        "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0000000000000000000000000000008C00060C610183070A"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0D2A3C"
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Sequence:
    # - gettime wake ACK, gettime send ACK, gettime data
    # - get_current_data wake ACK (after one reconnect), LOOP ACK, LOOP data
    # Pedagogical note: this line is part of the step-by-step program flow.
    link = ScriptedLink(
        # Pedagogical note: this line is part of the step-by-step program flow.
        read_values=[
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\n\r',
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\x06',
            # Pedagogical note: this line is part of the step-by-step program flow.
            gettime_payload,
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\n\r',
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\x06',
            # Pedagogical note: this line is part of the step-by-step program flow.
            loop_payload,
        # Pedagogical note: this line is part of the step-by-step program flow.
        ],
        # Pedagogical note: this line is part of the step-by-step program flow.
        fail_on_writes={3},  # fail first wake_up write in get_current_data()
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = link
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevA = False
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevB = True

    # Pedagogical note: this line is part of the step-by-step program flow.
    got_time = vp.gettime()
    # Pedagogical note: this line is part of the step-by-step program flow.
    current_data = vp.get_current_data()

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert got_time == datetime(2012, 6, 7, 10, 53, 37)
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert current_data['RainRate'] == 655.35
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert link.close_calls == 1
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert link.open_calls == 1


# Pedagogical note: this line is part of the step-by-step program flow.
def test_wake_up_recreates_link_when_open_cannot_recover(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    created = {'count': 0}

    # Pedagogical note: this line is part of the step-by-step program flow.
    def factory():
        # Pedagogical note: this line is part of the step-by-step program flow.
        created['count'] += 1
        # Pedagogical note: this line is part of the step-by-step program flow.
        return HealthyLink(device_module.VantagePro2.WAKE_ACK)

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = DeadLink()
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = factory
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.wake_up() is True
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert created['count'] == 1
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert isinstance(vp.link, HealthyLink)


# Pedagogical note: this line is part of the step-by-step program flow.
def test_meta_returns_current_data_variable_names(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    loop_payload = hex_to_bytes(
        # Pedagogical note: this line is part of the step-by-step program flow.
        "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0000000000000000000000000000008C00060C610183070A"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0D2A3C"
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    link = ScriptedLink(
        # Pedagogical note: this line is part of the step-by-step program flow.
        read_values=[
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\n\r',
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\x06',
            # Pedagogical note: this line is part of the step-by-step program flow.
            loop_payload,
        # Pedagogical note: this line is part of the step-by-step program flow.
        ]
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = link
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevA = False
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevB = True

    # Pedagogical note: this line is part of the step-by-step program flow.
    fields = vp.meta()
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert isinstance(fields, list)
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert 'Datetime' in fields
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert 'TempIn' in fields
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert 'TempOut' in fields
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert 'RainRate' in fields
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert 'SunRise' in fields


# Pedagogical note: this line is part of the step-by-step program flow.
def test_get_current_data_as_json(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    loop_payload = hex_to_bytes(
        # Pedagogical note: this line is part of the step-by-step program flow.
        "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0000000000000000000000000000008C00060C610183070A"
        # Pedagogical note: this line is part of the step-by-step program flow.
        "0D2A3C"
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    link = ScriptedLink(
        # Pedagogical note: this line is part of the step-by-step program flow.
        read_values=[
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\n\r',
            # Pedagogical note: this line is part of the step-by-step program flow.
            '\x06',
            # Pedagogical note: this line is part of the step-by-step program flow.
            loop_payload,
        # Pedagogical note: this line is part of the step-by-step program flow.
        ]
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = link
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevA = False
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.RevB = True

    # Pedagogical note: this line is part of the step-by-step program flow.
    payload = vp.get_current_data_as_json()
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert isinstance(payload, dict)
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert payload['TempIn'] == 85.0
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert payload['RainRate'] == 655.35
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert isinstance(payload['Datetime'], str)
    # Pedagogical note: this line is part of the step-by-step program flow.
    json.dumps(payload)


# Pedagogical note: this line is part of the step-by-step program flow.
def test_wake_up_accepts_crlf_ack(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = FakeLink('\r\n')
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.wake_up() is True


# Pedagogical note: this line is part of the step-by-step program flow.
def test_wake_up_accepts_bytes_and_mixed_ack(monkeypatch):
    # Pedagogical note: this line is part of the step-by-step program flow.
    device_module = load_device_module(monkeypatch)
    # Pedagogical note: this line is part of the step-by-step program flow.
    import pyvantagepro.utils as utils_module
    # Pedagogical note: this line is part of the step-by-step program flow.
    monkeypatch.setattr(utils_module.time, 'sleep', lambda _: None)

    # Pedagogical note: this line is part of the step-by-step program flow.
    vp = object.__new__(device_module.VantagePro2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.link = FakeLink(b'\n\x06')
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._link_factory = None
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp._timeout = 10

    # Pedagogical note: this line is part of the step-by-step program flow.
    assert vp.wake_up() is True
