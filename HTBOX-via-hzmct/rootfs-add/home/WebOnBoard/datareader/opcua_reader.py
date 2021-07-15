#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/12 23:26
# @Author  : Cooky Long
# @File    : opcua
import datetime
import logging
import time

from datareader import DataReaderError
from opcua import Client


class OpcuaReader(object):
    def __init__(self, endPointUrl):
        self.client = Client(endPointUrl)
        self.open()

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.client.disconnect()
        except Exception as e:
            logging.info("OpcuaReader Disconnect Failed: " + str(e))

    def __dovalue(self, value, index, subindex):
        if type(value) == list:
            value = value[index][subindex]
        if type(value) == datetime.datetime:
            try:
                value = int(time.mktime(value.timetuple()))
            except Exception:
                value = 0
        elif type(value) == bool:
            if value:
                value = 1
            else:
                value = 0
        elif type(value) == str:
            if len(value) > 0:
                value = 1
            else:
                value = 0
        return value

    def open(self):
        self.close()

        try:
            self.client.connect()
        except Exception as e:
            raise DataReaderError("OpcuaReader Connect Failed: " + str(e))

    def getData(self, nodeidStr, index, subindex):
        try:
            tag = self.client.get_node(nodeidStr.encode('utf-8'))
            value = self.__dovalue(tag.get_value(), index, subindex)
            return value
        except Exception as e:
            logging.warning("OpcuaReader GetData Failed: " + str(type(e)) + ' \t ' + str(e))
            self.open()
