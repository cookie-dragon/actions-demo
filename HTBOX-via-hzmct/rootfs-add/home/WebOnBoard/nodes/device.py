#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/12 21:33
# @Author  : Cooky Long
# @File    : device
import ipaddress

from datareader import d_opcua_reader
from datareader.opcua_reader import OpcuaReader
from nodes import NodesConfigError
from nodes.node import Node


class Device(Node):

    def __init__(self, node):
        super(Device, self).__init__(node)

        try:
            if len(self.node['reference']) != 1:
                raise NodesConfigError("Device reference is not equal 1")
        except Exception:
            raise NodesConfigError("reference decode error")

        self.product = None
        self.d_accessmode1 = dict()

        try:
            # collect_cycle - 采集周期ms
            # ##
            self.collect_cycle = self.node['device'][1]

            # report_cycle - 上报周期ms
            # ##
            self.report_cycle = self.node['device'][2]
        except Exception:
            raise NodesConfigError("device decode error")

    def setProduct(self, product):
        self.product = product

        # OPCUA模式
        if self.product.protocol == 5 and self.product.port == 3:
            try:
                # dev_InvterPort - IP地址中的端口
                # ##
                self.dev_InvterPort = self.node['device'][5]

                # dev_InvterPort - IP地址中的IP（整型数字模式）
                # ##
                self.dev_IP = self.node['device'][6]

                # url - OPCUA中服务器路径后缀
                # ##
                self.url = self.node['device'][8]
            except Exception:
                raise NodesConfigError("device decode error")

            # OPCUA中服务器路径（拼接）
            endPointUrl = 'opc.tcp://' + ipaddress.IPv4Address(self.dev_IP).compressed + ':' + str(
                self.dev_InvterPort) + self.url

            if endPointUrl not in d_opcua_reader:
                d_opcua_reader[endPointUrl] = OpcuaReader(endPointUrl=endPointUrl)
            self.reader = d_opcua_reader[endPointUrl]

    def get_bit_val(self, i, index):
        if i & (1 << index):
            return 1
        else:
            return 0

    def getMsg(self):
        msg = dict()
        if self.product.protocol == 5 and self.product.port == 3:
            for var_ex in self.product.l_var_ex:
                value = self.reader.getData(var_ex.hnpchicpath, var_ex.index, var_ex.subindex)

                # value校验 - 返回类型是否与设定类型一致
                checkRst = False
                if var_ex.typ == 0:
                    if type(value) == int:
                        checkRst = True
                elif var_ex.typ == 1 or var_ex.typ == 2:
                    if type(value) == float:
                        checkRst = True
                elif var_ex.typ == 9:
                    if value == 0 or value == 1:
                        checkRst = True

                if checkRst:
                    # value修饰 - 是否按位
                    if type(value) == int and var_ex.typ == 9:
                        value = self.get_bit_val(value, var_ex.decimal_digits)
                    else:
                        # value修饰 - 乘除处理
                        value = value * var_ex.mul / var_ex.div
                        # value修饰 - 小数位数
                        if type(value) == float:
                            if var_ex.decimal_digits > 0:
                                value = round(value, var_ex.decimal_digits)
                            else:
                                value = int(value)

                    # value修饰 - 上传方式
                    if var_ex.accessmode == 1:
                        if var_ex.name in self.d_accessmode1:
                            value = value - self.d_accessmode1[var_ex.name]
                            msg[var_ex.name] = value
                        self.d_accessmode1[var_ex.name] = value
                    else:
                        msg[var_ex.name] = value

        return msg
