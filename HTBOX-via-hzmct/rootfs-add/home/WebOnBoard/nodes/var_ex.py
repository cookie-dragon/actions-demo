#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/12 21:36
# @Author  : Cooky Long
# @File    : var_ex
from nodes.node import Node
from nodes import NodesConfigError


class VarEx(Node):
    def __init__(self, node):
        super(VarEx, self).__init__(node)

        try:
            # type - 8位整形枚举
            # 0:int
            # 1:float
            # 2:double
            # 9:bit
            # ##
            self.typ = self.node['var_ex'][0]

            # decimal_digits - 小数位数(type = int时，大于0表示字节第几bit)
            # 0:0位
            # 1:1位
            # 2:2位
            # 3:3位
            # …
            # ##
            self.decimal_digits = self.node['var_ex'][3]

            # mul - 乘数
            # ##
            self.mul = self.node['var_ex'][4]

            # div - 除数
            # ##
            self.div = self.node['var_ex'][5]

            # accessmode - 上传方式
            # 0:normal（正常上传）
            # 1:subtract（差值上传）
            # ##
            self.accessmode = self.node['var_ex'][8]

            # index - OPC中表示矩阵参数行
            # ##
            self.index = self.node['var_ex'][12]

            # subindex - OPC中表示矩阵参数列
            # ##
            self.subindex = self.node['var_ex'][13]

            # hnpchicpath - OPC中表示参数路径
            # ##
            self.hnpchicpath = self.node['var_ex'][20]
        except Exception:
            raise NodesConfigError("var_ex decode error")
