#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/13 0:00
# @Author  : Cooky Long
# @File    : plat_device
import json
import logging
import time

import crcmod
from apscheduler.schedulers.background import BackgroundScheduler

from datasender import getCrcModbusStr
from datasender.mqtt_sender import MQTTSender


class PlatDevice(object):
    def __init__(self, dtuId, name):
        self.dtuId = dtuId
        self.name = name

        self.devices = list()
        self.report_cycle = 1000
        self.collect_cycle = 1000

        self.remote_scheduler = BackgroundScheduler(timezone='UTC')
        self.local_scheduler = BackgroundScheduler(timezone='UTC')

        self.remote_sender = None
        self.local_sender = None
        self.d_sender_args = dict()

        self.hasPublishOnlineMsg_local = False
        self.hasPublishOnlineMsg_remote = False

    @staticmethod
    def getCrcModbusStr(strVal):
        rtn = str(hex(crcmod.predefined.mkCrcFun('CrcModbus')(strVal.encode())))[2:].upper()
        if len(rtn) < 4:
            rtn = '0' * (4 - len(rtn)) + rtn
        return rtn

    def addDevice(self, device):
        if len(self.devices) > 0 and device.report_cycle != self.devices[0].report_cycle:
            raise Exception('PlatDevice with diff report_cycle')
        self.devices.append(device)
        self.report_cycle = self.devices[0].report_cycle
        if self.report_cycle < 1000:
            self.report_cycle = 1000
        self.collect_cycle = self.devices[0].collect_cycle
        if self.collect_cycle < 1000:
            self.collect_cycle = 1000

    def setSender(self, remote_sender, local_sender, d_sender_args):
        self.remote_sender = remote_sender
        self.local_sender = local_sender
        self.d_sender_args = d_sender_args

    def getMsgPayload(self):
        msg_payload = []
        msg_template = {
            'deviceId': self.name,
            'timestamp': int(time.time())
        }

        for device in self.devices:
            msg = device.getMsg()
            for k, v in msg_template.items():
                msg[k] = v
            msg_payload.append(msg)

        return msg_payload

    def remote_job(self):
        try:
            send_payload = self.getMsgPayload()
            send_payload_str = json.dumps(send_payload)
            send_payload_str_send = send_payload_str + PlatDevice.getCrcModbusStr(send_payload_str)

            # 第一次数据，上报设备上线信息
            if not self.hasPublishOnlineMsg_remote:
                # 设备上线信息
                online_dev_payload = []
                online_dev_payload.append({'deviceId': self.name})
                online_dev_payload_str = json.dumps(online_dev_payload)
                online_dev_payload_str_send = online_dev_payload_str + getCrcModbusStr(online_dev_payload_str)
                d_online_dev = {'topic': 'productKey/receive/' + self.dtuId + '/deviceOn',
                                'payload': online_dev_payload_str_send}
                self.remote_sender.publish(d_online_dev['topic'], d_online_dev['payload'])
                self.hasPublishOnlineMsg_remote = True

            if isinstance(self.remote_sender, MQTTSender):
                self.remote_sender.publish(topic='productKey/receive/' + self.d_sender_args['dtuId'] + '/report',
                                           payload=send_payload_str_send)
            else:
                print(send_payload_str_send)
        except Exception as e:
            logging.warning(str(e))

    def local_job(self):
        try:
            send_payload = self.getMsgPayload()
            send_payload_str = json.dumps(send_payload)
            send_payload_str_send = send_payload_str + PlatDevice.getCrcModbusStr(send_payload_str)

            # 第一次数据，上报设备上线信息
            if not self.hasPublishOnlineMsg_local:
                # 设备上线信息
                online_dev_payload = []
                online_dev_payload.append({'deviceId': self.name})
                online_dev_payload_str = json.dumps(online_dev_payload)
                online_dev_payload_str_send = online_dev_payload_str + getCrcModbusStr(online_dev_payload_str)
                d_online_dev = {'topic': 'productKey/receive/' + self.dtuId + '/deviceOn',
                                'payload': online_dev_payload_str_send}
                self.local_sender.publish(d_online_dev['topic'], d_online_dev['payload'])
                self.hasPublishOnlineMsg_local = True

            if isinstance(self.local_sender, MQTTSender):
                self.local_sender.publish(topic='productKey/receive/' + self.d_sender_args['dtuId'] + '/report',
                                          payload=send_payload_str_send)
        except Exception as e:
            logging.warning(str(e))

    def startJob(self):
        self.local_scheduler.add_job(self.local_job, 'interval', seconds=int(self.collect_cycle / 1000))
        self.remote_scheduler.add_job(self.remote_job, 'interval', seconds=int(self.report_cycle / 1000))
        self.local_scheduler.start()
        self.remote_scheduler.start()
