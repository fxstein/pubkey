#!/usr/local/bin/python3 -u
#
# The MIT License (MIT)
#
# Copyright (c) 2015 by Oliver Ratzesberger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Make sure correct version of python is being used.
if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and
                               sys.version_info[1] < 4):
    print("pubkey requires Python 3.4 or later.")
    sys.exit(1)

sys.path.insert(0, os.path.abspath('pubkey'))
from pubkey import __version__, __author__, __email__, __license__

# For development versions add current timestamp of build. We could use git
# but that would required a commit for every change before being able to test
# the build locally
if __version__.find('dev') is not -1:
    import time
    __version__ = __version__ + time.strftime('%Y%m%d%H%M%S')

setup(
    name='pubkey',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,  # noqa

    description='Public Key Distribution made simple.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/fxstein/pubkey',

    # Author details
    author=__author__,
    author_email=__email__,

    # Choose your license
    license=__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: System :: Systems Administration',
        'Topic :: Security :: Cryptography',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',

    ],

    # What does your project relate to?
    keywords='public private keys pairs security ssh rest asyncio cement',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'asyncio>=3.4.0',
        'aiohttp>=0.17.0',
        'cement>=2.6.0',
        'colorlog>=2.6.0',
    ],

    scripts=[
        'pubkey/pubkey'
    ]
)
