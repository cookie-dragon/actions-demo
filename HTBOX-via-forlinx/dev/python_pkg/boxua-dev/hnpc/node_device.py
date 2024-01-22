#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hnpc.hnpc_error import NodesConfigError
from hnpc.node import Node


class DeviceNodeDevice(object):
    def __init__(self, l_device):
        try:
            self.addr = int(l_device[0])  # 无符号32位整数
            self.collect_cycle = int(l_device[1])  # 无符号32位整数
            self.report_cycle = int(l_device[2])  # 无符号32位整数
            self.collect_min_interver = int(l_device[3])  # 无符号32位整数
            self.dev_collect_min_interval = int(l_device[4])  # 无符号16位整数
            self.dev_InvterPort = int(l_device[5])  # 无符号16位整数
            self.dev_IP = int(l_device[6])  # 无符号16位整数
            self.dev_destserver = int(l_device[7])  # 无符号32位整数
            self.dev_serverpath = str(l_device[8])  # 字符串(OPCUA-新增服务器路径)
            self.dev_adsnetip = int(l_device[9])  # 无符号32位整数
            self.dev_adsnetid = int(l_device[10])  # 无符号16位整数
        except Exception:
            raise NodesConfigError("node device decode error")


class DeviceNode(Node):
    def __init__(self, node):
        super().__init__(node)
        self.device = DeviceNodeDevice(node['device'])
