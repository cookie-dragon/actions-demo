#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:54 下午
# @Author  : Cooky Long
# @File    : sed.py
import os


class SedShell:

    @staticmethod
    def get_line(file, index):
        line = ""
        lines = os.popen("sed -n '" + str(index) + "p' " + file).readlines()
        if len(lines) == 1:
            line = lines[0]
        return line

    @staticmethod
    def replace_line(file, index, text):
        os.system("sed -i '" + str(index) + "c " + text + "' " + file)
        os.system("sync")

    @staticmethod
    def annotate_well(file, index):
        line = SedShell.get_line(file, index)
        if not line.startswith('#'):
            SedShell.replace_line(file, index, '# ' + line)
