#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.hnpc_error import NodesConfigError
from hnpc.node import Node


class ProductNodeProduct(object):
    def __init__(self, l_product):
        try:
            self.protocol = int(l_product[0])  # 0:MODBUS 1:MODBUS TCP 2:CANOpen 3.Simenes7（西门子） 4.HNPC(Hi设备专用) 5.OPCUA 6.FINS/TCP（欧姆龙） 7.MC(三菱Q/L专用) 8.MC(三菱FX专用) 9.ADS(倍福专用)
            self.port = int(l_product[1])  # 0:485 1:232 2:CAN 3.NET
            self.baud = int(l_product[2])  # 无符号32位整数
            self.ip = int(l_product[3])  # 无符号32位整数
            self.Invterport = int(l_product[4])  # 无符号16位整数
            self.data_bit = int(l_product[5])  # 无符号16位整数
            self.stop_bits = int(l_product[6])  # 无符号16位整数
            self.parity = int(l_product[7])  # 无符号16位整数
        except Exception:
            raise NodesConfigError("node product decode error")


class ProductNode(Node):
    def __init__(self, node):
        super().__init__(node)
        self.product = ProductNodeProduct(node['product'])
