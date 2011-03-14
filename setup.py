#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup


install_requires = []
if sys.version_info[0:2] < (2, 7):
    install_requires.append('unittest2')


try:
    readme_content = open("README.rst").read()
except:
    readme_content = ""


setup(
    name='testmania',
    version='0.4.2',
    description='Library of assert_xxx functions for more convenient testing',
    long_description=readme_content,
    author='Victor Nakoryakov (aka nailxx)',
    author_email='nail.xx@gmail.com',
    license='MIT',
    keywords="test unittest assert",
    url='https://github.com/nailxx/testmania',
    packages=['testmania'],
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
