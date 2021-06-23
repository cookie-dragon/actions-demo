#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/11 1:00 下午
# @Author  : Cooky Long
# @File    : boxua.py
import logging
import threading

from boxua import boxua_global_v
from boxua.server.bxoua_server import BoxUaServer
from hnpc.hnpc_global_f import trans_nodes_config2dict

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:

        trans_nodes_config2dict()

        boxua_global_v.boxuaserver = BoxUaServer()
        boxua_global_v.boxuaserver.setDaemon(True)
        boxua_global_v.boxuaserver.start()

        condition = threading.Condition()
        condition.acquire()
        condition.wait()
    except Exception as e:
        print(e)
    finally:
        if boxua_global_v.boxuaserver and boxua_global_v.boxuaserver.is_alive():
            boxua_global_v.boxuaserver.stop()
