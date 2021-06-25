#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:00 下午
# @Author  : Cooky Long
# @File    : ppp.py
import os
from pathlib import Path

from htbox.interface.network import NetworkInterface


class PPPInterface(NetworkInterface):

    def __init__(self, jsondict_iface, index):
        super().__init__(jsondict_iface, 'ppp', index)

        self.devname = self.jsondict_iface['ppp']['devname']
        self.apn = self.jsondict_iface['ppp']['apn']
        self.user = self.jsondict_iface['ppp']['user']
        self.password = self.jsondict_iface['ppp']['password']

    def check_conf(self):
        rtn_sys = 1

        if self.mode == "main":
            if Path(self.devname).exists():
                rtn_sys = 0
        elif self.mode == "off":
            rtn_sys = 0

        return rtn_sys

    def start(self):
        if self.mode == "main":
            os.system(
                '/usr/local/bin/quectel-pppd ' + self.devname + ' ' + self.apn + ' ' + self.user + ' ' + self.password)
        elif self.mode == "off":
            pass

    def stop(self):
        if self.mode == "main":
            os.system('/usr/local/bin/quectel-ppp-kill')
        elif self.mode == "off":
            pass
