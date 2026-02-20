# -*- coding: utf-8 -*-
# Pedagogical note: the next line explains one concrete step in the program flow.
'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro.utils
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ------------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
'''
# Pedagogical note: the next line explains one concrete step in the program flow.
from __future__ import unicode_literals
# Pedagogical note: the next line explains one concrete step in the program flow.
import sys
# Pedagogical note: the next line explains one concrete step in the program flow.
import time
# Pedagogical note: the next line explains one concrete step in the program flow.
import csv
# Pedagogical note: the next line explains one concrete step in the program flow.
import binascii

# Pedagogical note: the next line explains one concrete step in the program flow.
from .compat import to_char, str, bytes, StringIO, is_py3, OrderedDict


# Pedagogical note: the next line explains one concrete step in the program flow.
def is_text(data):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Check if data is text instance'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return isinstance(data, str)


# Pedagogical note: the next line explains one concrete step in the program flow.
def is_bytes(data):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Check if data is bytes instance'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return isinstance(data, bytes)


# Pedagogical note: the next line explains one concrete step in the program flow.
class cached_property(object):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """A decorator that converts a function into a lazy property.  The
    # Pedagogical note: the next line explains one concrete step in the program flow.
    function wrapped is called the first time to retrieve the result
    # Pedagogical note: the next line explains one concrete step in the program flow.
    and then that calculated result is used the next time you access
    # Pedagogical note: the next line explains one concrete step in the program flow.
    the value::

        # Pedagogical note: the next line explains one concrete step in the program flow.
        class Foo(object):

            # Pedagogical note: the next line explains one concrete step in the program flow.
            @cached_property
            # Pedagogical note: the next line explains one concrete step in the program flow.
            def foo(self):
                # calculate something important here
                # Pedagogical note: the next line explains one concrete step in the program flow.
                return 42

    # Pedagogical note: the next line explains one concrete step in the program flow.
    The class has to have a `__dict__` in order for this property to
    # Pedagogical note: the next line explains one concrete step in the program flow.
    work.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    Stolen from:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    https://raw.github.com/mitsuhiko/werkzeug/master/werkzeug/utils.py
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def __init__(self, func, name=None, doc=None, writeable=False):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if writeable:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            from warnings import warn
            # Pedagogical note: the next line explains one concrete step in the program flow.
            warn(DeprecationWarning('the writeable argument to the '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'cached property is a noop since 0.6 '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'because the property is writeable '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'by default for performance reasons'))

        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.__name__ = name or func.__name__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.__module__ = func.__module__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.__doc__ = doc or func.__doc__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.func = func

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def __get__(self, obj, type=None):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if obj is None:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            return self
        # Pedagogical note: the next line explains one concrete step in the program flow.
        value = obj.__dict__.get(self.__name__)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if value is None:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            value = self.func(obj)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            obj.__dict__[self.__name__] = value
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return value


# Pedagogical note: the next line explains one concrete step in the program flow.
class retry(object):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Retries a function or method until it returns True value.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    delay sets the initial delay in seconds, and backoff sets the factor by
    # Pedagogical note: the next line explains one concrete step in the program flow.
    which the delay should lengthen after each failure.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    Tries must be at least 0, and delay greater than 0.'''

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def __init__(self, tries=3, delay=1):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.tries = tries
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.delay = delay

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def __call__(self, f):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        def wrapped_f(*args, **kwargs):
            # Pedagogical note: the next line explains one concrete step in the program flow.
            for i in range(self.tries):
                # Pedagogical note: the next line explains one concrete step in the program flow.
                try:
                    # Pedagogical note: the next line explains one concrete step in the program flow.
                    ret = f(*args, **kwargs)
                    # Pedagogical note: the next line explains one concrete step in the program flow.
                    if ret:
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        return ret
                    # Pedagogical note: the next line explains one concrete step in the program flow.
                    elif i == self.tries - 1:
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        return ret
                # Pedagogical note: the next line explains one concrete step in the program flow.
                except Exception as e:
                    # Pedagogical note: the next line explains one concrete step in the program flow.
                    if i == self.tries - 1:
                        # last chance
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        raise e
                # Pedagogical note: the next line explains one concrete step in the program flow.
                if self.delay > 0:
                    # Pedagogical note: the next line explains one concrete step in the program flow.
                    time.sleep(self.delay)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        wrapped_f.__doc__ = f.__doc__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        wrapped_f.__name__ = f.__name__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        wrapped_f.__module__ = f.__module__
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return wrapped_f


# Pedagogical note: the next line explains one concrete step in the program flow.
def bytes_to_hex(byte):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert a bytearray to it's hex string representation.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if sys.version_info[0] >= 3:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        hexstr = str(binascii.hexlify(byte), "utf-8")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    else:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        hexstr = str(binascii.hexlify(byte))
    # Pedagogical note: the next line explains one concrete step in the program flow.
    data = []
    # Pedagogical note: the next line explains one concrete step in the program flow.
    for i in range(0, len(hexstr), 2):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        data.append("%s" % hexstr[i:i + 2].upper())
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return ' '.join(data)


# Pedagogical note: the next line explains one concrete step in the program flow.
def hex_to_bytes(hexstr):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert a string hex byte values into a byte string.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return binascii.unhexlify(hexstr.replace(' ', '').encode('utf-8'))


# Pedagogical note: the next line explains one concrete step in the program flow.
def byte_to_binary(byte):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert byte to binary string representation.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    E.g.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> byte_to_binary("\x4A")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '0000000001001010'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return ''.join(str((byte & (1 << i)) and 1) for i in reversed(range(8)))


# Pedagogical note: the next line explains one concrete step in the program flow.
def bytes_to_binary(values):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert bytes to binary string representation.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    E.g.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> bytes_to_binary(b"\x4A\xFF")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '0100101011111111'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if is_py3:
        # TODO: Python 3 convert \x00 to integer 0 ?
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if values == 0:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            data = '00000000'
        # Pedagogical note: the next line explains one concrete step in the program flow.
        else:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            data = ''.join([byte_to_binary(b) for b in values])
    # Pedagogical note: the next line explains one concrete step in the program flow.
    else:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        data = ''.join(byte_to_binary(ord(b)) for b in values)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return data


# Pedagogical note: the next line explains one concrete step in the program flow.
def hex_to_binary(hexstr):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert hexadecimal string to binary string representation.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    E.g.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> hex_to_binary("FF")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '11111111'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if is_py3:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return ''.join(byte_to_binary(b) for b in hex_to_bytes(hexstr))
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return ''.join(byte_to_binary(ord(b)) for b in hex_to_bytes(hexstr))


# Pedagogical note: the next line explains one concrete step in the program flow.
def binary_to_int(buf, start=0, stop=None):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Convert binary string representation to integer.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    E.g.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> binary_to_int('1111110')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    126
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> binary_to_int('1111110', 0, 2)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    2
    # Pedagogical note: the next line explains one concrete step in the program flow.
    >>> binary_to_int('1111110', 0, 3)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    6
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return int(buf[::-1][start:(stop or len(buf))][::-1], 2)


# Pedagogical note: the next line explains one concrete step in the program flow.
def csv_to_dict(file_input, delimiter=','):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Deserialize csv to list of dictionaries.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    delimiter = to_char(delimiter)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    table = []
    # Pedagogical note: the next line explains one concrete step in the program flow.
    reader = csv.DictReader(file_input, delimiter=delimiter,
                            # Pedagogical note: the next line explains one concrete step in the program flow.
                            skipinitialspace=True)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    for d in reader:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        table.append(d)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return ListDict(table)


# Pedagogical note: the next line explains one concrete step in the program flow.
def dict_to_csv(items, delimiter, header):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Serialize list of dictionaries to csv.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    content = ""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if len(items) > 0:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        delimiter = to_char(delimiter)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        output = StringIO()
        # Pedagogical note: the next line explains one concrete step in the program flow.
        csvwriter = csv.DictWriter(output, fieldnames=items[0].keys(),
                                   # Pedagogical note: the next line explains one concrete step in the program flow.
                                   delimiter=delimiter)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if header:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            csvwriter.writerow(dict((key, key) for key in items[0].keys()))
            # writeheader is not supported in python2.6
            # csvwriter.writeheader()
        # Pedagogical note: the next line explains one concrete step in the program flow.
        for item in items:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            csvwriter.writerow(dict(item))

        # Pedagogical note: the next line explains one concrete step in the program flow.
        content = output.getvalue()
        # Pedagogical note: the next line explains one concrete step in the program flow.
        output.close()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return content


# Pedagogical note: the next line explains one concrete step in the program flow.
class Dict(OrderedDict):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''A dict with somes additional methods.'''

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def filter(self, keys):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Create a dict with only the following `keys`.

        # Pedagogical note: the next line explains one concrete step in the program flow.
        >>> mydict = Dict({"name":"foo", "firstname":"bar", "age":1})
        # Pedagogical note: the next line explains one concrete step in the program flow.
        >>> mydict.filter(['age', 'name'])
        # Pedagogical note: the next line explains one concrete step in the program flow.
        {'age': 1, 'name': 'foo'}
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        data = Dict()
        # Pedagogical note: the next line explains one concrete step in the program flow.
        real_keys = set(self.keys()) - set(set(self.keys()) - set(keys))
        # Pedagogical note: the next line explains one concrete step in the program flow.
        for key in keys:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            if key in real_keys:
                # Pedagogical note: the next line explains one concrete step in the program flow.
                data[key] = self[key]
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return data

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def to_csv(self, delimiter=',', header=True):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Serialize list of dictionaries to csv.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return dict_to_csv([self], delimiter, header)


# Pedagogical note: the next line explains one concrete step in the program flow.
class ListDict(list):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''List of dicts with somes additional methods.'''

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def to_csv(self, delimiter=',', header=True):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Serialize list of dictionaries to csv.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return dict_to_csv(list(self), delimiter, header)

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def filter(self, keys):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Create a list of dictionaries with only the following `keys`.

        # Pedagogical note: the next line explains one concrete step in the program flow.
        >>> mylist = ListDict([{"name":"foo", "age":31},
        # Pedagogical note: the next line explains one concrete step in the program flow.
        ...                    {"name":"bar", "age":24}])
        # Pedagogical note: the next line explains one concrete step in the program flow.
        >>> mylist.filter(['name'])
        # Pedagogical note: the next line explains one concrete step in the program flow.
        [{'name': 'foo'}, {'name': 'bar'}]
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        items = ListDict()
        # Pedagogical note: the next line explains one concrete step in the program flow.
        for item in self:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            items.append(item.filter(keys))
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return items

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def sorted_by(self, keyword, reverse=False):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Returns list sorted by `keyword`.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        key_ = keyword
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return ListDict(sorted(self, key=lambda k: k[key_], reverse=reverse))
