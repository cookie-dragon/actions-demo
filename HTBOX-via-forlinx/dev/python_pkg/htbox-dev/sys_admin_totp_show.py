#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
import base64
import os
import pyotp
import pyqrcode
import sys


def get_serial_b32():
    serial_b32 = None

    s_line_s = os.popen("cat /proc/cpuinfo | grep Serial").readlines()
    if len(s_line_s) == 1:
        serial = s_line_s[0].replace('Serial\t\t: ', '').replace('\n', '')
        serial_fix = None
        for loop_i in range(8):
            if 5 * (loop_i + 1) < len(serial):
                continue
            else:
                fixcnt = 5 * (loop_i + 1) - len(serial)
                if fixcnt > 0:
                    serial_fix = serial + str("=").rjust(fixcnt, "=")
                else:
                    serial_fix = serial
                break
        if serial_fix:
            serial_b32 = base64.b32encode(serial_fix.encode(encoding='utf-8')).decode(encoding='utf-8')

    return serial_b32


if __name__ == '__main__':
    exit_sys = 1

    show_name = "htbox-undefined"
    if len(sys.argv) > 1:
        show_name = sys.argv[1]

    serial_b32 = get_serial_b32()
    if serial_b32:
        totp = pyotp.TOTP(serial_b32)
        google_url = totp.provisioning_uri(name=show_name + ' Admin Password', issuer_name='Hilectro')
        print(pyqrcode.create(google_url).terminal(quiet_zone=1))
        print(serial_b32)
