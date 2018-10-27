#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 22:12:21 2018

@author: tzech
"""

from distutils.core import setup

from modres import __version__

setup(name='modres',
      version=__version__,
      description='model-based resampling',
      author='Tobias Zech'
     )