#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : network.py
from htbox.interface.neti import NetInterface


class NetworkInterface(NetInterface):

    def __init__(self, jsondict_iface, typ_iface, index):
        super().__init__(jsondict_iface)
        self.typ_iface = typ_iface
        self.index = index
        self.mode = self.jsondict_iface['mode']

    def get_name(self):
        return self.typ_iface + str(self.index)
