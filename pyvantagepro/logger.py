# -*- coding: utf-8 -*-
# Pedagogical note: the next line explains one concrete step in the program flow.
"""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro.logger
    # Pedagogical note: the next line explains one concrete step in the program flow.
    -------------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    Logging setup.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
"""
# Pedagogical note: the next line explains one concrete step in the program flow.
from __future__ import unicode_literals
# Pedagogical note: the next line explains one concrete step in the program flow.
import logging
# Pedagogical note: the next line explains one concrete step in the program flow.
from .compat import NullHandler


# Pedagogical note: the next line explains one concrete step in the program flow.
LOGGER = logging.getLogger('pyvpdriver')
# Pedagogical note: the next line explains one concrete step in the program flow.
LOGGER.addHandler(NullHandler())


# Pedagogical note: the next line explains one concrete step in the program flow.
def active_logger():
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Initialize a speaking logger with stream handler (stderr).'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    LOGGER = logging.getLogger('pyvpdriver')

    # Pedagogical note: the next line explains one concrete step in the program flow.
    LOGGER.setLevel(logging.INFO)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    logging.getLogger('pylink').setLevel(logging.INFO)

    # Default to logging to stderr.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s ')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    stream_handler = logging.StreamHandler()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    stream_handler.setFormatter(formatter)

    # Pedagogical note: the next line explains one concrete step in the program flow.
    LOGGER.addHandler(stream_handler)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    logging.getLogger('pylink').addHandler(stream_handler)
