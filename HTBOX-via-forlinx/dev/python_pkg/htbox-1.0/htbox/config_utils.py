#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : config_utils.py
import json
from json import JSONDecodeError


def load_conf(file_conf='/etc/htbox/htbox.conf'):
    conf = None
    print("打开配置文件: ", end="")
    try:
        with open(file_conf, 'r', encoding='utf8')as fp:
            print("OK")

            print("载入配置文件: ", end="")
            conf = json.load(fp)
            print("OK")
    except FileNotFoundError as fnfe:
        print(fnfe.strerror)
    except JSONDecodeError as jde:
        print(jde.msg)
    return conf
