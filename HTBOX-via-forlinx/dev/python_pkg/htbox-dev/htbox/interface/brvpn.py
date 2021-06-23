#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : brvpn.py
from IPy import IP

from htbox.interface.neti import NetInterface
from htbox.shell.sed import SedShell


class BrVpnInterface(NetInterface):

    def __init__(self, jsondict_iface, eth0, eth1):
        super().__init__(jsondict_iface)
        self.eth0 = eth0
        self.eth1 = eth1

    def get_name(self):
        return 'br-vpn'

    def check_conf(self):
        rtn_sys = 1

        tmp_iface = None
        if self.jsondict_iface == "eth0":
            tmp_iface = self.eth0
        elif self.jsondict_iface == "eth1":
            tmp_iface = self.eth1
        if tmp_iface \
                and (((tmp_iface.mode == "main" or tmp_iface.mode == "vice") \
                      and tmp_iface.device_inet == "static") \
                     or tmp_iface.mode == "gateway"):
            rtn_sys = 0
        elif not tmp_iface:
            rtn_sys = 0

        return rtn_sys

    def config(self):
        rtn_sys = 1

        SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                              index=9,
                              text='br="' + self.get_name() + '"')
        SedShell.replace_line(file="/usr/local/bin/bridge-stop.sh",
                              index=8,
                              text='br="' + self.get_name() + '"')

        tmp_iface = None
        if self.jsondict_iface == "eth0":
            tmp_iface = self.eth0
        elif self.jsondict_iface == "eth1":
            tmp_iface = self.eth1
        if tmp_iface:
            SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                  index=17,
                                  text='eth="' + tmp_iface.get_name() + '"')
            SedShell.replace_line(file="/usr/local/bin/bridge-stop.sh",
                                  index=15,
                                  text='eth="' + tmp_iface.get_name() + '"')
            if (tmp_iface.mode == "main" or tmp_iface.mode == "vice") and tmp_iface.device_inet == "static":
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=18,
                                      text='eth_ip="' + tmp_iface.device_address + '"')
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=19,
                                      text='eth_netmask="' + tmp_iface.device_netmask + '"')
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=20,
                                      text='eth_broadcast="' + str(IP(tmp_iface.device_gateway).make_net(
                                          tmp_iface.device_netmask).broadcast()) + '"')
            elif tmp_iface.mode == "gateway":
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=18,
                                      text='eth_ip="' + tmp_iface.gateway_router + '"')
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=19,
                                      text='eth_netmask="' + tmp_iface.gateway_subnet + '"')
                SedShell.replace_line(file="/usr/local/bin/bridge-start.sh",
                                      index=20,
                                      text='eth_broadcast="' + str(IP(tmp_iface.gateway_router).make_net(
                                          tmp_iface.gateway_subnet).broadcast()) + '"')

        return rtn_sys
