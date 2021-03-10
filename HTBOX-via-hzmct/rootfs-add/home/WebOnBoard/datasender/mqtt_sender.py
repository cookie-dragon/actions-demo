#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/13 10:17 上午
# @Author  : Cooky Long
# @File    : mqtt_sender
import logging

from paho.mqtt.client import Client


class MQTTSender(object):
    def __init__(self, client_id):
        self.client = Client(client_id)
        self.client.reconnect_delay_set()

        self.username = None
        self.password = None
        self.will_topic = None
        self.will_payload = None

        self.l_onstart_msg = None

    def setUserNameAndPassword(self, username, password):
        self.username = username
        self.password = password

    def setWill(self, will_topic, will_payload):
        self.will_topic = will_topic
        self.will_payload = will_payload

    def setMsgOnStart(self, l_msg):
        self.l_onstart_msg = l_msg

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        logging.debug(topic + ': ' + str(payload))

    def connect(self, host, port, keepalive):
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        if self.will_topic and self.will_payload:
            self.client.will_set(self.will_topic, self.will_payload)
        self.client.connect(host, port, keepalive)
        self.client.loop_start()
        if self.l_onstart_msg:
            for msg in self.l_onstart_msg:
                self.publish(msg['topic'], msg['payload'])

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
