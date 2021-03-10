#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 10:16 上午
# @Author  : Cooky Long
# @File    : main_opc
from Log import initLog

initLog()
from entrance_opc import opc_main

if __name__ == '__main__':
    opc_main()
