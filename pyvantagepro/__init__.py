# -*- coding: utf-8 -*-
'''
    pyvantagepro
    ------------

    The public API and command-line interface to PyVantagePro package.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
# Initialize logger symbols at import time so downstream modules can
# immediately call logging helpers without extra setup.
from .logger import LOGGER, active_logger
try:
    # Import the hardware-facing API when optional runtime deps are present.
    from .device import VantagePro2
except ImportError:
    # Keep top-level imports usable when optional runtime deps (pylink)
    # are not installed, e.g. parser/utils-only environments.
    # Setting this to None provides an explicit sentinel for callers.
    VantagePro2 = None

# Keep the legacy version constant expected by setup.py.
VERSION = '0.4.0dev'
# Mirror VERSION to the conventional __version__ export.
__version__ = VERSION
