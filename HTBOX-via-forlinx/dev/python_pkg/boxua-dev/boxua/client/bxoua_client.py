#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import ipaddress
from threading import Thread

from asyncua import Client

from boxua import boxua_global_v


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)


class BoxUaClient(Thread):
    def __init__(self, device_node, product_node):
        super().__init__()
        self.running_tag = False

        self.device_node = device_node
        self.product_node = product_node
        self.var_nodes = []
        self.__init()

    def __init(self):
        dev_IP = self.device_node.device.dev_IP
        dev_InvterPort = self.device_node.device.dev_InvterPort
        dev_serverpath = self.device_node.device.dev_serverpath
        self.endPointUrl = 'opc.tcp://' + ipaddress.IPv4Address(dev_IP).compressed + ':' + str(
            dev_InvterPort) + dev_serverpath
        self.collect_cycle = self.device_node.device.collect_cycle
        for var_node in self.product_node.reference.child_nodes:
            boxua_global_v.d_boxuaclient_by_varid[str(var_node.attribute.id)] = self
            self.var_nodes.append(var_node)

    async def client_main(self):
        self.client = Client(url=self.endPointUrl)
        async with self.client:
            handler = SubHandler()
            sub = await self.client.create_subscription(self.collect_cycle, handler)
            for var_node in self.var_nodes:
                uanode = self.client.get_node(var_node.var.hnpchicpath)
                handle = await sub.subscribe_data_change(uanode)

            while self.running_tag:
                await asyncio.sleep(0.1)

            print("Asyncua Client Stop!")

    def run(self):
        self.running_tag = True
        asyncio.run(self.client_main())

    def stop(self):
        self.running_tag = False
        while self.is_alive():
            pass
        print("Stop!!")

    async def test(self):
        var = self.client.get_node("ns=2;i=372")
        await var.write_value(10)
