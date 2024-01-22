#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.p_node_varex.inode_varex import VarNodeVarExI, VarNodeExI


class VarNodeVarEx2(VarNodeVarExI):  # 2:double
    def __init__(self):
        super().__init__()
        self.decimal_digits = int(0)  # 小数位数 0:0位 1:1位 2:2位 3:3位 …
        self.mul = int(1)  # 16位整数
        self.div = int(1)  # 16位整数
        self.index = int(0)  # 无符号16位整数
        self.subindex = int(0)  # 无符号16位整数
        self.hnpchicpath = str("")

        self.value = float(0)

    def init(self, l_varex):
        super().init(l_varex)
        self.decimal_digits = int(l_varex[3])  # 小数位数 0:0位 1:1位 2:2位 3:3位 …
        self.mul = int(l_varex[4])  # 16位整数
        self.div = int(l_varex[5])  # 16位整数
        self.index = int(l_varex[12])  # 无符号16位整数
        self.subindex = int(l_varex[13])  # 无符号16位整数
        self.hnpchicpath = str(l_varex[20])

    def read_value(self):
        disp_value = self.value * self.mul / self.div
        if self.decimal_digits > 0:
            disp_value = round(disp_value, self.decimal_digits)
        else:
            disp_value = int(disp_value)
        return disp_value

    def write_value(self, disp_value):
        value = disp_value * self.div / self.mul


class VarNodeEx2(VarNodeExI):
    def __init__(self, node):
        super().__init__(node)
        self.var = None

    def init(self):
        self.var = VarNodeVarEx2()
        self.var.init(self.node['var_ex'])
