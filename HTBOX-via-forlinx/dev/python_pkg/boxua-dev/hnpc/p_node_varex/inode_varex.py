#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.inode_value import ValueNodeValueI, ValueNodeI


class VarNodeVarExI(ValueNodeValueI):
    def __init__(self):
        super().__init__()

        self.value = None

    def init(self, l_var):
        super().init(l_var)

    def read_value(self):
        disp_value = self.value
        return disp_value

    def write_value(self, disp_value):
        self.value = disp_value


class VarNodeExI(ValueNodeI):
    def __init__(self, node):
        super().__init__(node)

    def init(self):
        self.var = VarNodeVarExI()
        self.var.init(self.node['var_ex'])

    def read(self):
        return self.var.read_value()

    def write(self, disp_value):
        self.var.write_value(disp_value)
