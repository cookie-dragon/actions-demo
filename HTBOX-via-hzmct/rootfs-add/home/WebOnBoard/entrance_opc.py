#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/6/30 10:00 上午
# @Author  : Cooky Long
# @File    : entrance_opc
import json
import logging
import threading

from serial import Serial, SerialException

from datasender import getCrcModbusStr
from datasender.mqtt_sender import MQTTSender
from entity.plat_device import PlatDevice
from nodes.device import Device
from nodes.product import Product
from nodes.var_ex import VarEx


def getICCID():
    global serial
    at_bsn = 'AT{}'.format('+QCCID')
    cmd_at = at_bsn.encode('utf-8') + b'\r\n'

    iccid = ''
    try:
        serial = Serial(port='/dev/ttyUSB2', timeout=1)
        serial.write(cmd_at)

        serial.inWaiting()
        l_result = serial.readlines(serial.inWaiting())

        for line in l_result:
            if line.startswith('+QCCID'):
                iccid = line.replace('+QCCID:', '').replace(' ', '').replace('\r', '').replace('\n', '')
                break
    except SerialException:
        pass
    finally:
        try:
            serial.close()
        except NameError:
            pass

    return iccid


def pre_config():
    with open("config.json", 'r') as f:
        load_dict = json.load(f)
    return load_dict['box_id'], 'v1.58', getICCID()


def pre_mqtt_config():
    with open("config.json", 'r') as f:
        load_dict = json.load(f)

    addr = ''
    port = 0
    usr = ''
    pwd = ''
    try:
        for i in range(3):
            switch_key = 'server' + str(i + 1) + '_switch'
            if switch_key in load_dict:
                type_key = 'server' + str(i + 1) + '_type'
                typ = load_dict[type_key]
                if typ == '0' or typ == '3':
                    addr = load_dict['server' + str(i + 1) + '_addr']
                    port = int(load_dict['server' + str(i + 1) + '_port'])
                    usr = load_dict['server' + str(i + 1) + '_usr']
                    pwd = load_dict['server' + str(i + 1) + '_pwd']
                    break
            else:
                break
    except Exception:
        pass

    return addr, port, usr, pwd


def pre_nodes_config(dtuId):
    d_PlatDevice = dict()

    d_device = dict()
    d_product = dict()
    d_var_ex = dict()

    with open("nodes_config.json", 'r') as f:
        load_list = json.load(f)

    for node in load_list:
        id = node['attribute'][0]
        clazz = node['attribute'][1]
        if clazz == '1':
            d_product[id] = Product(node)
        elif clazz == '2':
            d_device[id] = Device(node)
        elif clazz == '5':
            d_var_ex[id] = VarEx(node)

    for device in d_device.values():
        name = device.name
        if name not in d_PlatDevice:
            d_PlatDevice[name] = PlatDevice(dtuId=dtuId, name=name)
        d_PlatDevice[name].addDevice(device=device)

        reference = device.node['reference'][0]
        if str(reference) in d_product:
            device.setProduct(d_product[str(reference)])

    for product in d_product.values():
        l_reference = product.node['reference']
        for reference in l_reference:
            if str(reference) in d_var_ex:
                product.addVarEx(d_var_ex[str(reference)])

    wouldRemoveKey = []
    for loop_device_name, platDevice in d_PlatDevice.items():
        hasOpcUaProduct = False
        for loop_device in platDevice.devices:
            if loop_device.product.protocol == 5 and loop_device.product.port == 3:
                hasOpcUaProduct=True
                break
        if not hasOpcUaProduct:
            wouldRemoveKey.append(loop_device_name)
    for loop_device_name in wouldRemoveKey:
        d_PlatDevice.pop(loop_device_name)

    return d_PlatDevice


def pre_remote_mqtt(dtuId, softVer, ICCID,
                    client_id, username, password):
    # 遗嘱数据
    will_payload = []
    will_payload.append({'dtuId': dtuId})
    will_payload_str = json.dumps(will_payload)
    will_payload_str_send = will_payload_str + getCrcModbusStr(will_payload_str)

    # 上线立即发送的数据
    l_msgOnStart = list()
    online_dtu_payload = {'protocalVer': 2,
                          'devType': 101,
                          'softVer': softVer,
                          'softVerNum': 0,
                          'ICCID': ICCID,
                          'CNUM': ''}
    online_dtu_payload_str = json.dumps(online_dtu_payload)
    online_dtu_payload_str_send = online_dtu_payload_str + getCrcModbusStr(online_dtu_payload_str)
    d_online_dtu = {'topic': 'productKey/receive/' + dtuId + '/dtuOn/dtuOnCallback',
                    'payload': online_dtu_payload_str_send}
    l_msgOnStart.append(d_online_dtu)

    # 设置发送服务
    sender = MQTTSender(client_id)
    sender.setUserNameAndPassword(username, password)
    # sender.setWill(will_topic='productKey/receive/' + dtuId + '/dtuOff', will_payload=will_payload_str_send)
    # sender.setMsgOnStart(l_msgOnStart)

    return sender


def pre_local_mqtt(dtuId, softVer, ICCID,
                   client_id):
    # 遗嘱数据
    will_payload = []
    will_payload.append({'dtuId': dtuId})
    will_payload_str = json.dumps(will_payload)
    will_payload_str_send = will_payload_str + getCrcModbusStr(will_payload_str)

    # 上线立即发送的数据
    l_msgOnStart = list()
    online_dtu_payload = {'protocalVer': 2,
                          'devType': 101,
                          'softVer': softVer,
                          'softVerNum': 0,
                          'ICCID': ICCID,
                          'CNUM': ''}
    online_dtu_payload_str = json.dumps(online_dtu_payload)
    online_dtu_payload_str_send = online_dtu_payload_str + getCrcModbusStr(online_dtu_payload_str)
    d_online_dtu = {'topic': 'productKey/receive/' + dtuId + '/dtuOn/dtuOnCallback',
                    'payload': online_dtu_payload_str_send}
    l_msgOnStart.append(d_online_dtu)

    # 设置发送服务
    sender = MQTTSender(client_id)
    sender.setWill(will_topic='productKey/receive/' + dtuId + '/dtuOff', will_payload=will_payload_str_send)
    sender.setMsgOnStart(l_msgOnStart)

    return sender


def opc_main():
    logging.info('OPCUA_MAIN START!')
    try:
        dtuId, softVer, ICCID = pre_config()
        addr, port, usr, pwd = pre_mqtt_config()
        remote_sender = pre_remote_mqtt(dtuId, softVer, ICCID, client_id=dtuId + '_py', username=usr, password=pwd)
        local_sender = pre_local_mqtt(dtuId, softVer, ICCID, client_id=dtuId + '_py')
        try:
            remote_sender.connect(host=addr, port=port, keepalive=20)  # mqtt连接动作
            local_sender.connect(host='127.0.0.1', port=1883, keepalive=20)  # mqtt连接动作
            d_PlatDevice = pre_nodes_config(dtuId)  # 内部有opc连接动作

            for platDevice in d_PlatDevice.values():
                platDevice.setSender(remote_sender, local_sender, {'dtuId': dtuId})
                platDevice.startJob()

            condition = threading.Condition()
            condition.acquire()
            condition.wait()
        finally:
            local_sender.loop_stop()
            local_sender.disconnect()
            remote_sender.loop_stop()
            remote_sender.disconnect()
    except Exception as e:
        logging.error('OPCUA_MAIN ERROR!' + str(e))
    finally:
        logging.info('OPCUA_MAIN STOP!')
