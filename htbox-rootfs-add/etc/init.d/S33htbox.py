#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 2:47 下午
# @Author  : Cooky Long
# @File    : S33htbox.py
import os
import sys

from htbox import load_conf
from htbox.script import check, config, start, stop
from htbox.shell.job import JobShell
from pathlib import Path


def check_new():
    print("检查新配置: ", end="")
    tmp_conf_path = "/etc/htbox/htbox.conf.tmp"
    if Path(tmp_conf_path).exists():
        if check(load_conf(tmp_conf_path)) == 0:
            os.system('mv /etc/htbox/htbox.conf.tmp /etc/htbox/htbox.conf')
    print("OK")


if __name__ == '__main__':
    exit_sys = 1

    if len(sys.argv) > 1:
        cmd_shell = sys.argv[1]
        conf = load_conf()
        if conf is not None:
            if cmd_shell == 'check':
                if len(sys.argv) > 2:
                    conf = load_conf(sys.argv[2])
                exit_sys = check(conf)
            elif cmd_shell == 'config':
                exit_sys = config(conf)
            elif cmd_shell == 'start':
                exit_sys = start(conf)
                print("开启默认路由监控: ", end="")
                os.system('/usr/local/bin/defroute_monitor.py >/dev/null &')
                print("OK")
            elif cmd_shell == 'stop':
                print("关闭默认路由监控: ", end="")
                JobShell.killjob('/usr/local/bin/defroute_monitor.py')
                print("OK")
                exit_sys = stop(conf)
                if exit_sys == 0:
                    check_new()
            elif cmd_shell == 'restart' or 'reload':
                exit_sys = stop(conf)
                if exit_sys == 0:
                    check_new()
                    conf = load_conf()
                    exit_sys = start(conf)
            else:
                print('Usage: ' + sys.argv[0] + ' {start|stop|restart}')
    else:
        print('Usage: ' + sys.argv[0] + ' {start|stop|restart}')

    # print("系统Shell返回：" + str(exit_sys))
    sys.exit(exit_sys)
