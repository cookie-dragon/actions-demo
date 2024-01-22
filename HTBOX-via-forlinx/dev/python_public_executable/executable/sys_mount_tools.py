#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
import argparse
import base64
import hashlib
import os
import struct
import sys
from pathlib import Path


def get_serial():
    serial = ""
    s_line_s = os.popen("cat /proc/cpuinfo | grep Serial").readlines()
    if len(s_line_s) == 1:
        serial = s_line_s[0].replace('Serial\t\t: ', '').replace('\n', '')
    return serial


def get_boxid():
    boxid = "BoxWithNoID"
    fp = "/etc/boxid"
    if Path(fp).is_file():
        s_line_s = os.popen(f"cat {fp}").readlines()
        if len(s_line_s) > 0 and len(s_line_s[0].replace("\n", "")) > 0:
            boxid = s_line_s[0].replace("\n", "")
    return boxid


def get_cid():
    cid = "CardWithNoID"
    fp = "/sys/class/mmc_host/mmc0/mmc0:0001/cid"
    if Path(fp).is_file():
        s_line_s = os.popen(f"cat {fp}").readlines()
        if len(s_line_s) > 0 and len(s_line_s[0].replace("\n", "")) > 0:
            cid = s_line_s[0].replace("\n", "")
    return cid


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


def get_str_md5(str_input):
    fac_md5 = hashlib.md5()
    fac_md5.update(str_input.encode(encoding='utf8'))
    return fac_md5.hexdigest()


def get_str_sha1(str_input):
    return hashlib.sha1(str_input.encode(encoding='utf-8')).hexdigest()


def get_str_sha256(str_input):
    return hashlib.sha256(str_input.encode(encoding='utf-8')).hexdigest()


def get_three_sha256(serial, cid, boxid):
    serial_md5_sha256 = get_str_sha256(get_str_md5(serial))
    cid_sha1_sha256 = get_str_sha256(get_str_sha1(cid))
    boxid_b32_sha256 = get_str_sha256(get_str_b32(boxid))
    sha256_sha256 = get_str_sha256(serial_md5_sha256 + cid_sha1_sha256 + boxid_b32_sha256)
    return serial_md5_sha256, cid_sha1_sha256, boxid_b32_sha256, sha256_sha256


def build_bin_list(bin_list, str_input, offset):
    str_char_list = list(str_input)
    for i in range(len(str_char_list)):
        bin_list[offset + i] = ord(str_char_list[i])


def write_block(three_sha256):
    byt_b = 0xff
    byt_w = 0x00

    bin_list = [byt_w] * 64 + [byt_b] * 256 \
               + [byt_b] * 16 \
               + ([byt_w] * 2 + [byt_b] * 4 + [byt_w] * 10) * 2 \
               + ([byt_w] * 2 + [byt_b] * 4 + [byt_w] * 2 + [byt_b] * 2 + [byt_w] * 4 + [byt_b] * 2) * 2 \
               + ([byt_w] * 8 + [byt_b] * 2 + [byt_w] * 4 + [byt_b] * 2) * 2 \
               + ([byt_w] * 2 + [byt_b] * 4 + [byt_w] * 2 + [byt_b] * 2 + [byt_w] * 4 + [byt_b] * 2) * 4 \
               + [byt_b] * 16
    build_bin_list(bin_list, three_sha256[0], 64)
    build_bin_list(bin_list, three_sha256[1], 128)
    build_bin_list(bin_list, three_sha256[2], 192)
    build_bin_list(bin_list, three_sha256[3], 256)

    fpath = "/tmp/block"
    with open(fpath, 'wb') as fp:
        for i in range(len(bin_list)):
            s = struct.pack('B', bin_list[i])
            fp.write(s)

    r = 1
    if Path("/dev/mmcblk0").exists():
        r = os.system("dd if=/tmp/block of=/dev/mmcblk0 seek=1 bs=512 count=1")
    return r


def read_block():
    r_serial_md5_sha256 = None
    r_cid_sha1_sha256 = None
    r_boxid_b32_sha256 = None
    r_sha256_sha256 = None

    r = 1
    if Path("/dev/mmcblk0").exists():
        r = os.system("dd if=/dev/mmcblk0 of=/tmp/block skip=1 bs=512 count=1")
    if r == 0:
        fpath = "/tmp/block"
        with open(fpath, 'rb') as fp:
            b_0 = fp.read(64)
            r_serial_md5_sha256 = fp.read(64).decode(encoding='utf-8')
            r_cid_sha1_sha256 = fp.read(64).decode(encoding='utf-8')
            r_boxid_b32_sha256 = fp.read(64).decode(encoding='utf-8')
            r_sha256_sha256 = fp.read(64).decode(encoding='utf-8')
            b_f_0 = fp.read(16)
            b_ht = fp.read(160)
            b_f_1 = fp.read(16)
    return r_serial_md5_sha256, r_cid_sha1_sha256, r_boxid_b32_sha256, r_sha256_sha256


def check_block(three_sha256, r_three_sha256):
    return True if three_sha256[0] == r_three_sha256[0] else False, \
           True if three_sha256[1] == r_three_sha256[1] else False, \
           True if three_sha256[2] == r_three_sha256[2] else False, \
           True if r_three_sha256[3] == get_str_sha256(
               r_three_sha256[0] + r_three_sha256[1] + r_three_sha256[2]) else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mount Tools')
    parser.add_argument("--action", type=str, default="check")  # build super check
    parser.add_argument("--serial", type=str, default="")
    parser.add_argument("--cid", type=str, default="CardWithNoID")
    parser.add_argument("--boxid", type=str, default="BoxWithNoID")
    parser.add_argument("--auth", type=int,
                        default=2)  # 0:No Auth;1:Check Card Only;2:Check BOXID;3:Check Serial;4:Check All
    args = parser.parse_args()

    exit_sys = 1
    super_three_sha256 = get_three_sha256("", "CardWithNoID", "BoxWithNoID")
    if args.action == "build":
        set_three_sha256 = get_three_sha256(get_serial() if args.serial == "" else args.serial,
                                            get_cid() if args.cid == "CardWithNoID" else args.cid,
                                            get_boxid() if args.boxid == "BoxWithNoID" else args.boxid)
        exit_sys = write_block(set_three_sha256)
    elif args.action == "super":
        exit_sys = write_block(super_three_sha256)
    elif args.action == "check":
        r_three_sha256 = read_block()
        if r_three_sha256[3] == super_three_sha256[3]:
            exit_sys = 0
        elif args.auth == 0:
            exit_sys = 0
        else:
            rst = check_block(get_three_sha256(get_serial(), get_cid(), get_boxid()), r_three_sha256)
            if rst[3]:
                if args.auth == 1 and rst[1]:
                    exit_sys = 0
                elif args.auth == 2 and (rst[1] and rst[2]):
                    exit_sys = 0
                elif args.auth == 3 and (rst[1] and rst[0]):
                    exit_sys = 0
                elif args.auth == 4 and (rst[1] and rst[2] and rst[0]):
                    exit_sys = 0

    sys.exit(exit_sys)
