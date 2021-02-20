#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:35 下午
# @Author  : Cooky Long
# @File    : setup.py
from distutils.core import setup

setup(name='htbox',
      version='1.0',
      description='Script for HTBOX',
      author='Cooky Long',
      author_email='lj12875@mail.haitian.com',
      packages=['htbox',
                'htbox/interface', 'htbox/routetable', 'htbox/shell']
      )
