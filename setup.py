#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path

from setuptools import setup
from testmania import __version__

install_requires = []
if sys.version_info[0:2] < (2, 7):
    install_requires.append('unittest2')

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='testmania',
    version=__version__,
    description='Library of assert_xxx functions for more convenient testing',
    long_description=read('README.rst'),
    author='Victor Nakoryakov (aka nailxx)',
    author_email='nail.xx@gmail.com',
    license='MIT',
    keywords="test unittest assert",
    url='https://github.com/nailxx/testmania',
    py_modules=['testmania'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
)
