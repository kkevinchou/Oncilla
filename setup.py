from __future__ import absolute_import
import os
import sys

from setuptools import setup, find_packages

setup(
    name='Oncilla',
    version='1.0',
    description='Oncilla',
    author='Kevin Chou',
    author_email='kkevinchou@gmail.com',
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
)
