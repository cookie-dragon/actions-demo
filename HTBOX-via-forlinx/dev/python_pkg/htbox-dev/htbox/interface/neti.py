#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : neti.py
class NetInterface(object):

    def __init__(self, jsondict_iface):
        self.jsondict_iface = jsondict_iface

    def get_name(self):
        return ''

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
