# coding: utf8
# Pedagogical note: the next line explains one concrete step in the program flow.
'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    PyVantagePro
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    Communication tools for the Davis VantagePro2 devices.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
'''
# Pedagogical note: the next line explains one concrete step in the program flow.
import re
# Pedagogical note: the next line explains one concrete step in the program flow.
import sys
# Pedagogical note: the next line explains one concrete step in the program flow.
import os
# Pedagogical note: the next line explains one concrete step in the program flow.
from setuptools import setup, find_packages

# Pedagogical note: the next line explains one concrete step in the program flow.
here = os.path.abspath(os.path.dirname(__file__))

# Pedagogical note: the next line explains one concrete step in the program flow.
README = ''
# Pedagogical note: the next line explains one concrete step in the program flow.
CHANGES = ''
# Pedagogical note: the next line explains one concrete step in the program flow.
try:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    README = open(os.path.join(here, 'README.rst')).read()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
# Pedagogical note: the next line explains one concrete step in the program flow.
except:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pass

# Pedagogical note: the next line explains one concrete step in the program flow.
REQUIREMENTS = [
    # Pedagogical note: the next line explains one concrete step in the program flow.
    'pylink',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    'progressbar-latest',
# Pedagogical note: the next line explains one concrete step in the program flow.
]

# Pedagogical note: the next line explains one concrete step in the program flow.
if sys.version_info < (2, 7):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    REQUIREMENTS.append('ordereddict')

# Pedagogical note: the next line explains one concrete step in the program flow.
if sys.version_info < (2, 7) or (3,) <= sys.version_info < (3, 2):
    # In the stdlib from 2.7:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    REQUIREMENTS.append('argparse')


# Pedagogical note: the next line explains one concrete step in the program flow.
with open(os.path.join(os.path.dirname(__file__), 'pyvantagepro',
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        '__init__.py')) as init_py:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    release = re.search("VERSION = '([^']+)'", init_py.read()).group(1)
# The short X.Y version.
# Pedagogical note: the next line explains one concrete step in the program flow.
version = release.rstrip('dev')

# Pedagogical note: the next line explains one concrete step in the program flow.
setup(
    # Pedagogical note: the next line explains one concrete step in the program flow.
    name='PyVantagePro',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    version=version,
    # Pedagogical note: the next line explains one concrete step in the program flow.
    url='https://github.com/SalemHarrache/PyVantagePro',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    license='GNU GPL v3',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    description='Communication tools for the Davis VantagePro2 devices',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    long_description=README + '\n\n' + CHANGES,
    # Pedagogical note: the next line explains one concrete step in the program flow.
    author='Salem Harrache',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    author_email='salem.harrache@gmail.com',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    maintainer='Lionel Darras',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    maintainer_email='Lionel.Darras@obs.ujf-grenoble.fr',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    classifiers=[
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Development Status :: 4 - Beta',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Intended Audience :: Science/Research',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Intended Audience :: Developers',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Programming Language :: Python :: 2',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Programming Language :: Python :: 2.6',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Programming Language :: Python :: 2.7',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Programming Language :: Python :: 3',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Programming Language :: Python :: 3.2',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Topic :: Internet',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Topic :: Utilities',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'Topic :: Software Development :: Libraries :: Python Modules'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ],
    # Pedagogical note: the next line explains one concrete step in the program flow.
    packages=find_packages(),
    # Pedagogical note: the next line explains one concrete step in the program flow.
    zip_safe=False,
    # Pedagogical note: the next line explains one concrete step in the program flow.
    install_requires=REQUIREMENTS,
    # Pedagogical note: the next line explains one concrete step in the program flow.
    test_suite='pyvantagepro.tests',
    # Pedagogical note: the next line explains one concrete step in the program flow.
    entry_points={
        # Pedagogical note: the next line explains one concrete step in the program flow.
        'console_scripts': [
            # Pedagogical note: the next line explains one concrete step in the program flow.
            'pyvantagepro = pyvantagepro.__main__:main'
        # Pedagogical note: the next line explains one concrete step in the program flow.
        ],
    # Pedagogical note: the next line explains one concrete step in the program flow.
    },
# Pedagogical note: the next line explains one concrete step in the program flow.
)
