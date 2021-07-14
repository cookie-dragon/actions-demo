#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : sys_admin_totp_chpwd.py
import base64
import os
from pathlib import Path

import pyotp


def get_boxid():
    boxid = "BoxWithNoID"
    fp = "/etc/boxid"
    if Path(fp).is_file():
        s_line_s = os.popen(f"cat {fp}").readlines()
        if len(s_line_s) > 0 and len(s_line_s[0].replace("\n", "")) > 0:
            boxid = s_line_s[0].replace("\n", "")
    return boxid


def get_str_b32(str_input):
    str_b32 = None
    if str_input:
        serial_fix = None
        for loop_i in range(8):
            if 5 * (loop_i + 1) < len(str_input):
                continue
            else:
                fixcnt = 5 * (loop_i + 1) - len(str_input)
                if fixcnt > 0:
                    serial_fix = str_input + str("=").rjust(fixcnt, "=")
                else:
                    serial_fix = str_input
                break
        if serial_fix:
            str_b32 = base64.b32encode(serial_fix.encode(encoding='utf-8')).decode(encoding='utf-8')

    return str_b32


if __name__ == '__main__':
    boxid = get_boxid()
    str_b32 = get_str_b32(boxid)
    if str_b32:
        totp = pyotp.TOTP(str_b32)
        totp_now = totp.now()
        if os.system("echo -e \"" + totp_now + "\\n" + totp_now + "\" | passwd admin >/dev/null") != 0:
            print("User 'admin' password change Failed!")
            os.system("rm -rf /etc/*+")
            if os.system("echo -e \"" + totp_now + "\\n" + totp_now + "\" | passwd admin >/dev/null") != 0:
                print("User 'admin' password change Failed Again, Exit!")
