#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 9:59 上午
# @Author  : Cooky Long
# @File    : __init__
import logging

# TODO: 正式环境改为False
debug = True


def initLog():
    logging.getLogger("apscheduler").setLevel(logging.ERROR)
    logging.getLogger("opcua").setLevel(logging.WARNING)

    if debug:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s \t %(levelname)s \t %(name)s \t %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S"
                            )
    else:
        logging.basicConfig(level=logging.WARNING,
                            format="%(asctime)s \t %(levelname)s \t %(name)s \t %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename='Log/pylog.log', filemode='a',
                            )
