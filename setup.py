#!/usr/bin/python

import os
import sys
from setuptools import setup, Command

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = read('requirements.txt')

setup(
    name = "RhymerFinder",
    version = "1.0",
    author = "John Case",
    author_email = "johnchuckcase@gmail.com",
    license = "GPLv3",
    url = "https://github.com/johnchuckcase/RhymerFinder",
    packages=['RhymerFinder'],
    include_package_data=True,
    install_requires = install_requires,
)
