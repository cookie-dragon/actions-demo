#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 2:55 下午
# @Author  : Cooky Long
# @File    : net.py
import os
import time


class NetShell:
    class Route:
        def __init__(self, destination, gateway, genmask, flags, metric, ref, use, iface):
            self.destination = destination
            self.gateway = gateway
            self.genmask = genmask
            self.flags = flags
            self.metric = metric
            self.ref = ref
            self.use = use
            self.iface = iface

    @staticmethod
    def get_routes():
        p = os.popen('route -n')
        lines = p.readlines()
        routers = []
        realData = False
        for line in lines:
            line_str_list = line.split()
            if line_str_list[0] == 'Destination':
                realData = True
                continue
            if realData:
                routers.append(NetShell.Route(line_str_list[0], line_str_list[1], line_str_list[2], line_str_list[3],
                                              line_str_list[4], line_str_list[5], line_str_list[6], line_str_list[7]))
        return routers

    @staticmethod
    def get_gateway(ifacename):
        gateway = None

        routes = NetShell.get_routes()
        for router in routes:
            if router.iface == ifacename and router.destination == '0.0.0.0':
                gateway = router.gateway
                break

        return gateway

    @staticmethod
    def wait_for_iface_up(ifacename):
        rtn = 1

        loop = 10
        while loop > 0:
            time.sleep(0.5)
            if len(os.popen('ifconfig | grep ' + ifacename).readlines()) == 1:
                rtn = 0
                break
            else:
                loop -= 1

        return rtn

    @staticmethod
    def wait_for_defroute_up(ifacename):
        rtn = 1

        loop = 10
        while loop > 0:
            time.sleep(0.5)

            if NetShell.get_gateway(ifacename) is not None:
                rtn = 0
                break
            else:
                loop -= 1

        return rtn
