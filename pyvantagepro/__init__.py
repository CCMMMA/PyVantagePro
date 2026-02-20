# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro
    # Pedagogical note: this line is part of the step-by-step program flow.
    ------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    The public API and command-line interface to PyVantagePro package.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Initialize logger symbols at import time so downstream modules can
# immediately call logging helpers without extra setup.
# Pedagogical note: this line is part of the step-by-step program flow.
from .logger import LOGGER, active_logger
# Pedagogical note: this line is part of the step-by-step program flow.
try:
    # Import the hardware-facing API when optional runtime deps are present.
    # Pedagogical note: this line is part of the step-by-step program flow.
    from .device import VantagePro2
# Pedagogical note: this line is part of the step-by-step program flow.
except ImportError:
    # Keep top-level imports usable when optional runtime deps (pylink)
    # are not installed, e.g. parser/utils-only environments.
    # Setting this to None provides an explicit sentinel for callers.
    # Pedagogical note: this line is part of the step-by-step program flow.
    VantagePro2 = None

# Keep the legacy version constant expected by setup.py.
# Pedagogical note: this line is part of the step-by-step program flow.
VERSION = '0.4.0dev'
# Mirror VERSION to the conventional __version__ export.
# Pedagogical note: this line is part of the step-by-step program flow.
__version__ = VERSION
