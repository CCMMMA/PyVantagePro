# coding: utf8
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    PyVantagePro
    # Pedagogical note: this line is part of the step-by-step program flow.
    ------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    Communication tools for the Davis VantagePro2 devices.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Pedagogical note: this line is part of the step-by-step program flow.
import re
# Pedagogical note: this line is part of the step-by-step program flow.
import sys
# Pedagogical note: this line is part of the step-by-step program flow.
import os
# Pedagogical note: this line is part of the step-by-step program flow.
from setuptools import setup, find_packages

# Pedagogical note: this line is part of the step-by-step program flow.
here = os.path.abspath(os.path.dirname(__file__))

# Pedagogical note: this line is part of the step-by-step program flow.
README = ''
# Pedagogical note: this line is part of the step-by-step program flow.
CHANGES = ''
# Pedagogical note: this line is part of the step-by-step program flow.
try:
    # Pedagogical note: this line is part of the step-by-step program flow.
    README = open(os.path.join(here, 'README.rst')).read()
    # Pedagogical note: this line is part of the step-by-step program flow.
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
# Pedagogical note: this line is part of the step-by-step program flow.
except:
    # Pedagogical note: this line is part of the step-by-step program flow.
    pass

# Pedagogical note: this line is part of the step-by-step program flow.
REQUIREMENTS = [
    # Pedagogical note: this line is part of the step-by-step program flow.
    'pylink',
    # Pedagogical note: this line is part of the step-by-step program flow.
    'progressbar-latest',
# Pedagogical note: this line is part of the step-by-step program flow.
]

# Pedagogical note: this line is part of the step-by-step program flow.
if sys.version_info < (2, 7):
    # Pedagogical note: this line is part of the step-by-step program flow.
    REQUIREMENTS.append('ordereddict')

# Pedagogical note: this line is part of the step-by-step program flow.
if sys.version_info < (2, 7) or (3,) <= sys.version_info < (3, 2):
    # In the stdlib from 2.7:
    # Pedagogical note: this line is part of the step-by-step program flow.
    REQUIREMENTS.append('argparse')


# Pedagogical note: this line is part of the step-by-step program flow.
with open(os.path.join(os.path.dirname(__file__), 'pyvantagepro',
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        '__init__.py')) as init_py:
    # Pedagogical note: this line is part of the step-by-step program flow.
    release = re.search("VERSION = '([^']+)'", init_py.read()).group(1)
# The short X.Y version.
# Pedagogical note: this line is part of the step-by-step program flow.
version = release.rstrip('dev')

# Pedagogical note: this line is part of the step-by-step program flow.
setup(
    # Pedagogical note: this line is part of the step-by-step program flow.
    name='PyVantagePro',
    # Pedagogical note: this line is part of the step-by-step program flow.
    version=version,
    # Pedagogical note: this line is part of the step-by-step program flow.
    url='https://github.com/SalemHarrache/PyVantagePro',
    # Pedagogical note: this line is part of the step-by-step program flow.
    license='GNU GPL v3',
    # Pedagogical note: this line is part of the step-by-step program flow.
    description='Communication tools for the Davis VantagePro2 devices',
    # Pedagogical note: this line is part of the step-by-step program flow.
    long_description=README + '\n\n' + CHANGES,
    # Pedagogical note: this line is part of the step-by-step program flow.
    author='Salem Harrache',
    # Pedagogical note: this line is part of the step-by-step program flow.
    author_email='salem.harrache@gmail.com',
    # Pedagogical note: this line is part of the step-by-step program flow.
    maintainer='Lionel Darras',
    # Pedagogical note: this line is part of the step-by-step program flow.
    maintainer_email='Lionel.Darras@obs.ujf-grenoble.fr',
    # Pedagogical note: this line is part of the step-by-step program flow.
    classifiers=[
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Development Status :: 4 - Beta',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Intended Audience :: Science/Research',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Intended Audience :: Developers',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Programming Language :: Python :: 2',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Programming Language :: Python :: 2.6',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Programming Language :: Python :: 2.7',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Programming Language :: Python :: 3',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Programming Language :: Python :: 3.2',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Topic :: Internet',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Topic :: Utilities',
        # Pedagogical note: this line is part of the step-by-step program flow.
        'Topic :: Software Development :: Libraries :: Python Modules'
    # Pedagogical note: this line is part of the step-by-step program flow.
    ],
    # Pedagogical note: this line is part of the step-by-step program flow.
    packages=find_packages(),
    # Pedagogical note: this line is part of the step-by-step program flow.
    zip_safe=False,
    # Pedagogical note: this line is part of the step-by-step program flow.
    install_requires=REQUIREMENTS,
    # Pedagogical note: this line is part of the step-by-step program flow.
    test_suite='pyvantagepro.tests',
    # Pedagogical note: this line is part of the step-by-step program flow.
    entry_points={
        # Pedagogical note: this line is part of the step-by-step program flow.
        'console_scripts': [
            # Pedagogical note: this line is part of the step-by-step program flow.
            'pyvantagepro = pyvantagepro.__main__:main'
        # Pedagogical note: this line is part of the step-by-step program flow.
        ],
    # Pedagogical note: this line is part of the step-by-step program flow.
    },
# Pedagogical note: this line is part of the step-by-step program flow.
)
