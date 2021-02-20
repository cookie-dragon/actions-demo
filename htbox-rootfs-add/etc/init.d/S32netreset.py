#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 1:17 下午
# @Author  : Cooky Long
# @File    : S32netreset.py
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    exit_sys = 1

    if len(sys.argv) > 1:
        cmd_shell = sys.argv[1]
        if cmd_shell == 'start':
            if not Path("/etc/htbox/htbox.conf").exists():
                print("网络初始化: ", end="")
                os.system('cp -f /etc/htbox/htbox.conf.def /etc/htbox/htbox.conf')
                print("OK")
        else:
            print('Usage: ' + sys.argv[0] + ' {start}')
    else:
        print('Usage: ' + sys.argv[0] + ' {start}')

    # print("系统Shell返回：" + str(exit_sys))
    sys.exit(exit_sys)
