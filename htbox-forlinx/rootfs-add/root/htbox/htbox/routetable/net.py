#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:02 下午
# @Author  : Cooky Long
# @File    : net.py
import os

from htbox.network_utils import NetworkUtils


class RouteTableNet:
    def __init__(self, target, netmask, gw):
        if NetworkUtils.check_ip(target) == 0:
            self.target = target
            if NetworkUtils.check_ip(netmask) == 0:
                self.netmask = netmask
                if NetworkUtils.check_ip(gw) == 0:
                    self.gw = gw
                else:
                    with open('/etc/network/defroute/' + gw, 'r', encoding='utf-8') as f:
                        self.gw = f.readline()

    def add(self):
        os.system('route add -net ' + self.target + ' netmask ' + self.netmask + ' gw ' + self.gw)

    def delete(self):
        os.system('route del -net ' + self.target + ' netmask ' + self.netmask + ' gw ' + self.gw)
