#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncua import ua


class SubHandler(object):

    def __init__(self, obj):
        self.obj = obj

    async def datachange_notification(self, node, val, data):
        # print("Python: New data change event", node, val, data)

        _node_name = await node.read_browse_name()
        setattr(self.obj, _node_name.Name, data.monitored_item.Value.Value.Value)

    async def event_notification(self, event):
        print("Python: New event", event)


class UaObject(object):

    def __init__(self, asyncua_server, ua_node_value):
        self.asyncua_server = asyncua_server
        self.ua_node_value = ua_node_value

    async def init(self):
        self.b_name = await self.ua_node_value.read_browse_name()

        handler = SubHandler(self)
        sub = await self.asyncua_server.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(self.ua_node_value)

    async def write_value(self):
        # await self.ua_node_value.write_value(getattr(self, self.name))
        await self.asyncua_server.write_attribute_value(self.ua_node_value.nodeid,
                                                        ua.DataValue(getattr(self, self.b_name.Name)))

class MyIntObj(UaObject):

    def __init__(self, asyncua_server, ua_node_value):
        self.value = 0

        super().__init__(asyncua_server, ua_node_value)

    async def init(self):
        await super().init()


class MyFloatObj(UaObject):

    def __init__(self, asyncua_server, ua_node_value):
        self.value = 0.0

        super().__init__(asyncua_server, ua_node_value)

    async def init(self):
        await super().init()


class MyBoolObj(UaObject):

    def __init__(self, asyncua_server, ua_node_value):
        self.value = False

        super().__init__(asyncua_server, ua_node_value)

    async def init(self):
        await super().init()

