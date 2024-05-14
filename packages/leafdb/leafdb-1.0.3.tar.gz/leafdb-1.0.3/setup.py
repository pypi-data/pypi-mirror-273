#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from leafdb import __version__

setup(
  name='leafdb',
  version=__version__,
  author='Huaqing Ye',
  author_email='wacunye@outlook.com',
  url='http://www.leafpy.org/',
  py_modules=['leafdb'],
  description='LeafDb library',
  long_description="LeafDb is a simple library for makeing raw SQL queries to most relational databases.",
  install_requires = ['sqlalchemy<2.0'],
  license="MIT license",
  platforms=["any"],
)
