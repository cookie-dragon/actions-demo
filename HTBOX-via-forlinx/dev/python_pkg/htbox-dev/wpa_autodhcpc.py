#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 2:47 下午
# @Author  : Cooky Long
# @File    : wpa_autodhcpc.py
import os
import sys

from htbox.config_utils import load_conf
from htbox.shell.job import JobShell
from htbox.shell.net import NetShell
from htbox.interface.wlan import WlanInterface

if __name__ == '__main__':
    exit_sys = 1
    if len(sys.argv) > 1:
        ifname = sys.argv[1]
        cmd = sys.argv[2]

        conf = load_conf()
        if conf is not None:
            wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
            if cmd == 'CONNECTED':
                openvpn_pid = -1
                if wlan0.mode == "main":
                    JobShell.killjob('/opt/bin/defroute_monitor')
                    openvpn_pid = JobShell.get_pid('/usr/sbin/openvpn --config')
                    if openvpn_pid != -1:
                        os.system('/opt/bin/box_openvpn stop')
                os.system('udhcpc -i ' + ifname + ' -n')
                if NetShell.wait_for_iface_up(ifname) != 0:
                    print(ifname + ' up ERROR!')
                    exit_sys = 1
                if NetShell.wait_for_defroute_up(ifname) != 0:
                    print(ifname + ' default route ERROR!')
                    exit_sys = 1
                else:
                    os.system('echo ' + NetShell.get_gateway(ifname) + ' > /etc/network/defroute/' + ifname)

                if wlan0.mode == "main":
                    if openvpn_pid != -1:
                        os.system('/opt/bin/box_openvpn start')
                    os.system('/opt/bin/defroute_monitor >/dev/null &')
            elif cmd == 'DISCONNECTED':
                if wlan0.mode == "main":
                    JobShell.killjob('/opt/bin/defroute_monitor')
                JobShell.killjob('udhcpc -i ' + ifname)

    # print("系统Shell返回：" + str(exit_sys))
    sys.exit(exit_sys)
