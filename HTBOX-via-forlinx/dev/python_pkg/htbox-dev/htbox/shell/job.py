#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:55 下午
# @Author  : Cooky Long
# @File    : job.py
import os


class JobShell:

    @staticmethod
    def get_pid(text):
        pid = -1
        shell_lines = os.popen("ps -ef | grep \"" + text + "\" | grep -v grep").readlines()
        if len(shell_lines) > 0:
            shell_lines = os.popen("ps -ef | grep \"" + text + "\" | grep -v grep | awk '{print $1}'").readlines()
            if len(shell_lines) == 1:
                pid = shell_lines[0]
        return pid

    @staticmethod
    def killjob(text):
        pid = JobShell.get_pid(text)
        if pid != -1:
            os.system('kill -9 ' + pid)
            return 0
        return 1
