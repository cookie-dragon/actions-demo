#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/12 21:35
# @Author  : Cooky Long
# @File    : product
from nodes.node import Node
from nodes import NodesConfigError


class Product(Node):

    def __init__(self, node):
        super(Product, self).__init__(node)

        self.l_var_ex = list()

        try:
            # protocol - 传输协议
            # 0:MODBUS
            # 1:MODBUS TCP
            # 2:CANOpen
            # 3.Simenes7
            # 4.HNPC
            # 5.OPCUA
            # ##
            self.protocol = self.node['product'][0]

            # port - 传输硬件接口
            # 0:485
            # 1:232
            # 2:CAN
            # 3.NET
            # ##
            self.port = self.node['product'][1]
        except Exception:
            raise NodesConfigError("product decode error")

    def setLVarEx(self, l_var_ex):
        self.l_var_ex = l_var_ex

    def addVarEx(self, var_ex):
        self.l_var_ex.append(var_ex)
