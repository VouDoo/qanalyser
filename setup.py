#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All modules below are part of standard distribution for python
import os
import sys

from setuptools import setup
from setuptools import find_packages


# Check Python version
current_python = sys.version_info[:2]
required_python = (3, 4)
if current_python < required_python:
    sys.stderr.write("""
--------------------------
Unsupported Python version
--------------------------
This version requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(required_python + current_python)))
    sys.exit(1)


def readfile(file_name):
    """
    Return file content in a string
    """
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='Qanalyser',
    version=__import__('qanalyser').get_version(),
    description='Analyser for database queries',
    long_description=readfile('README.md'),
    author='Maxence Grymonprez',
    author_email='maxgrymonprez@live.fr',
    url='https://github.com/VouDoo/Qanalyser',
    license=readfile('LICENSE'),
    python_requires='>=3.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'pyodbc',
        'Jinja2'
    ]
)
