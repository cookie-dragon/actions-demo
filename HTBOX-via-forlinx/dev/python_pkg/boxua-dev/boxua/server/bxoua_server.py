#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from threading import Thread

from asyncua import Server, Node
from asyncua.common.callback import CallbackType

from boxua.boxua_error import UnWritableError
from boxua.boxua_pyobj import *
from boxua.boxua_typ import *
from hnpc import hnpc_global_v
from hnpc.inode_value import ValueNodeI
from hnpc.node_device import DeviceNode
from hnpc.node_product import ProductNode
from hnpc.p_node_varex.node_varex0 import VarNodeEx0
from hnpc.p_node_varex.node_varex1 import VarNodeEx1
from hnpc.p_node_varex.node_varex2 import VarNodeEx2
from hnpc.p_node_varex.node_varex9 import VarNodeEx9


class BoxUaServer(Thread):
    def __init__(self):
        super().__init__()
        self.running_tag = False

        self.asyncua_server = None
        self.namespace_idx = -1

        self.ua_d_var_by_id = dict()
        self.ua_d_var_by_name = dict()
        self.ua_d_var_by_nodeid = dict()

    async def build_device(self, uanode_device: Node, hnpcnode_device: DeviceNode):
        uanode_device_attribute_id = await uanode_device.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:id"])
        uanode_device_attribute_clazz = await uanode_device.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:clazz"])
        uanode_device_attribute_name = await uanode_device.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:name"])
        uanode_device_attribute_path = await uanode_device.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:path"])

        uanode_device_device_collect_cycle = await uanode_device.get_child(
            [f"{self.namespace_idx}:device", f"{self.namespace_idx}:collect_cycle"])
        uanode_device_device_report_cycle = await uanode_device.get_child(
            [f"{self.namespace_idx}:device", f"{self.namespace_idx}:report_cycle"])

        await uanode_device_attribute_id.set_value(hnpcnode_device.attribute.id)
        await uanode_device_attribute_clazz.set_value(hnpcnode_device.attribute.clazz)
        await uanode_device_attribute_name.set_value(hnpcnode_device.attribute.name)
        await uanode_device_attribute_path.set_value(hnpcnode_device.attribute.path)

        await uanode_device_device_collect_cycle.set_value(hnpcnode_device.device.collect_cycle)
        await uanode_device_device_report_cycle.set_value(hnpcnode_device.device.report_cycle)

    async def build_product(self, uanode_product: Node, hnpcnode_product: ProductNode):
        uanode_product_attribute_id = await uanode_product.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:id"])
        uanode_product_attribute_clazz = await uanode_product.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:clazz"])
        uanode_product_attribute_name = await uanode_product.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:name"])
        uanode_product_attribute_path = await uanode_product.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:path"])

        uanode_product_product_protocol = await uanode_product.get_child(
            [f"{self.namespace_idx}:product", f"{self.namespace_idx}:protocol"])
        uanode_product_product_port = await uanode_product.get_child(
            [f"{self.namespace_idx}:product", f"{self.namespace_idx}:port"])

        await uanode_product_attribute_id.set_value(hnpcnode_product.attribute.id)
        await uanode_product_attribute_clazz.set_value(hnpcnode_product.attribute.clazz)
        await uanode_product_attribute_name.set_value(hnpcnode_product.attribute.name)
        await uanode_product_attribute_path.set_value(hnpcnode_product.attribute.path)

        await uanode_product_product_protocol.set_value(hnpcnode_product.product.protocol)
        await uanode_product_product_port.set_value(hnpcnode_product.product.port)

    async def build_var(self, uanode_var: Node, hnpcnode_var: ValueNodeI):
        uanode_var_attribute_id = await uanode_var.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:id"])
        uanode_var_attribute_clazz = await uanode_var.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:clazz"])
        uanode_var_attribute_name = await uanode_var.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:name"])
        uanode_var_attribute_path = await uanode_var.get_child(
            [f"{self.namespace_idx}:attribute", f"{self.namespace_idx}:path"])

        uanode_var_var = await uanode_var.get_child([f"{self.namespace_idx}:var"])
        uanode_var_var_type = await uanode_var_var.get_child([f"{self.namespace_idx}:type"])
        uanode_var_var_rw = await uanode_var_var.get_child([f"{self.namespace_idx}:rw"])

        await uanode_var_attribute_id.set_value(hnpcnode_var.attribute.id)
        await uanode_var_attribute_clazz.set_value(hnpcnode_var.attribute.clazz)
        await uanode_var_attribute_name.set_value(hnpcnode_var.attribute.name)
        await uanode_var_attribute_path.set_value(hnpcnode_var.attribute.path)

        await uanode_var_var_type.set_value(hnpcnode_var.var.type)
        await uanode_var_var_rw.set_value(hnpcnode_var.var.rw)

        if isinstance(hnpcnode_var, VarNodeEx0):
            if hnpcnode_var.var.symbol == 0:  # 0:无符号
                if hnpcnode_var.var.valuesize == 0:  # 0:8位 1:16位 2:32位 3:64位
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.Byte)
                elif hnpcnode_var.var.valuesize == 1:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.UInt16)
                elif hnpcnode_var.var.valuesize == 2:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.UInt32)
                elif hnpcnode_var.var.valuesize == 3:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.UInt64)
                else:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.UInt32)
            else:  # 1:有符号
                if hnpcnode_var.var.valuesize == 0:  # 0:8位 1:16位 2:32位 3:64位
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.SByte)
                elif hnpcnode_var.var.valuesize == 1:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.Int16)
                elif hnpcnode_var.var.valuesize == 2:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.Int32)
                elif hnpcnode_var.var.valuesize == 3:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.Int64)
                else:
                    var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0,
                                                                      ua.VariantType.Int32)
            py_value = MyIntObj(self.asyncua_server, var_var_value)
        elif isinstance(hnpcnode_var, VarNodeEx1):
            var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0.0, ua.VariantType.Float)
            py_value = MyFloatObj(self.asyncua_server, var_var_value)
        elif isinstance(hnpcnode_var, VarNodeEx2):
            var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0.0, ua.VariantType.Double)
            py_value = MyFloatObj(self.asyncua_server, var_var_value)
        elif isinstance(hnpcnode_var, VarNodeEx9):
            var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", False,
                                                              ua.VariantType.Boolean)
            py_value = MyBoolObj(self.asyncua_server, var_var_value)
        else:
            var_var_value = await uanode_var_var.add_variable(self.namespace_idx, "value", 0, ua.VariantType.Int32)
            py_value = MyIntObj(self.asyncua_server, var_var_value)
        await var_var_value.set_writable(False if hnpcnode_var.var.rw == 0 else True)
        await py_value.init()
        # 构建列表(id ,name, nodeid) (var_node:ValueNodeI, py_value:MyObj)
        self.ua_d_var_by_id[str(hnpcnode_var.attribute.id)] = (hnpcnode_var, py_value)
        self.ua_d_var_by_name[hnpcnode_var.attribute.name] = (hnpcnode_var, py_value)
        self.ua_d_var_by_nodeid[py_value.ua_node_value.nodeid] = (hnpcnode_var, py_value)

    async def server_main(self):
        self.asyncua_server = Server()
        await self.asyncua_server.init()

        self.asyncua_server.disable_clock()  # for debuging

        self.asyncua_server.set_endpoint("opc.tcp://0.0.0.0:4840/boxua/server/")
        self.asyncua_server.set_server_name("BoxUa Server")

        self.asyncua_server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])

        uri = "http://haitianiot.com"
        self.namespace_idx = await self.asyncua_server.register_namespace(uri)

        # <editor-fold desc="ua_type">
        uatyp_device = await init_uatyp_device(self.asyncua_server, self.namespace_idx)
        uatyp_product = await init_uatyp_product(self.asyncua_server, self.namespace_idx)
        uatyp_var = await init_uatyp_var(self.asyncua_server, self.namespace_idx)
        # </editor-fold>

        # <editor-fold desc="ua_structure">
        f_boxua = await self.asyncua_server.nodes.objects.add_folder(self.namespace_idx, "BoxUa")
        for device_node_attribute_id in hnpc_global_v.d_device:
            device_node = hnpc_global_v.d_device[device_node_attribute_id]
            mydevice = await f_boxua.add_object(self.namespace_idx, device_node.attribute.name, uatyp_device)
            f_product = await mydevice.add_folder(self.namespace_idx, "products")
            for product_node in device_node.reference.child_nodes:
                myproduct = await f_product.add_object(self.namespace_idx, product_node.attribute.name, uatyp_product)
                f_var = await myproduct.add_folder(self.namespace_idx, "vars")
                for var_node in product_node.reference.child_nodes:
                    myvar = await f_var.add_object(self.namespace_idx, var_node.attribute.name, uatyp_var)
        # </editor-fold>

        # starting!
        async with self.asyncua_server:

            # <editor-fold desc="ua_property">
            f_boxua = await self.asyncua_server.nodes.objects.get_child(f"{self.namespace_idx}:BoxUa")
            for device_node_attribute_id in hnpc_global_v.d_device:
                device_node = hnpc_global_v.d_device[device_node_attribute_id]
                mydevice = await f_boxua.get_child(f"{self.namespace_idx}:" + device_node.attribute.name)
                await self.build_device(mydevice, device_node)

                f_product = await mydevice.get_child(f"{self.namespace_idx}:products")
                for product_node in device_node.reference.child_nodes:
                    myproduct = await f_product.get_child(f"{self.namespace_idx}:" + product_node.attribute.name)
                    await self.build_product(myproduct, product_node)

                    f_var = await myproduct.get_child(f"{self.namespace_idx}:vars")
                    for var_node in product_node.reference.child_nodes:
                        myvar = await f_var.get_child(f"{self.namespace_idx}:" + var_node.attribute.name)
                        await self.build_var(myvar, var_node)
            # </editor-fold>

            self.asyncua_server.subscribe_server_callback(CallbackType.PreWrite, self.pre_write)
            self.asyncua_server.subscribe_server_callback(CallbackType.PostWrite, self.post_write)

            while self.running_tag:
                await asyncio.sleep(0.1)

            print("Asyncua Server Stop!")

    async def pre_write(self, event, dispatcher):  # 外部写入触发，内部写入采用server.write_attribute_value不触发此函数
        for idx in range(len(event.request_params.NodesToWrite)):
            nodeId = event.request_params.NodesToWrite[idx].NodeId
            value = event.request_params.NodesToWrite[idx].Value.Value.Value
            s = str(nodeId)
            node_value = self.asyncua_server.get_node(s)
            node_var = await node_value.get_parent()
            node_rw = await node_var.get_child(f"{self.namespace_idx}:rw")
            value_in_node_rw = await node_rw.read_value()
            if value_in_node_rw != 0:  # 先判断是否可写
                if True:  # 根据nodeId找到结构体，查询采集方式，若非OPC采集，则MQTT通知写入（不进行逆向运算），若为OPC采集，找到制定OPCClient发送写入请求（先进行逆向运算）
                    print(f"Node {nodeId} prepare to write: " + str(value))
                else:
                    raise Exception(f"Node {nodeId} to write ERROR!")
            else:
                raise UnWritableError(f"Node {nodeId} to write ERROR, readOnly!")

    async def post_write(self, event, dispatcher):
        for idx in range(len(event.response_params)):
            if event.response_params[idx].is_good():
                nodeId = event.request_params.NodesToWrite[idx].NodeId
                value = event.request_params.NodesToWrite[idx].Value.Value.Value
                print(f"Node {nodeId} was writed: " + str(value))

    def run(self):
        self.running_tag = True
        asyncio.run(self.server_main())

    def stop(self):
        self.running_tag = False
        while self.is_alive():
            pass
        print("Stop!!")
