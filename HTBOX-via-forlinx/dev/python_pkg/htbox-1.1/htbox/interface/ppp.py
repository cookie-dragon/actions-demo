#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 3:00 下午
# @Author  : Cooky Long
# @File    : ppp.py
import os
import time
from pathlib import Path

import serial

from htbox.interface.network import NetworkInterface


class PPPInterface(NetworkInterface):

    def __init__(self, jsondict_iface, index):
        super().__init__(jsondict_iface, 'ppp', index)

        self.devname = self.jsondict_iface['ppp']['devname']
        self.apn = self.jsondict_iface['ppp']['apn']
        self.user = self.jsondict_iface['ppp']['user']
        self.password = self.jsondict_iface['ppp']['password']

        try:  # 兼容老的配置文件（老的配置文件没有这个选项）
            self.at_dev = self.jsondict_iface['at']['devname']
        except Exception as e:
            self.at_dev = None

    def __check_module_ready(self):
        if self.at_dev is not None:
            rst = False
            try_cnt = 15
            ser = None
            try:

                dev_exist = False
                for i in range(try_cnt):
                    print("Check PPP Dev: " + str(i))
                    if Path(self.at_dev).exists():
                        dev_exist = True
                        print("Check PPP Dev PASS!")
                        break
                    time.sleep(1)

                if dev_exist:
                    ser = serial.Serial(self.at_dev, 9600, timeout=1)
                    for i in range(try_cnt):
                        print("Check Module Registered: " + str(i))
                        ser.write("AT+CEREG?\r\n".encode("utf8"))
                        b_lines = ser.readlines()

                        registered = False
                        for b_line in b_lines:
                            s_line = b_line.decode("utf8")
                            if "+CEREG: 0,1" in s_line or "+CEREG: 1,1" in s_line or "+CEREG: 2,1" in s_line:
                                registered = True
                                print("Check Module Registered PASS!")
                                break

                        if registered:
                            rst = True
                            break
            finally:
                if ser is not None:
                    try:
                        ser.close()
                    except Exception as e:
                        pass
        else:
            # 兼容老的配置文件（老的配置文件没有这个选项）
            rst = True
        return rst

    def check_conf(self):
        rtn_sys = 1

        if self.mode == "main":
            if Path(self.devname).exists():
                rtn_sys = 0
        elif self.mode == "off":
            rtn_sys = 0

        return rtn_sys

    def start(self):
        if self.mode == "main":
            if self.__check_module_ready():
                os.system(
                    '/usr/local/bin/quectel-pppd ' + self.devname + ' ' + self.apn + ' ' + self.user + ' ' + self.password)
        elif self.mode == "off":
            pass

    def stop(self):
        if self.mode == "main":
            os.system('/usr/local/bin/quectel-ppp-kill')
        elif self.mode == "off":
            pass
