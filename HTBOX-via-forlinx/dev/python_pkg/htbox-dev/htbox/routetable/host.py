#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:02 下午
# @Author  : Cooky Long
# @File    : host.py
import os

from htbox.network_utils import NetworkUtils


class RouteTableHost:
    def __init__(self, target, gw):
        self.checked = self.check(target, gw)

    def check(self, target, gw):
        checked = False
        if NetworkUtils.check_ip(target) == 0:
            self.target = target
            if NetworkUtils.check_ip(gw) == 0:
                self.gw = gw
                checked = True
            else:
                with open('/etc/network/defroute/' + gw, 'r', encoding='utf-8') as f:
                    self.gw = f.readline()
                    checked = True
        return checked

    def add(self):
        if self.checked:
            os.system('route add -host ' + self.target + ' gw ' + self.gw)

    def delete(self):
        if self.checked:
            os.system('route del -host ' + self.target + ' gw ' + self.gw)
