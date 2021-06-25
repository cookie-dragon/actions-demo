#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.node import Node


class ValueNodeValueI(object):
    def __init__(self):
        self.type = int(0)  # 8位整形枚举 0:int 1:float 2:double 3:string 4:enum 5:timestamp 9:bit
        self.rw = int(0)  # 0:可读 1:可读写 2.只写 3.周期写

    def init(self, l_var):
        self.type = int(l_var[0])
        self.rw = int(l_var[1])


class ValueNodeI(Node):
    def __init__(self, node):
        super().__init__(node)
        self.var = None

    def init(self):
        self.var = ValueNodeValueI()
        self.var.init(self.node['var'])
