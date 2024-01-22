#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 2:47 下午
# @Author  : Cooky Long
# @File    : defroute_monitor.py
import os
import time
from pathlib import Path

from htbox.config_utils import load_conf
from htbox.interface.eth import EthInterface
from htbox.interface.ppp import PPPInterface
from htbox.interface.wlan import WlanInterface
from htbox.shell.net import NetShell

if __name__ == '__main__':
    f_pid_path = '/var/run/defroute_monitor.pid'
    pid_file = Path(f_pid_path)
    try:
        if pid_file.exists():
            f_pid = open(f_pid_path, 'r')
            pid = f_pid.readline()
            print('Old Pid: ' + str(pid))
            os.system('kill -9 ' + pid)
            print('Old Pid: Killed!')

        pid = os.getpid()
        print('New Pid: ' + str(pid))
        f_pid = open(f_pid_path, 'w')
        f_pid.write(str(pid) + '\n')
        f_pid.close()
        print('New Pid: Protected!')

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
                    while len(routes) > 0 and routes[0].destination == '0.0.0.0' and routes[0].genmask == '0.0.0.0':
                        os.system('route del default')
                        routes = NetShell.get_routes()
                    if main_iface_name == 'ppp0':
                        os.system('route add default ppp0')
                    else:
                        with open('/etc/network/defroute/' + main_iface_name, 'r', encoding='utf-8') as f:
                            gw = f.readline()
                            os.system('route add default gw ' + gw)
                else:
                    print("Default Route OK!")
    finally:
        os.system('rm -rf ' + f_pid_path)
