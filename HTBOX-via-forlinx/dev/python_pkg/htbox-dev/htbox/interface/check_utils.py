#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : check_utils.py
def check_main_mode_count(*args):
    rtn_sys = 1

    main_mode_cnt = 0
    for iface in args:
        if iface.mode == "main":
            main_mode_cnt += 1
    if main_mode_cnt == 1:
        rtn_sys = 0

    return rtn_sys
