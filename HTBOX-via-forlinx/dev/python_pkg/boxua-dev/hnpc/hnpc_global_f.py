#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from hnpc import hnpc_global_v
from hnpc.node_device import DeviceNode
from hnpc.node_product import ProductNode
from hnpc.p_node_varex.node_varex0 import VarNodeEx0
from hnpc.p_node_varex.node_varex1 import VarNodeEx1
from hnpc.p_node_varex.node_varex2 import VarNodeEx2
from hnpc.p_node_varex.node_varex9 import VarNodeEx9

def trans_nodes_config2dict():
    with open("etc/htbox/nodes_config.json", 'r') as f:
        hnpc_global_v.nodes = json.load(f)

    for node in hnpc_global_v.nodes:
        node_attribute_id = node['attribute'][0]
        node_attribute_clazz = node['attribute'][1]
        if node_attribute_clazz == '1':
            hnpc_global_v.d_product[str(node_attribute_id)] = ProductNode(node)
        elif node_attribute_clazz == '2':
            hnpc_global_v.d_device[str(node_attribute_id)] = DeviceNode(node)
        elif node_attribute_clazz == '5':
            if node['var_ex'][0] == 0:
                n = VarNodeEx0(node)
                n.init()
                hnpc_global_v.d_var[str(node_attribute_id)] = n
            elif node['var_ex'][0] == 1:
                n = VarNodeEx1(node)
                n.init()
                hnpc_global_v.d_var[str(node_attribute_id)] = n
            elif node['var_ex'][0] == 2:
                n = VarNodeEx2(node)
                n.init()
                hnpc_global_v.d_var[str(node_attribute_id)] = n
            elif node['var_ex'][0] == 9:
                n = VarNodeEx9(node)
                n.init()
                hnpc_global_v.d_var[str(node_attribute_id)] = n

    # <editor-fold desc="reference 关联">
    hnpc_global_v.d_node.update(hnpc_global_v.d_device)
    hnpc_global_v.d_node.update(hnpc_global_v.d_product)
    hnpc_global_v.d_node.update(hnpc_global_v.d_var)

    for (node_attribute_id, node) in hnpc_global_v.d_node.items():
        for child_node_attribute_id in node.reference.child_node_ids:
            if str(child_node_attribute_id) in hnpc_global_v.d_node.keys():
                child_node = hnpc_global_v.d_node[str(child_node_attribute_id)]
                node.reference.child_nodes.append(child_node)
                child_node.reference.parent_node_ids.append(node_attribute_id)
                child_node.reference.parent_nodes.append(node)
    # </editor-fold>

    for (node_attribute_id, node) in hnpc_global_v.d_var.items():
        hnpc_global_v.d_var_by_name[node.attribute.name] = node