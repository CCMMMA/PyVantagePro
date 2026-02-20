# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
"""
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.logger
    # Pedagogical note: this line is part of the step-by-step program flow.
    -------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    Logging setup.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
"""
# Pedagogical note: this line is part of the step-by-step program flow.
from __future__ import unicode_literals
# Pedagogical note: this line is part of the step-by-step program flow.
import logging
# Pedagogical note: this line is part of the step-by-step program flow.
from .compat import NullHandler


# Pedagogical note: this line is part of the step-by-step program flow.
LOGGER = logging.getLogger('pyvpdriver')
# Pedagogical note: this line is part of the step-by-step program flow.
LOGGER.addHandler(NullHandler())


# Pedagogical note: this line is part of the step-by-step program flow.
def active_logger():
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Initialize a speaking logger with stream handler (stderr).'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    LOGGER = logging.getLogger('pyvpdriver')

    # Pedagogical note: this line is part of the step-by-step program flow.
    LOGGER.setLevel(logging.INFO)
    # Pedagogical note: this line is part of the step-by-step program flow.
    logging.getLogger('pylink').setLevel(logging.INFO)

    # Default to logging to stderr.
    # Pedagogical note: this line is part of the step-by-step program flow.
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s ')
    # Pedagogical note: this line is part of the step-by-step program flow.
    stream_handler = logging.StreamHandler()
    # Pedagogical note: this line is part of the step-by-step program flow.
    stream_handler.setFormatter(formatter)

    # Pedagogical note: this line is part of the step-by-step program flow.
    LOGGER.addHandler(stream_handler)
    # Pedagogical note: this line is part of the step-by-step program flow.
    logging.getLogger('pylink').addHandler(stream_handler)
