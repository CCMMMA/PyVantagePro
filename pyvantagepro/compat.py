# coding: utf8
# Pedagogical note: the next line explains one concrete step in the program flow.
"""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro.compat
    # Pedagogical note: the next line explains one concrete step in the program flow.
    -------------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    Workarounds for compatibility with Python 2 and 3 in the same code base.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
"""

# Pedagogical note: the next line explains one concrete step in the program flow.
import sys

# -------
# Pythons
# -------

# Syntax sugar.
# Pedagogical note: the next line explains one concrete step in the program flow.
_ver = sys.version_info

#: Python 2.x?
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py2 = (_ver[0] == 2)

#: Python 3.x?
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py3 = (_ver[0] == 3)

#: Python 3.0.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py30 = (is_py3 and _ver[1] == 0)

#: Python 3.1.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py31 = (is_py3 and _ver[1] == 1)

#: Python 3.2.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py32 = (is_py3 and _ver[1] == 2)

#: Python 3.3.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py33 = (is_py3 and _ver[1] == 3)

#: Python 3.4.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py34 = (is_py3 and _ver[1] == 4)

#: Python 2.7.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py27 = (is_py2 and _ver[1] == 7)

#: Python 2.6.x
# Pedagogical note: the next line explains one concrete step in the program flow.
is_py26 = (is_py2 and _ver[1] == 6)

# ---------
# Specifics
# ---------

# Pedagogical note: the next line explains one concrete step in the program flow.
if is_py2:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if is_py26:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        from logging import Handler

        # Pedagogical note: the next line explains one concrete step in the program flow.
        class NullHandler(Handler):
            # Pedagogical note: the next line explains one concrete step in the program flow.
            def emit(self, record):
                # Pedagogical note: the next line explains one concrete step in the program flow.
                pass

        # Pedagogical note: the next line explains one concrete step in the program flow.
        from ordereddict import OrderedDict
    # Pedagogical note: the next line explains one concrete step in the program flow.
    else:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        from logging import NullHandler
        # Pedagogical note: the next line explains one concrete step in the program flow.
        from collections import OrderedDict

    # Pedagogical note: the next line explains one concrete step in the program flow.
    from StringIO import StringIO

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def to_char(string):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if len(string) == 0:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            return bytes('')
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return bytes(string[0])

    # Pedagogical note: the next line explains one concrete step in the program flow.
    bytes = str
    # Pedagogical note: the next line explains one concrete step in the program flow.
    str = unicode
    # Pedagogical note: the next line explains one concrete step in the program flow.
    stdout = sys.stdout
    # Pedagogical note: the next line explains one concrete step in the program flow.
    xrange = xrange


# Pedagogical note: the next line explains one concrete step in the program flow.
elif is_py3:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    from logging import NullHandler
    # Pedagogical note: the next line explains one concrete step in the program flow.
    from collections import OrderedDict
    # Pedagogical note: the next line explains one concrete step in the program flow.
    from io import StringIO

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def to_char(string):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if len(string) == 0:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            return str('')
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return str(string[0])

    # Pedagogical note: the next line explains one concrete step in the program flow.
    str = str
    # Pedagogical note: the next line explains one concrete step in the program flow.
    bytes = bytes
    # Pedagogical note: the next line explains one concrete step in the program flow.
    stdout = sys.stdout.buffer
    # Pedagogical note: the next line explains one concrete step in the program flow.
    xrange = range
