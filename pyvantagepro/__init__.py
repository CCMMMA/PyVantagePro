# -*- coding: utf-8 -*-
# Pedagogical note: the next line explains one concrete step in the program flow.
'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    The public API and command-line interface to PyVantagePro package.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
'''
# Initialize logger symbols at import time so downstream modules can
# immediately call logging helpers without extra setup.
# Pedagogical note: the next line explains one concrete step in the program flow.
from .logger import LOGGER, active_logger
# Pedagogical note: the next line explains one concrete step in the program flow.
try:
    # Import the hardware-facing API when optional runtime deps are present.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    from .device import VantagePro2
# Pedagogical note: the next line explains one concrete step in the program flow.
except ImportError:
    # Keep top-level imports usable when optional runtime deps (pylink)
    # are not installed, e.g. parser/utils-only environments.
    # Setting this to None provides an explicit sentinel for callers.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    VantagePro2 = None

# Keep the legacy version constant expected by setup.py.
# Pedagogical note: the next line explains one concrete step in the program flow.
VERSION = '0.4.0dev'
# Mirror VERSION to the conventional __version__ export.
# Pedagogical note: the next line explains one concrete step in the program flow.
__version__ = VERSION
