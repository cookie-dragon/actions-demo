#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.p_node_varex.inode_varex import VarNodeVarExI, VarNodeExI


class VarNodeVarEx0(VarNodeVarExI):  # 0:int
    def __init__(self):
        super().__init__()
        self.symbol = int(0)  # 有无符号 0:无符号 1:有符号
        self.mul = int(1)  # 16位整数
        self.div = int(1)  # 16位整数
        self.valuesize = int(0)  # 0:8位 1:16位 2:32位 3:64位
        self.index = int(0)  # 无符号16位整数
        self.subindex = int(0)  # 无符号16位整数
        self.hnpchicpath = str("")

        self.value = int(0)

    def init(self, l_varex):
        super().init(l_varex)
        self.symbol = int(l_varex[2])
        self.mul = int(l_varex[4])
        self.div = int(l_varex[5])
        self.valuesize = int(l_varex[6])
        self.index = int(l_varex[12])
        self.subindex = int(l_varex[13])
        self.hnpchicpath = str(l_varex[20])

    def read_value(self):
        disp_value = int(self.value * self.mul / self.div)
        return disp_value

    def write_value(self, disp_value):
        self.value = int(disp_value * self.div / self.mul)


class VarNodeEx0(VarNodeExI):
    def __init__(self, node):
        super().__init__(node)
        self.var = None

    def init(self):
        self.var = VarNodeVarEx0()
        self.var.init(self.node['var_ex'])
