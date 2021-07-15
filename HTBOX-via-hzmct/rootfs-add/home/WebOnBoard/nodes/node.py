#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/12 21:40
# @Author  : Cooky Long
# @File    : node
from nodes import NodesConfigError


class Node(object):
    def __init__(self, node):
        self.node = node
        try:
            self.id = node['attribute'][0]
            self.clazz = node['attribute'][1]
            self.name = node['attribute'][2]
            self.path = node['attribute'][3]
        except Exception:
            raise NodesConfigError("attribute decode error")
