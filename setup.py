#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 22:12:21 2018

@author: tzech
"""
from setuptools import setup, find_packages

__version__ = '0.1.0_alpha'

setup(
    name='modres',
    version=__version__,
    description='Model-based resampling',
    long_description='A Python package for deterministic and stochastic resampling of time series data.',
    author='Tobias Zech',
    license='MIT',
    url='https://github.com/tozech/modres',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'pytest'
    ],
)

