#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : network.py

class NetworkInterface(object):

    def __init__(self, jsondict_iface, typ_iface, index):
        self.jsondict_iface = jsondict_iface
        self.typ_iface = typ_iface
        self.index = index
        self.mode = self.jsondict_iface['mode']

    def get_name(self):
        return self.typ_iface + str(self.index)

    def check_conf(self):
        rtn_sys = 1
        return rtn_sys

    def config(self):
        rtn_sys = 1
        return rtn_sys

    def start(self):
        rtn_sys = 1
        return rtn_sys

    def stop(self):
        rtn_sys = 1
        return rtn_sys
