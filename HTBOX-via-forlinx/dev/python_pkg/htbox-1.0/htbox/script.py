#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:49 下午
# @Author  : Cooky Long
# @File    : script.py
import os

from htbox.interface.brvpn import BrVpnInterface
from htbox.interface.check_utils import check_main_mode_count
from htbox.interface.eth import EthInterface
from htbox.interface.ppp import PPPInterface
from htbox.interface.wlan import WlanInterface
from htbox.routetable.host import RouteTableHost
from htbox.routetable.net import RouteTableNet
from htbox.shell.job import JobShell
from htbox.shell.net import NetShell


def checkrt(conf):
    rt_hosts = []
    jsondict_rt_hosts = conf['routetable']['host']
    for jsondict_rt_host in jsondict_rt_hosts:
        target = jsondict_rt_host['target']
        gw = jsondict_rt_host['gw']
        iface = jsondict_rt_host['iface']
        if gw == "":
            rt_hosts.append(RouteTableHost(target=target, gw=iface))
        else:
            rt_hosts.append(RouteTableHost(target=target, gw=gw))

    rt_nets = []
    jsondict_rt_nets = conf['routetable']['net']
    for jsondict_rt_net in jsondict_rt_nets:
        target = jsondict_rt_net['target']
        netmask = jsondict_rt_net['netmask']
        gw = jsondict_rt_net['gw']
        iface = jsondict_rt_net['iface']
        if gw == "":
            rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=iface))
        else:
            rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=gw))

    rtn_sys = 0
    for host in rt_hosts:
        if not host.checked:
            rtn_sys = 1
            break
    if rtn_sys == 0:
        for net in rt_nets:
            if not net.checked:
                rtn_sys = 1
                break
    return rtn_sys


def check(conf):
    exit_sys = 1

    eth0 = EthInterface(conf['interface']['eth0'], index=0)
    eth1 = EthInterface(conf['interface']['eth1'], index=1)
    wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
    ppp0 = PPPInterface(conf['interface']['ppp0'], index=0)

    br_vpn = BrVpnInterface(conf['openvpn_iface'], eth0=eth0, eth1=eth1)

    print("检查主出口数量: ", end="")
    if check_main_mode_count(eth0, eth1, wlan0, ppp0) == 0:
        print("OK")

        print("检查eth0配置: ", end="")
        if eth0.check_conf() == 0:
            print("OK")

            print("检查eth1配置: ", end="")
            if eth1.check_conf() == 0:
                print("OK")

                print("检查wlan0配置: ", end="")
                if wlan0.check_conf() == 0:
                    print("OK")

                    print("检查ppp0配置: ", end="")
                    if ppp0.check_conf() == 0:
                        print("OK")

                        print("检查vpn配置: ", end="")
                        if br_vpn.check_conf() == 0:
                            print("OK")

                            print("检查路由表配置: ", end="")
                            if checkrt(conf) == 0:
                                print("OK")
                                exit_sys = 0
    return exit_sys


def config(conf):
    exit_sys = 1

    eth0 = EthInterface(conf['interface']['eth0'], index=0)
    eth1 = EthInterface(conf['interface']['eth1'], index=1)
    wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
    ppp0 = PPPInterface(conf['interface']['ppp0'], index=0)

    br_vpn = BrVpnInterface(conf['openvpn_iface'], eth0=eth0, eth1=eth1)

    if check(conf) == 0:
        exit_sys = 0

        print("执行eth0配置: ", end="")
        eth0.config()
        print("OK")

        print("执行eth1配置: ", end="")
        eth1.config()
        print("OK")

        print("执行wlan0配置: ", end="")
        wlan0.config()
        print("OK")

        print("执行ppp0配置: ", end="")
        ppp0.config()
        print("OK")

        print("执行br-vpn配置: ", end="")
        br_vpn.config()
        print("OK")

    return exit_sys


def start(conf):
    exit_sys = 0

    eth0 = EthInterface(conf['interface']['eth0'], index=0)
    eth1 = EthInterface(conf['interface']['eth1'], index=1)
    wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
    ppp0 = PPPInterface(conf['interface']['ppp0'], index=0)

    if config(conf) == 0:
        print("打开网关: ", end="")
        for iface in [eth0, eth1, wlan0, ppp0]:
            if iface.mode == "gateway":
                iface.start()
                if NetShell.wait_for_iface_up(iface.get_name()) != 0:
                    print(iface.get_name() + ' up ERROR!')
                    # exit_sys = 1
                if iface == eth0 or iface == eth1:
                    os.system(
                        'echo ' + iface.gateway_router + ' > /etc/network/defroute/' + iface.get_name())
                elif iface == wlan0:
                    os.system(
                        'echo ' + iface.ap_router + ' > /etc/network/defroute/' + iface.get_name())
                os.system('route del default')
        print("OK")

        print("打开副出口: ", end="")
        for iface in [eth0, eth1, wlan0, ppp0]:
            if iface.mode == "vice":
                iface.start()
                if NetShell.wait_for_iface_up(iface.get_name()) != 0:
                    print(iface.get_name() + ' up ERROR!')
                    # exit_sys = 1
                if NetShell.wait_for_defroute_up(iface.get_name()) != 0:
                    print(iface.get_name() + ' default route ERROR!')
                    # exit_sys = 1
                else:
                    os.system(
                        'echo ' + NetShell.get_gateway(
                            iface.get_name()) + ' > /etc/network/defroute/' + iface.get_name())
                    os.system('route del default')
        print("OK")

        print("打开主出口: ", end="")
        for iface in [eth0, eth1, wlan0, ppp0]:
            if iface.mode == "main":
                iface.start()
                if NetShell.wait_for_iface_up(iface.get_name()) != 0:
                    print(iface.get_name() + ' up ERROR!')
                    exit_sys = 1
                if NetShell.wait_for_defroute_up(iface.get_name()) != 0:
                    print(iface.get_name() + ' default route ERROR!')
                    exit_sys = 1
                else:
                    os.system(
                        'echo ' + NetShell.get_gateway(
                            iface.get_name()) + ' > /etc/network/defroute/' + iface.get_name())

                print("配置路由转发与iptables: ", end="")
                if conf['ip_forward'] == 1:
                    os.system('echo "net.ipv4.ip_forward = 1" > /etc/sysctl.conf')
                    os.system('sysctl -p')
                    os.system('iptables -t nat -A POSTROUTING -o ' + iface.get_name() + ' -j MASQUERADE')
                else:
                    os.system('echo "net.ipv4.ip_forward = 0" > /etc/sysctl.conf')
                    os.system('sysctl -p')
                print("OK")

                if (iface == eth0 or iface == eth1) and iface.device_inet == 'static':
                    print("配置静态IP地址的DNS: ", end="")
                    if iface.device_dns1 != "":
                        os.system('echo "nameserver ' + iface.device_dns1 + '" > /etc/resolv.conf')
                        if iface.device_dns2 != "":
                            os.system('echo "nameserver ' + iface.device_dns2 + '" >> /etc/resolv.conf')
                elif iface == wlan0 and iface.station_inet == 'static':
                    print("配置静态IP地址的DNS: ", end="")
                    if iface.station_dns1 != "":
                        os.system('echo "nameserver ' + iface.station_dns1 + '" > /etc/resolv.conf')
                        if iface.station_dns2 != "":
                            os.system('echo "nameserver ' + iface.station_dns2 + '" >> /etc/resolv.conf')
                print("OK")

        print("OK")

        rt_hosts = []
        jsondict_rt_hosts = conf['routetable']['host']
        for jsondict_rt_host in jsondict_rt_hosts:
            target = jsondict_rt_host['target']
            gw = jsondict_rt_host['gw']
            iface = jsondict_rt_host['iface']
            if gw == "":
                rt_hosts.append(RouteTableHost(target=target, gw=iface))
            else:
                rt_hosts.append(RouteTableHost(target=target, gw=gw))

        rt_nets = []
        jsondict_rt_nets = conf['routetable']['net']
        for jsondict_rt_net in jsondict_rt_nets:
            target = jsondict_rt_net['target']
            netmask = jsondict_rt_net['netmask']
            gw = jsondict_rt_net['gw']
            iface = jsondict_rt_net['iface']
            if gw == "":
                rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=iface))
            else:
                rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=gw))

        print("配置路由表: ", end="")
        for host in rt_hosts:
            host.add()
        for net in rt_nets:
            net.add()
        print("OK")

    return exit_sys


def stop(conf):
    exit_sys = 0

    eth0 = EthInterface(conf['interface']['eth0'], index=0)
    eth1 = EthInterface(conf['interface']['eth1'], index=1)
    wlan0 = WlanInterface(conf['interface']['wlan0'], index=0)
    ppp0 = PPPInterface(conf['interface']['ppp0'], index=0)

    rt_hosts = []
    jsondict_rt_hosts = conf['routetable']['host']
    for jsondict_rt_host in jsondict_rt_hosts:
        target = jsondict_rt_host['target']
        gw = jsondict_rt_host['gw']
        iface = jsondict_rt_host['iface']
        if gw == "":
            rt_hosts.append(RouteTableHost(target=target, gw=iface))
        else:
            rt_hosts.append(RouteTableHost(target=target, gw=gw))

    rt_nets = []
    jsondict_rt_nets = conf['routetable']['net']
    for jsondict_rt_net in jsondict_rt_nets:
        target = jsondict_rt_net['target']
        netmask = jsondict_rt_net['netmask']
        gw = jsondict_rt_net['gw']
        iface = jsondict_rt_net['iface']
        if gw == "":
            rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=iface))
        else:
            rt_nets.append(RouteTableNet(target=target, netmask=netmask, gw=gw))

    print("删除路由表: ", end="")
    for host in rt_hosts:
        host.delete()
    for net in rt_nets:
        net.delete()
    print("OK")

    print("关闭vpn: ", end="")
    if JobShell.killjob('openvpn') == 0:
        os.system('/usr/local/bin/bridge-stop.sh')
    print("OK")

    print("关闭主出口: ", end="")
    for iface in [eth0, eth1, wlan0, ppp0]:
        if iface.mode == "main":
            print("删除路由转发与iptables: ", end="")
            os.system('echo "net.ipv4.ip_forward = 0" > /etc/sysctl.conf')
            os.system('sysctl -p')
            os.system('iptables -t nat -D POSTROUTING -o ' + iface.get_name() + ' -j MASQUERADE')
            print("OK")
            iface.stop()
    print("OK")

    print("关闭副出口: ", end="")
    for iface in [eth0, eth1, wlan0, ppp0]:
        if iface.mode == "vice":
            iface.stop()
    print("OK")

    print("关闭网关: ", end="")
    for iface in [eth0, eth1, wlan0, ppp0]:
        if iface.mode == "gateway":
            iface.stop()
    print("OK")

    return exit_sys
