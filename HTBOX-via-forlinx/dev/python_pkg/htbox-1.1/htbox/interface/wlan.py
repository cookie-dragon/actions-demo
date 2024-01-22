#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:00 下午
# @Author  : Cooky Long
# @File    : wlan.py
import os

from htbox.interface.network import NetworkInterface
from htbox.network_utils import NetworkUtils
from htbox.shell.job import JobShell
from htbox.shell.sed import SedShell


class WlanInterface(NetworkInterface):

    def __init__(self, jsondict_iface, index):
        super().__init__(jsondict_iface, 'wlan', index)

        self.station_ssid = self.jsondict_iface['station']['ssid']
        self.station_psk = self.jsondict_iface['station']['psk']

        self.station_inet = self.jsondict_iface['station']['inet']
        self.station_address = self.jsondict_iface['station']['inet_static']['address']
        self.station_netmask = self.jsondict_iface['station']['inet_static']['netmask']
        self.station_gateway = self.jsondict_iface['station']['inet_static']['gateway']
        self.station_dns1 = self.jsondict_iface['station']['inet_static']['dns_nameserver1']
        self.station_dns2 = self.jsondict_iface['station']['inet_static']['dns_nameserver2']

        self.ap_ssid = self.jsondict_iface['ap']['ssid']
        self.ap_wpa_passphrase = self.jsondict_iface['ap']['wpa_passphrase']

        self.ap_subnet = self.jsondict_iface['ap']['subnet']
        self.ap_router = self.jsondict_iface['ap']['router']
        self.ap_inet = self.jsondict_iface['ap']['inet']
        self.ap_dns1 = self.jsondict_iface['ap']['inet_dhcp']['dns1']
        self.ap_dns2 = self.jsondict_iface['ap']['inet_dhcp']['dns2']
        self.ap_poolstart = self.jsondict_iface['ap']['inet_dhcp']['start']
        self.ap_poolend = self.jsondict_iface['ap']['inet_dhcp']['end']
        self.ap_poolmaxleases = self.jsondict_iface['ap']['inet_dhcp']['max_leases']

    def check_conf(self):
        rtn_sys = 1

        if self.mode == "main" or self.mode == "vice":
            if self.station_inet == "static":
                if NetworkUtils.check_interface(gateway=self.station_gateway,
                                                netmask=self.station_netmask,
                                                address=self.station_address) == 0:
                    if self.station_dns1 != "":
                        if NetworkUtils.check_ip(self.station_dns1) == 0:
                            if self.station_dns2 != "":
                                if NetworkUtils.check_ip(self.station_dns2) == 0:
                                    rtn_sys = 0
                            else:
                                rtn_sys = 0
                    else:
                        rtn_sys = 0
            elif self.station_inet == "dhcp":
                rtn_sys = 0
        elif self.mode == "gateway":
            if NetworkUtils.check_interface(gateway=self.ap_router, netmask=self.ap_subnet) == 0:
                if self.ap_inet == "dhcp":
                    if NetworkUtils.check_udhcpd(router=self.ap_router,
                                                 subnet=self.ap_subnet,
                                                 start=self.ap_poolstart,
                                                 end=self.ap_poolend,
                                                 max_leases=self.ap_poolmaxleases) == 0:
                        if self.ap_dns1 != "":
                            if NetworkUtils.check_ip(self.ap_dns1) == 0:
                                if self.ap_dns2 != "":
                                    if NetworkUtils.check_ip(self.ap_dns2) == 0:
                                        rtn_sys = 0
                                else:
                                    rtn_sys = 0
                        else:
                            rtn_sys = 0
                elif self.ap_inet == "static":
                    rtn_sys = 0
        elif self.mode == "off":
            rtn_sys = 0

        return rtn_sys

    def config(self):
        file_interfaces = '/etc/network/interfaces'

        if self.mode == "main" or self.mode == "vice":
            if self.station_psk != "":
                os.system(
                    '/usr/local/sbin/wpa_passphrase "' + self.station_ssid + '" "' + self.station_psk + '" > /etc/wpa_supplicant.conf')
            else:
                os.system(
                    '/usr/local/sbin/wpa_passphrase "' + self.station_ssid + '" "password" > /etc/wpa_supplicant.conf')
                os.system('sed -i "4c key_mgmt=NONE" /etc/wpa_supplicant.conf')
                os.system("sync")
            if self.station_inet == "static":
                SedShell.replace_line(file=file_interfaces,
                                      index=25,
                                      text="iface " + self.get_name() + " inet static")
                SedShell.annotate_well(file=file_interfaces, index=26)
                SedShell.replace_line(file=file_interfaces,
                                      index=27,
                                      text="  address " + self.station_address)
                SedShell.replace_line(file=file_interfaces,
                                      index=28,
                                      text="  netmask " + self.station_netmask)
                SedShell.replace_line(file=file_interfaces,
                                      index=29,
                                      text="  gateway " + self.station_gateway)
                if self.station_dns1 != "":
                    if self.station_dns2 != "":
                        SedShell.replace_line(file=file_interfaces,
                                              index=30,
                                              text="  dns-nameservers " + self.station_dns1 + " " + self.station_dns2)
                    else:
                        SedShell.replace_line(file=file_interfaces,
                                              index=30,
                                              text="  dns-nameservers " + self.station_dns1)
                else:
                    SedShell.annotate_well(file=file_interfaces, index=29)
            elif self.station_inet == "dhcp":
                SedShell.replace_line(file=file_interfaces,
                                      index=25,
                                      text="iface " + self.get_name() + " inet dhcp")
                SedShell.replace_line(file=file_interfaces,
                                      index=26,
                                      text="  udhcpc_opts -t 10")
                SedShell.annotate_well(file=file_interfaces, index=27)
                SedShell.annotate_well(file=file_interfaces, index=28)
                SedShell.annotate_well(file=file_interfaces, index=29)
                SedShell.annotate_well(file=file_interfaces, index=30)
        elif self.mode == "gateway":
            SedShell.replace_line(file=file_interfaces,
                                  index=25,
                                  text="iface " + self.get_name() + " inet manual")
            SedShell.annotate_well(file=file_interfaces, index=26)
            SedShell.annotate_well(file=file_interfaces, index=27)
            SedShell.annotate_well(file=file_interfaces, index=28)
            SedShell.annotate_well(file=file_interfaces, index=29)

            file_hostapd = '/etc/hostapd_' + self.get_name() + '.conf'

            SedShell.replace_line(file=file_hostapd,
                                  index=5,
                                  text="ssid=" + self.ap_ssid)
            SedShell.replace_line(file=file_hostapd,
                                  index=8,
                                  text="wpa_passphrase=" + self.ap_wpa_passphrase)

            if self.ap_inet == "dhcp":
                file_udhcpd = '/etc/udhcpd_' + self.get_name() + '.conf'

                SedShell.replace_line(file=file_udhcpd,
                                      index=2,
                                      text="option subnet " + self.ap_subnet)
                SedShell.replace_line(file=file_udhcpd,
                                      index=3,
                                      text="opt router " + self.ap_router)
                if self.ap_dns1 != "":
                    if self.ap_dns2 != "":
                        SedShell.replace_line(file=file_udhcpd,
                                              index=4,
                                              text="opt dns " + self.ap_dns1 + " " + self.ap_dns2)
                    else:
                        SedShell.replace_line(file=file_udhcpd,
                                              index=4,
                                              text="opt dns " + self.ap_dns1)
                else:
                    SedShell.annotate_well(file=file_udhcpd, index=4)
                SedShell.replace_line(file=file_udhcpd,
                                      index=5,
                                      text="start " + self.ap_poolstart)
                SedShell.replace_line(file=file_udhcpd,
                                      index=6,
                                      text="end " + self.ap_poolend)
                SedShell.replace_line(file=file_udhcpd,
                                      index=7,
                                      text="max_leases " + str(self.ap_poolmaxleases))
            elif self.ap_inet == "static":
                pass
        elif self.mode == "off":
            pass

    def start(self):
        if self.mode == "main" or self.mode == "vice":
            os.system("/usr/local/sbin/wpa_supplicant -B -Dwext -i" + self.get_name() + " -c/etc/wpa_supplicant.conf")
            os.system('ifup ' + self.get_name())
        elif self.mode == "gateway":
            os.system('ifconfig ' + self.get_name() + ' up ' + self.ap_router)
            os.system('/usr/local/bin/hostapd /etc/hostapd_' + self.get_name() + '.conf -B')
            if self.ap_inet == "dhcp":
                os.system('/usr/sbin/udhcpd /etc/udhcpd_' + self.get_name() + '.conf > /dev/null &')
            elif self.ap_inet == "static":
                pass
        elif self.mode == "off":
            pass

    def stop(self):
        if self.mode == "main" or self.mode == "vice":
            JobShell.killjob('/usr/local/sbin/wpa_supplicant')
            os.system('ifdown ' + self.get_name())
            os.system('ifconfig ' + self.get_name() + ' down')
        elif self.mode == "gateway":
            if self.ap_inet == "dhcp":
                JobShell.killjob('udhcpd /etc/udhcpd_' + self.get_name() + '.conf')
            elif self.ap_inet == "static":
                pass
            JobShell.killjob('hostapd /etc/hostapd_' + self.get_name() + '.conf')
            os.system('ifconfig ' + self.get_name() + ' down')
        elif self.mode == "off":
            pass
