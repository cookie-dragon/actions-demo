#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:57 下午
# @Author  : Cooky Long
# @File    : AdminPswBuilder.py
import argparse
import base64
import platform

import pyotp
import pyqrcode


def get_cpuid():
    cpu_id = None
    if platform.system() == "Windows":
        import wmi

        cpu0 = wmi.WMI().Win32_Processor()[0]
        cpu_id = cpu0.ProcessorId
    return cpu_id


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


def do_show(cpuid):
    if cpuid:
        str_b32 = get_str_b32(cpuid)
        if str_b32:
            totp = pyotp.TOTP(str_b32)
            google_url = totp.provisioning_uri(name=cpuid + ' Admin Psw Builder Password', issuer_name='Hilectro')
            code = pyqrcode.create(google_url)
            code.png(cpuid + ".png", scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
            code.show()


def do_auth():
    rtn = False

    cpuid = get_cpuid()
    if cpuid:
        str_b32 = get_str_b32(cpuid)
        if str_b32:
            totp = pyotp.TOTP(str_b32)
            print(f"身份认证（{cpuid}）：")
            totp_input = input()
            rtn = totp.verify(totp_input)
    return rtn


def do_box():
    boxid = "BoxWithNoID"

    while boxid != "exit":
        print("请输入BoxID（输入exit退出程序）：")
        boxid = input()
        if boxid != "exit":
            show_name = boxid
            str_b32 = get_str_b32(boxid)
            if str_b32:
                totp = pyotp.TOTP(str_b32)
                google_url = totp.provisioning_uri(name=show_name + ' Admin Password', issuer_name='Hilectro')
                code = pyqrcode.create(google_url)
                code.png(boxid + ".png", scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
                code.show()
                print("请使用Google Authenticator的APP扫描二维码（Android可使用微软的Authenticator）")
                print("\n========== ********** ========== ********** ========== ********** ==========\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Admin Psw Builder')
    parser.add_argument("--action", type=str, default="build")  # build show
    parser.add_argument("--cpuid", type=str, default=get_cpuid())
    args = parser.parse_args()

    if args.action == "show":
        do_show(args.cpuid)
    else:
        if do_auth():
            do_box()
