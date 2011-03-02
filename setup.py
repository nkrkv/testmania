#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from testmania import __version__
from setuptools import setup

install_requires = []
if sys.version_info[0:2] < (2, 7):
    install_requires.append('unittest2')

setup(
    name='testmania',
    version=__version__,
    description='Library of assert_xxx functions for more convenient testing',
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
