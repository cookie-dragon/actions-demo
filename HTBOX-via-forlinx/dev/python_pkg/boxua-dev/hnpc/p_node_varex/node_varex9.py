#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.p_node_varex.inode_varex import VarNodeVarExI, VarNodeExI


class VarNodeVarEx9(VarNodeVarExI):  # 9:bit
    def __init__(self):
        super().__init__()
        self.decimal_digits = int(0)  # 左移位数 0:0位 1:1位 2:2位 3:3位 …
        self.index = int(0)  # 无符号16位整数
        self.subindex = int(0)  # 无符号16位整数
        self.hnpchicpath = str("")

        self.value = int(0)

    def init(self, l_varex):
        super().init(l_varex)
        self.decimal_digits = int(l_varex[3])  # 左移位数 0:0位 1:1位 2:2位 3:3位 …
        self.index = int(l_varex[12])  # 无符号16位整数
        self.subindex = int(l_varex[13])  # 无符号16位整数
        self.hnpchicpath = str(l_varex[20])

    def read_value(self):
        if self.value & (1 << self.decimal_digits):
            disp_value = True
        else:
            disp_value = False
        return disp_value

    def write_value(self, disp_value):
        if not disp_value:  # False 0
            self.value = self.value & (~(1 << self.decimal_digits))
        else:
            self.value = self.value | (1 << self.decimal_digits)


class VarNodeEx9(VarNodeExI):
    def __init__(self, node):
        super().__init__(node)
        self.var = None

    def init(self):
        self.var = VarNodeVarEx9()
        self.var.init(self.node['var_ex'])
