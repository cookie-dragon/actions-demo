#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:59 下午
# @Author  : Cooky Long
# @File    : eth.py
import os

from htbox.interface.network import NetworkInterface
from htbox.network_utils import NetworkUtils
from htbox.shell.job import JobShell
from htbox.shell.sed import SedShell


class EthInterface(NetworkInterface):

    def __init__(self, jsondict_iface, index):
        super().__init__(jsondict_iface, 'eth', index)

        self.device_inet = self.jsondict_iface['device']['inet']
        self.device_address = self.jsondict_iface['device']['inet_static']['address']
        self.device_netmask = self.jsondict_iface['device']['inet_static']['netmask']
        self.device_gateway = self.jsondict_iface['device']['inet_static']['gateway']
        self.device_dns1 = self.jsondict_iface['device']['inet_static']['dns_nameserver1']
        self.device_dns2 = self.jsondict_iface['device']['inet_static']['dns_nameserver2']

        self.gateway_subnet = self.jsondict_iface['gateway']['subnet']
        self.gateway_router = self.jsondict_iface['gateway']['router']
        self.gateway_inet = self.jsondict_iface['gateway']['inet']
        self.gateway_dns1 = self.jsondict_iface['gateway']['inet_dhcp']['dns1']
        self.gateway_dns2 = self.jsondict_iface['gateway']['inet_dhcp']['dns2']
        self.gateway_poolstart = self.jsondict_iface['gateway']['inet_dhcp']['start']
        self.gateway_poolend = self.jsondict_iface['gateway']['inet_dhcp']['end']
        self.gateway_poolmaxleases = self.jsondict_iface['gateway']['inet_dhcp']['max_leases']

    def check_conf(self):
        rtn_sys = 1

        if self.mode == "main" or self.mode == "vice":
            if self.device_inet == "static":
                if NetworkUtils.check_interface(gateway=self.device_gateway,
                                                netmask=self.device_netmask,
                                                address=self.device_address) == 0:
                    if self.device_dns1 != "":
                        if NetworkUtils.check_ip(self.device_dns1) == 0:
                            if self.device_dns2 != "":
                                if NetworkUtils.check_ip(self.device_dns2) == 0:
                                    rtn_sys = 0
                            else:
                                rtn_sys = 0
                    else:
                        rtn_sys = 0
            elif self.device_inet == "dhcp":
                rtn_sys = 0
        elif self.mode == "gateway":
            if NetworkUtils.check_interface(gateway=self.gateway_router, netmask=self.gateway_subnet) == 0:
                if self.gateway_inet == "dhcp":
                    if NetworkUtils.check_udhcpd(router=self.gateway_router,
                                                 subnet=self.gateway_subnet,
                                                 start=self.gateway_poolstart,
                                                 end=self.gateway_poolend,
                                                 max_leases=self.gateway_poolmaxleases) == 0:
                        if self.gateway_dns1 != "":
                            if NetworkUtils.check_ip(self.gateway_dns1) == 0:
                                if self.gateway_dns2 != "":
                                    if NetworkUtils.check_ip(self.gateway_dns2) == 0:
                                        rtn_sys = 0
                                else:
                                    rtn_sys = 0
                        else:
                            rtn_sys = 0
                elif self.gateway_inet == "static":
                    rtn_sys = 0
        elif self.mode == "off":
            rtn_sys = 0

        return rtn_sys

    def config(self):
        file_interfaces = '/etc/network/interfaces'

        if self.mode == "main" or self.mode == "vice":
            if self.device_inet == "static":
                SedShell.replace_line(file=file_interfaces,
                                      index=7 + self.index * 10,
                                      text="iface " + self.get_name() + " inet static")
                SedShell.replace_line(file=file_interfaces,
                                      index=11 + self.index * 7,
                                      text="  address " + self.device_address)
                SedShell.replace_line(file=file_interfaces,
                                      index=12 + self.index * 7,
                                      text="  netmask " + self.device_netmask)
                SedShell.replace_line(file=file_interfaces,
                                      index=13 + self.index * 7,
                                      text="  gateway " + self.device_gateway)
                if self.device_dns1 != "":
                    if self.device_dns2 != "":
                        SedShell.replace_line(file=file_interfaces,
                                              index=14 + self.index * 7,
                                              text="  dns-nameservers " + self.device_dns1 + " " + self.device_dns2)
                    else:
                        SedShell.replace_line(file=file_interfaces,
                                              index=14 + self.index * 7,
                                              text="  dns-nameservers " + self.device_dns1)
                else:
                    SedShell.annotate_well(file=file_interfaces, index=14 + self.index * 7)
            elif self.device_inet == "dhcp":
                SedShell.replace_line(file=file_interfaces,
                                      index=7 + self.index * 10,
                                      text="iface " + self.get_name() + " inet dhcp")
                SedShell.annotate_well(file=file_interfaces, index=11 + self.index * 7)
                SedShell.annotate_well(file=file_interfaces, index=12 + self.index * 7)
                SedShell.annotate_well(file=file_interfaces, index=13 + self.index * 7)
                SedShell.annotate_well(file=file_interfaces, index=14 + self.index * 7)
        elif self.mode == "gateway":
            SedShell.replace_line(file=file_interfaces,
                                  index=7 + self.index * 10,
                                  text="iface " + self.get_name() + " inet static")
            SedShell.replace_line(file=file_interfaces,
                                  index=11 + self.index * 7,
                                  text="  address " + self.gateway_router)
            SedShell.replace_line(file=file_interfaces,
                                  index=12 + self.index * 7,
                                  text="  netmask " + self.gateway_subnet)
            SedShell.replace_line(file=file_interfaces,
                                  index=13 + self.index * 7,
                                  text="  gateway " + self.gateway_router)
            SedShell.annotate_well(file=file_interfaces, index=14 + self.index * 7)
            if self.gateway_inet == "dhcp":
                file_udhcpd = '/etc/udhcpd_' + self.get_name() + '.conf'

                SedShell.replace_line(file=file_udhcpd,
                                      index=2,
                                      text="option subnet " + self.gateway_subnet)
                SedShell.replace_line(file=file_udhcpd,
                                      index=3,
                                      text="opt router " + self.gateway_router)
                if self.gateway_dns1 != "":
                    if self.gateway_dns2 != "":
                        SedShell.replace_line(file=file_udhcpd,
                                              index=4,
                                              text="opt dns " + self.gateway_dns1 + " " + self.gateway_dns2)
                    else:
                        SedShell.replace_line(file=file_udhcpd,
                                              index=4,
                                              text="opt dns " + self.gateway_dns1)
                else:
                    SedShell.annotate_well(file=file_udhcpd, index=4)
                SedShell.replace_line(file=file_udhcpd,
                                      index=5,
                                      text="start " + self.gateway_poolstart)
                SedShell.replace_line(file=file_udhcpd,
                                      index=6,
                                      text="end " + self.gateway_poolend)
                SedShell.replace_line(file=file_udhcpd,
                                      index=7,
                                      text="max_leases " + str(self.gateway_poolmaxleases))
            elif self.gateway_inet == "static":
                pass
        elif self.mode == "off":
            SedShell.annotate_well(file=file_interfaces, index=7 + self.index * 10)
            SedShell.annotate_well(file=file_interfaces, index=11 + self.index * 7)
            SedShell.annotate_well(file=file_interfaces, index=12 + self.index * 7)
            SedShell.annotate_well(file=file_interfaces, index=13 + self.index * 7)
            SedShell.annotate_well(file=file_interfaces, index=14 + self.index * 7)

    def start(self):
        if self.mode == "main" or self.mode == "vice":
            os.system('ifup ' + self.get_name())
        elif self.mode == "gateway":
            os.system('ifup ' + self.get_name())
            if self.gateway_inet == "dhcp":
                os.system('/usr/sbin/udhcpd /etc/udhcpd_' + self.get_name() + '.conf > /dev/null &')
            elif self.gateway_inet == "static":
                pass
        elif self.mode == "off":
            pass

    def stop(self):
        if self.mode == "main" or self.mode == "vice":
            os.system('ifdown ' + self.get_name())
            os.system('ifconfig ' + self.get_name() + ' down')
        elif self.mode == "gateway":
            if self.gateway_inet == "dhcp":
                JobShell.killjob('udhcpd /etc/udhcpd_' + self.get_name() + '.conf')
            elif self.gateway_inet == "static":
                pass
            os.system('ifdown ' + self.get_name())
            os.system('ifconfig ' + self.get_name() + ' down')
        elif self.mode == "off":
            pass
