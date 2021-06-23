#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 2:47 下午
# @Author  : Cooky Long
# @File    : defroute_monitor.py
import time

import os
from htbox.config_utils import load_conf
from htbox.interface.eth import EthInterface
from htbox.interface.ppp import PPPInterface
from htbox.interface.wlan import WlanInterface
from htbox.shell.net import NetShell

if __name__ == '__main__':

    while True:
        time.sleep(1)
        conf = load_conf()
        if conf is not None:
            eth0 = EthInterface(conf['interface']['eth0'], index=0)
            eth1 = EthInterface(conf['interface']['eth1'], index=1)
            wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
            ppp0 = PPPInterface(conf['interface']['ppp0'], index=0)

            main_iface_name = ''
            if eth0.mode == "main":
                main_iface_name = eth0.get_name()
            elif eth1.mode == "main":
                main_iface_name = eth1.get_name()
            elif wlan0.mode == "main":
                main_iface_name = wlan0.get_name()
            elif ppp0.mode == "main":
                main_iface_name = ppp0.get_name()

            routes = NetShell.get_routes()
            if not (len(routes) > 0 and routes[0].iface == main_iface_name and routes[0].destination == '0.0.0.0'):
                print("Default Route Missing!!!")
                if main_iface_name == 'ppp0':
                    os.system('route add default ppp0')
                else:
                    with open('/etc/network/defroute/' + main_iface_name, 'r', encoding='utf-8') as f:
                        gw = f.readline()
                        os.system('route add default gw ' + gw)
            else:
                print("Default Route OK!")
