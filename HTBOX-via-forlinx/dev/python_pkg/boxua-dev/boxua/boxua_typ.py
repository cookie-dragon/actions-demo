#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncua import ua


async def init_uatyp_device(server, idx):
    uatyp_device = await server.nodes.base_object_type.add_object_type(idx, "HiDevice")

    uatyp_device_attribute = await uatyp_device.add_object(idx, "attribute")
    await uatyp_device_attribute.set_modelling_rule(True)

    await (await uatyp_device_attribute.add_property(idx, "id", 0)).set_modelling_rule(True)
    await (await uatyp_device_attribute.add_property(idx, "clazz", 0)).set_modelling_rule(True)
    await (await uatyp_device_attribute.add_property(idx, "name", "")).set_modelling_rule(True)
    await (await uatyp_device_attribute.add_property(idx, "path", "")).set_modelling_rule(True)

    uatyp_device_device = await uatyp_device.add_object(idx, "device")
    await uatyp_device_device.set_modelling_rule(True)

    await (await uatyp_device_device.add_property(idx, "collect_cycle", 0)).set_modelling_rule(True)
    await (await uatyp_device_device.add_property(idx, "report_cycle", 0)).set_modelling_rule(True)

    return uatyp_device


async def init_uatyp_product(server, idx):
    uatyp_product = await server.nodes.base_object_type.add_object_type(idx, "HiProduct")

    uatyp_product_attribute = await uatyp_product.add_object(idx, "attribute")
    await uatyp_product_attribute.set_modelling_rule(True)

    await (await uatyp_product_attribute.add_property(idx, "id", 0)).set_modelling_rule(True)
    await (await uatyp_product_attribute.add_property(idx, "clazz", 0)).set_modelling_rule(True)
    await (await uatyp_product_attribute.add_property(idx, "name", "")).set_modelling_rule(True)
    await (await uatyp_product_attribute.add_property(idx, "path", "")).set_modelling_rule(True)

    uatyp_product_product = await uatyp_product.add_object(idx, "product")
    await uatyp_product_product.set_modelling_rule(True)

    await (await uatyp_product_product.add_property(idx, "protocol", 0)).set_modelling_rule(True)
    await (await uatyp_product_product.add_property(idx, "port", 0)).set_modelling_rule(True)

    return uatyp_product


async def init_uatyp_var(server, idx):
    uatyp_var = await server.nodes.base_object_type.add_object_type(idx, "HiVar")

    uatyp_var_attribute = await uatyp_var.add_object(idx, "attribute")
    await uatyp_var_attribute.set_modelling_rule(True)

    await (await uatyp_var_attribute.add_property(idx, "id", 0)).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "clazz", 0)).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "name", "")).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "path", "")).set_modelling_rule(True)

    uatyp_var_var = await uatyp_var.add_object(idx, "var")
    await uatyp_var_var.set_modelling_rule(True)

    await (await uatyp_var_var.add_property(idx, "type", 0)).set_modelling_rule(True)
    await (await uatyp_var_var.add_property(idx, "rw", 0)).set_modelling_rule(True)

    return uatyp_var


async def init_uatyp_var_ua(server, idx, variant_type: ua.VariantType):
    uatyp_var = await server.nodes.base_object_type.add_object_type(idx, "HiVar." + str(variant_type))

    uatyp_var_attribute = await uatyp_var.add_object(idx, "attribute")
    await uatyp_var_attribute.set_modelling_rule(True)

    await (await uatyp_var_attribute.add_property(idx, "id", 0)).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "clazz", 0)).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "name", "")).set_modelling_rule(True)
    await (await uatyp_var_attribute.add_property(idx, "path", "")).set_modelling_rule(True)

    uatyp_var_var = await uatyp_var.add_object(idx, "var")
    await uatyp_var_var.set_modelling_rule(True)

    await (await uatyp_var_var.add_property(idx, "type", 0)).set_modelling_rule(True)
    await (await uatyp_var_var.add_property(idx, "rw", 0)).set_modelling_rule(True)

    await (await uatyp_var_var.add_variable(idx, "value", 0, variant_type)).set_modelling_rule(True)

    return uatyp_var
