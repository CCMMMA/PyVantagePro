# coding: utf8
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.tests.test_link
    # Pedagogical note: this line is part of the step-by-step program flow.
    ----------------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    The pyvantagepro test suite.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''

# Pedagogical note: this line is part of the step-by-step program flow.
from __future__ import unicode_literals
# Pedagogical note: this line is part of the step-by-step program flow.
import os
# Pedagogical note: this line is part of the step-by-step program flow.
import random

# Pedagogical note: this line is part of the step-by-step program flow.
from ..utils import (cached_property, retry, Dict, hex_to_bytes,
                     # Pedagogical note: this line is part of the step-by-step program flow.
                     bytes_to_hex, bytes_to_binary, hex_to_binary,
                     # Pedagogical note: this line is part of the step-by-step program flow.
                     binary_to_int, csv_to_dict, is_text, is_bytes)
# Pedagogical note: this line is part of the step-by-step program flow.
from ..compat import StringIO


# Pedagogical note: this line is part of the step-by-step program flow.
def test_is_text_or_byte():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests is text.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert is_text("Text") is True
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert is_text(b"\xFF\xFF") is False
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert is_bytes(b"\xFF\xFF") is True
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert is_bytes("Text") is False


# Pedagogical note: this line is part of the step-by-step program flow.
def test_csv_to_dict():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests csv to dict.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    file_input = StringIO("a,f\r\n111,222")
    # Pedagogical note: this line is part of the step-by-step program flow.
    items = csv_to_dict(file_input)
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert items[0]["a"] == "111"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert items[0]["f"] == "222"


# Pedagogical note: this line is part of the step-by-step program flow.
def test_csv_to_dict_file():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests csv to dict with file archives.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    path = os.path.join('pyvantagepro', 'tests', 'ressources', 'archives.csv')
    # Pedagogical note: this line is part of the step-by-step program flow.
    path = os.path.abspath(os.path.join('.', path))
    # Pedagogical note: this line is part of the step-by-step program flow.
    file_input = open(path, 'r')
    # Pedagogical note: this line is part of the step-by-step program flow.
    items = csv_to_dict(file_input).sorted_by("Datetime", reverse=True)
    # Pedagogical note: this line is part of the step-by-step program flow.
    file_input.close()
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert items[0]["Barometer"] == "31.838"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert items[0]["Datetime"] == "2012-06-08 16:40:00"


# Pedagogical note: this line is part of the step-by-step program flow.
def test_csv_to_dict_empty_file():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests csv to dict with empty file archives.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    path = os.path.join('pyvantagepro', 'tests', 'ressources', 'empty.csv')
    # Pedagogical note: this line is part of the step-by-step program flow.
    path = os.path.abspath(os.path.join('.', path))
    # Pedagogical note: this line is part of the step-by-step program flow.
    file_input = open(path, 'r')
    # Pedagogical note: this line is part of the step-by-step program flow.
    items = csv_to_dict(file_input)
    # Pedagogical note: this line is part of the step-by-step program flow.
    file_input.close()
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert len(items) == 0


# Pedagogical note: this line is part of the step-by-step program flow.
def test_dict():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests DataDict.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    d = Dict()
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["f"] = "222"
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["a"] = "111"
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["b"] = "000"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "a" in d.filter(['a', 'b'])
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "b" in d.filter(['a', 'b'])
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "f" not in d.filter(['a', 'b'])
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "a,f\r\n111,222\r\n" == d.filter(['a', 'f']).to_csv()
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "f,b\r\n222,000\r\n" == d.filter(['f', 'b']).to_csv()


# Pedagogical note: this line is part of the step-by-step program flow.
def test_ordered_dict():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests DataDict.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    d = Dict()
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["f"] = "222"
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["a"] = "111"
    # Pedagogical note: this line is part of the step-by-step program flow.
    d["b"] = "000"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert "f,a,b\r\n222,111,000\r\n" == d.to_csv()


# Pedagogical note: this line is part of the step-by-step program flow.
class TestCachedProperty:
    # Pedagogical note: this line is part of the step-by-step program flow.
    ''' Tests cached_property decorator.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def random_bool(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns random bool'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return bool(random.getrandbits(1))

    # Pedagogical note: this line is part of the step-by-step program flow.
    def test_cached_property(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Tests cached_property decorator.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        value1 = self.random_bool
        # Pedagogical note: this line is part of the step-by-step program flow.
        value2 = self.random_bool
        # Pedagogical note: this line is part of the step-by-step program flow.
        assert value1 == value2


# Pedagogical note: this line is part of the step-by-step program flow.
class TestRetry:
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Test retry decorator.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    def setup_class(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Setup common data.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.retries = 0

    # Pedagogical note: this line is part of the step-by-step program flow.
    @retry(tries=3, delay=0)
    # Pedagogical note: this line is part of the step-by-step program flow.
    def retries_func(self, num):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns random bool.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.retries += 1
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.retries == num:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return False

    # Pedagogical note: this line is part of the step-by-step program flow.
    def test_cached_property(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Tests retry decorator.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        assert self.retries_func(3) is True
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.retries = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        assert self.retries_func(5) is False


# Pedagogical note: this line is part of the step-by-step program flow.
def test_bytes_to_hex():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests byte <-> hex and hex <-> byte.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert bytes_to_hex(b"\xFF") == "FF"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert hex_to_bytes(bytes_to_hex(b"\x4A")) == b"\x4A"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert bytes_to_hex(hex_to_bytes("4A")) == "4A"


# Pedagogical note: this line is part of the step-by-step program flow.
def test_bytes_binary():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests byte <-> binary and binary <-> byte.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert bytes_to_binary(b'\xFF\x00') == "1111111100000000"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert bytes_to_binary(b'\x00\x00') == "0000000000000000"


# Pedagogical note: this line is part of the step-by-step program flow.
def test_hex_binary():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests hex <-> binary and binary <-> hex.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert hex_to_binary('FF00') == "1111111100000000"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert hex_to_binary('0000') == "0000000000000000"


# Pedagogical note: this line is part of the step-by-step program flow.
def test_bin_integer():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Tests bin <-> int conversion.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    hexstr = "11111110"
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert binary_to_int(hexstr) == 254
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert binary_to_int(hexstr, 0, 1) == 0
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert binary_to_int(hexstr, 0, 2) == 2
    # Pedagogical note: this line is part of the step-by-step program flow.
    assert binary_to_int(hexstr, 0, 3) == 6
