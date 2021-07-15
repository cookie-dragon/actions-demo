#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 10:16 上午
# @Author  : Cooky Long
# @File    : __init__.py
import crcmod


def getCrcModbusStr(strVal):
    rtn = str(hex(crcmod.predefined.mkCrcFun('CrcModbus')(strVal.encode())))[2:].upper()
    if len(rtn) < 4:
        rtn = '0' * (4 - len(rtn)) + rtn
    return rtn
