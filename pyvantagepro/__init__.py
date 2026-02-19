# -*- coding: utf-8 -*-
'''
    pyvantagepro
    ------------

    The public API and command-line interface to PyVantagePro package.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
# Make sure the logger is configured early:
from .logger import LOGGER, active_logger
try:
    from .device import VantagePro2
except ImportError:
    # Keep top-level imports usable when optional runtime deps (pylink)
    # are not installed, e.g. parser/utils-only environments.
    VantagePro2 = None

VERSION = '0.4.0dev'
__version__ = VERSION
