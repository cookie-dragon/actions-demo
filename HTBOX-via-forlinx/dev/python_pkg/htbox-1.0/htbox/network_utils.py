#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:53 下午
# @Author  : Cooky Long
# @File    : network_utils.py
from IPy import IP


class NetworkUtils(object):

    @staticmethod
    def check_ip(address):
        rtn_sys = 1

        try:
            ip = IP(address)
            version = ip.version()
            if version == 4:  # IPv4
                prefixlen = ip.prefixlen()
                if prefixlen == 32:  # 子网掩码校验
                    rtn_sys = 0
                else:
                    print("ip prefixlen is not in 32. ", end="")
            else:
                print("ip version is not in IPv4. ", end="")
        except Exception as e:
            print("check_ip ERROR: " + address + ' ' + str(type(e)) + " - " + str(e.args) + " ", end="")

        return rtn_sys

    @staticmethod
    def check_interface(gateway, netmask, address=""):
        rtn_sys = 1

        try:
            network = IP(gateway).make_net(netmask)
            if network.version() == 4:  # IPv4
                if network.iptype() == "PRIVATE":  # 私有网络
                    if gateway == str(network.net()):  # 排除网络地址
                        print("gateway is network address. ", end="")
                    elif gateway == str(network.broadcast()):  # 排除广播地址
                        print("gateway is broadcast address. ", end="")
                    elif address != "":  # 检查address
                        if address in network:  # 包含
                            if address == str(network.net()):  # 排除网络地址
                                print("ip is network address. ", end="")
                            elif address == str(network.broadcast()):  # 排除广播地址
                                print("ip is broadcast address. ", end="")
                            else:
                                rtn_sys = 0
                        else:
                            print("ip not in network. ", end="")
                    else:
                        rtn_sys = 0
                else:
                    print("network is not PRIVATE. ", end="")
            else:
                print("network version is not in IPv4. ", end="")
        except Exception as e:
            print("check_interface ERROR: " + str(type(e)) + " - " + str(e.args) + " ", end="")

        return rtn_sys

    @staticmethod
    def check_udhcpd(router, subnet, start, end, max_leases):
        rtn_sys = 1

        try:
            network = IP(router).make_net(subnet)
            if network.version() == 4:  # IPv4
                if network.iptype() == "PRIVATE":  # 私有网络
                    if router == str(network.net()) or start == str(network.net()) or end == str(
                            network.net()):  # 排除网络地址
                        print("routeip or startip or endip is network address. ", end="")
                    elif router == str(network.broadcast()) or start == str(network.broadcast()) or end == str(
                            network.broadcast()):  # 排除广播地址
                        print("routeip or startip or endip is broadcast address. ", end="")
                    else:
                        dec_start = int(IP(start).strDec())
                        dec_end = int(IP(end).strDec())
                        if dec_start <= dec_end:  # 地址池开始/结束地址大小校验
                            if dec_end - dec_start + 1 == max_leases:  # 地址池数量校验
                                if start in network:  # 地址池开始地址包含校验
                                    if end in network:  # 地址池结束地址包含校验
                                        dec_route = int(IP(router).strDec())
                                        if dec_start <= dec_route <= dec_end:  # 网关地址是否在地址池内
                                            print("routeip is in startip and endip. ", end="")
                                        else:
                                            rtn_sys = 0
                                    else:
                                        print("endip not in network. ", end="")
                                else:
                                    print("startip not in network. ", end="")
                            else:
                                print("WRONG max_leases. ", end="")
                        else:
                            print("startip is bigger than endip. ", end="")
                else:
                    print("network is not PRIVATE. ", end="")
            else:
                print("network version is not in IPv4. ", end="")
        except Exception as e:
            print("check_udhcpd ERROR: " + str(type(e)) + " - " + str(e.args) + " ", end="")

        return rtn_sys
