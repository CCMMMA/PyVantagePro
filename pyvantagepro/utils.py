# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.utils
    # Pedagogical note: this line is part of the step-by-step program flow.
    ------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Pedagogical note: this line is part of the step-by-step program flow.
from __future__ import unicode_literals
# Pedagogical note: this line is part of the step-by-step program flow.
import sys
# Pedagogical note: this line is part of the step-by-step program flow.
import time
# Pedagogical note: this line is part of the step-by-step program flow.
import csv
# Pedagogical note: this line is part of the step-by-step program flow.
import binascii

# Pedagogical note: this line is part of the step-by-step program flow.
from .compat import to_char, str, bytes, StringIO, is_py3, OrderedDict


# Pedagogical note: this line is part of the step-by-step program flow.
def is_text(data):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Check if data is text instance'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    return isinstance(data, str)


# Pedagogical note: this line is part of the step-by-step program flow.
def is_bytes(data):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Check if data is bytes instance'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    return isinstance(data, bytes)


# Pedagogical note: this line is part of the step-by-step program flow.
class cached_property(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """A decorator that converts a function into a lazy property.  The
    # Pedagogical note: this line is part of the step-by-step program flow.
    function wrapped is called the first time to retrieve the result
    # Pedagogical note: this line is part of the step-by-step program flow.
    and then that calculated result is used the next time you access
    # Pedagogical note: this line is part of the step-by-step program flow.
    the value::

        # Pedagogical note: this line is part of the step-by-step program flow.
        class Foo(object):

            # Pedagogical note: this line is part of the step-by-step program flow.
            @cached_property
            # Pedagogical note: this line is part of the step-by-step program flow.
            def foo(self):
                # calculate something important here
                # Pedagogical note: this line is part of the step-by-step program flow.
                return 42

    # Pedagogical note: this line is part of the step-by-step program flow.
    The class has to have a `__dict__` in order for this property to
    # Pedagogical note: this line is part of the step-by-step program flow.
    work.
    # Pedagogical note: this line is part of the step-by-step program flow.
    Stolen from:
    # Pedagogical note: this line is part of the step-by-step program flow.
    https://raw.github.com/mitsuhiko/werkzeug/master/werkzeug/utils.py
    # Pedagogical note: this line is part of the step-by-step program flow.
    """

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, func, name=None, doc=None, writeable=False):
        # Pedagogical note: this line is part of the step-by-step program flow.
        if writeable:
            # Pedagogical note: this line is part of the step-by-step program flow.
            from warnings import warn
            # Pedagogical note: this line is part of the step-by-step program flow.
            warn(DeprecationWarning('the writeable argument to the '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'cached property is a noop since 0.6 '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'because the property is writeable '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'by default for performance reasons'))

        # Pedagogical note: this line is part of the step-by-step program flow.
        self.__name__ = name or func.__name__
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.__module__ = func.__module__
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.__doc__ = doc or func.__doc__
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.func = func

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __get__(self, obj, type=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        if obj is None:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return self
        # Pedagogical note: this line is part of the step-by-step program flow.
        value = obj.__dict__.get(self.__name__)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if value is None:
            # Pedagogical note: this line is part of the step-by-step program flow.
            value = self.func(obj)
            # Pedagogical note: this line is part of the step-by-step program flow.
            obj.__dict__[self.__name__] = value
        # Pedagogical note: this line is part of the step-by-step program flow.
        return value


# Pedagogical note: this line is part of the step-by-step program flow.
class retry(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Retries a function or method until it returns True value.
    # Pedagogical note: this line is part of the step-by-step program flow.
    delay sets the initial delay in seconds, and backoff sets the factor by
    # Pedagogical note: this line is part of the step-by-step program flow.
    which the delay should lengthen after each failure.
    # Pedagogical note: this line is part of the step-by-step program flow.
    Tries must be at least 0, and delay greater than 0.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, tries=3, delay=1):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tries = tries
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.delay = delay

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __call__(self, f):
        # Pedagogical note: this line is part of the step-by-step program flow.
        def wrapped_f(*args, **kwargs):
            # Pedagogical note: this line is part of the step-by-step program flow.
            for i in range(self.tries):
                # Pedagogical note: this line is part of the step-by-step program flow.
                try:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    ret = f(*args, **kwargs)
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    if ret:
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        return ret
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    elif i == self.tries - 1:
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        return ret
                # Pedagogical note: this line is part of the step-by-step program flow.
                except Exception as e:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    if i == self.tries - 1:
                        # last chance
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        raise e
                # Pedagogical note: this line is part of the step-by-step program flow.
                if self.delay > 0:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    time.sleep(self.delay)
        # Pedagogical note: this line is part of the step-by-step program flow.
        wrapped_f.__doc__ = f.__doc__
        # Pedagogical note: this line is part of the step-by-step program flow.
        wrapped_f.__name__ = f.__name__
        # Pedagogical note: this line is part of the step-by-step program flow.
        wrapped_f.__module__ = f.__module__
        # Pedagogical note: this line is part of the step-by-step program flow.
        return wrapped_f


# Pedagogical note: this line is part of the step-by-step program flow.
def bytes_to_hex(byte):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert a bytearray to it's hex string representation.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    if sys.version_info[0] >= 3:
        # Pedagogical note: this line is part of the step-by-step program flow.
        hexstr = str(binascii.hexlify(byte), "utf-8")
    # Pedagogical note: this line is part of the step-by-step program flow.
    else:
        # Pedagogical note: this line is part of the step-by-step program flow.
        hexstr = str(binascii.hexlify(byte))
    # Pedagogical note: this line is part of the step-by-step program flow.
    data = []
    # Pedagogical note: this line is part of the step-by-step program flow.
    for i in range(0, len(hexstr), 2):
        # Pedagogical note: this line is part of the step-by-step program flow.
        data.append("%s" % hexstr[i:i + 2].upper())
    # Pedagogical note: this line is part of the step-by-step program flow.
    return ' '.join(data)


# Pedagogical note: this line is part of the step-by-step program flow.
def hex_to_bytes(hexstr):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert a string hex byte values into a byte string.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    return binascii.unhexlify(hexstr.replace(' ', '').encode('utf-8'))


# Pedagogical note: this line is part of the step-by-step program flow.
def byte_to_binary(byte):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert byte to binary string representation.
    # Pedagogical note: this line is part of the step-by-step program flow.
    E.g.
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> byte_to_binary("\x4A")
    # Pedagogical note: this line is part of the step-by-step program flow.
    '0000000001001010'
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''
    # Pedagogical note: this line is part of the step-by-step program flow.
    return ''.join(str((byte & (1 << i)) and 1) for i in reversed(range(8)))


# Pedagogical note: this line is part of the step-by-step program flow.
def bytes_to_binary(values):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert bytes to binary string representation.
    # Pedagogical note: this line is part of the step-by-step program flow.
    E.g.
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> bytes_to_binary(b"\x4A\xFF")
    # Pedagogical note: this line is part of the step-by-step program flow.
    '0100101011111111'
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''
    # Pedagogical note: this line is part of the step-by-step program flow.
    if is_py3:
        # TODO: Python 3 convert \x00 to integer 0 ?
        # Pedagogical note: this line is part of the step-by-step program flow.
        if values == 0:
            # Pedagogical note: this line is part of the step-by-step program flow.
            data = '00000000'
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            data = ''.join([byte_to_binary(b) for b in values])
    # Pedagogical note: this line is part of the step-by-step program flow.
    else:
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = ''.join(byte_to_binary(ord(b)) for b in values)
    # Pedagogical note: this line is part of the step-by-step program flow.
    return data


# Pedagogical note: this line is part of the step-by-step program flow.
def hex_to_binary(hexstr):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert hexadecimal string to binary string representation.
    # Pedagogical note: this line is part of the step-by-step program flow.
    E.g.
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> hex_to_binary("FF")
    # Pedagogical note: this line is part of the step-by-step program flow.
    '11111111'
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''
    # Pedagogical note: this line is part of the step-by-step program flow.
    if is_py3:
        # Pedagogical note: this line is part of the step-by-step program flow.
        return ''.join(byte_to_binary(b) for b in hex_to_bytes(hexstr))
    # Pedagogical note: this line is part of the step-by-step program flow.
    return ''.join(byte_to_binary(ord(b)) for b in hex_to_bytes(hexstr))


# Pedagogical note: this line is part of the step-by-step program flow.
def binary_to_int(buf, start=0, stop=None):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Convert binary string representation to integer.
    # Pedagogical note: this line is part of the step-by-step program flow.
    E.g.
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> binary_to_int('1111110')
    # Pedagogical note: this line is part of the step-by-step program flow.
    126
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> binary_to_int('1111110', 0, 2)
    # Pedagogical note: this line is part of the step-by-step program flow.
    2
    # Pedagogical note: this line is part of the step-by-step program flow.
    >>> binary_to_int('1111110', 0, 3)
    # Pedagogical note: this line is part of the step-by-step program flow.
    6
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''
    # Pedagogical note: this line is part of the step-by-step program flow.
    return int(buf[::-1][start:(stop or len(buf))][::-1], 2)


# Pedagogical note: this line is part of the step-by-step program flow.
def csv_to_dict(file_input, delimiter=','):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Deserialize csv to list of dictionaries.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    delimiter = to_char(delimiter)
    # Pedagogical note: this line is part of the step-by-step program flow.
    table = []
    # Pedagogical note: this line is part of the step-by-step program flow.
    reader = csv.DictReader(file_input, delimiter=delimiter,
                            # Pedagogical note: this line is part of the step-by-step program flow.
                            skipinitialspace=True)
    # Pedagogical note: this line is part of the step-by-step program flow.
    for d in reader:
        # Pedagogical note: this line is part of the step-by-step program flow.
        table.append(d)
    # Pedagogical note: this line is part of the step-by-step program flow.
    return ListDict(table)


# Pedagogical note: this line is part of the step-by-step program flow.
def dict_to_csv(items, delimiter, header):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Serialize list of dictionaries to csv.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    content = ""
    # Pedagogical note: this line is part of the step-by-step program flow.
    if len(items) > 0:
        # Pedagogical note: this line is part of the step-by-step program flow.
        delimiter = to_char(delimiter)
        # Pedagogical note: this line is part of the step-by-step program flow.
        output = StringIO()
        # Pedagogical note: this line is part of the step-by-step program flow.
        csvwriter = csv.DictWriter(output, fieldnames=items[0].keys(),
                                   # Pedagogical note: this line is part of the step-by-step program flow.
                                   delimiter=delimiter)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if header:
            # Pedagogical note: this line is part of the step-by-step program flow.
            csvwriter.writerow(dict((key, key) for key in items[0].keys()))
            # writeheader is not supported in python2.6
            # csvwriter.writeheader()
        # Pedagogical note: this line is part of the step-by-step program flow.
        for item in items:
            # Pedagogical note: this line is part of the step-by-step program flow.
            csvwriter.writerow(dict(item))

        # Pedagogical note: this line is part of the step-by-step program flow.
        content = output.getvalue()
        # Pedagogical note: this line is part of the step-by-step program flow.
        output.close()
    # Pedagogical note: this line is part of the step-by-step program flow.
    return content


# Pedagogical note: this line is part of the step-by-step program flow.
class Dict(OrderedDict):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''A dict with somes additional methods.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    def filter(self, keys):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Create a dict with only the following `keys`.

        # Pedagogical note: this line is part of the step-by-step program flow.
        >>> mydict = Dict({"name":"foo", "firstname":"bar", "age":1})
        # Pedagogical note: this line is part of the step-by-step program flow.
        >>> mydict.filter(['age', 'name'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        {'age': 1, 'name': 'foo'}
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = Dict()
        # Pedagogical note: this line is part of the step-by-step program flow.
        real_keys = set(self.keys()) - set(set(self.keys()) - set(keys))
        # Pedagogical note: this line is part of the step-by-step program flow.
        for key in keys:
            # Pedagogical note: this line is part of the step-by-step program flow.
            if key in real_keys:
                # Pedagogical note: this line is part of the step-by-step program flow.
                data[key] = self[key]
        # Pedagogical note: this line is part of the step-by-step program flow.
        return data

    # Pedagogical note: this line is part of the step-by-step program flow.
    def to_csv(self, delimiter=',', header=True):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Serialize list of dictionaries to csv.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return dict_to_csv([self], delimiter, header)


# Pedagogical note: this line is part of the step-by-step program flow.
class ListDict(list):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''List of dicts with somes additional methods.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    def to_csv(self, delimiter=',', header=True):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Serialize list of dictionaries to csv.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return dict_to_csv(list(self), delimiter, header)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def filter(self, keys):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Create a list of dictionaries with only the following `keys`.

        # Pedagogical note: this line is part of the step-by-step program flow.
        >>> mylist = ListDict([{"name":"foo", "age":31},
        # Pedagogical note: this line is part of the step-by-step program flow.
        ...                    {"name":"bar", "age":24}])
        # Pedagogical note: this line is part of the step-by-step program flow.
        >>> mylist.filter(['name'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        [{'name': 'foo'}, {'name': 'bar'}]
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        items = ListDict()
        # Pedagogical note: this line is part of the step-by-step program flow.
        for item in self:
            # Pedagogical note: this line is part of the step-by-step program flow.
            items.append(item.filter(keys))
        # Pedagogical note: this line is part of the step-by-step program flow.
        return items

    # Pedagogical note: this line is part of the step-by-step program flow.
    def sorted_by(self, keyword, reverse=False):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns list sorted by `keyword`.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        key_ = keyword
        # Pedagogical note: this line is part of the step-by-step program flow.
        return ListDict(sorted(self, key=lambda k: k[key_], reverse=reverse))
