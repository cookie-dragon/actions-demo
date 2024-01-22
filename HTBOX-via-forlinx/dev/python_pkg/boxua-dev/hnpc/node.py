#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hnpc.hnpc_error import NodesConfigError


class NodeAttribute(object):
    def __init__(self, l_attribute):
        try:
            self.id = int(l_attribute[0])  # 节点ID 无符号32位整数
            self.clazz = int(l_attribute[1])  # 节点属类 8位整形枚举 0:dtu 1:product 2:device 3:group 4:var 5:var_ex
            self.name = str(l_attribute[2])  # 节点命名 字符串
            self.path = str(l_attribute[3])  # 拓扑结构中的ID 字符串
        except Exception:
            raise NodesConfigError("node attribute decode error")


class NodeReference(object):
    def __init__(self, l_reference):
        self.child_node_ids = []  # 引用 无符号32位整数

        try:
            for reference in l_reference:
                self.child_node_ids.append(int(reference))
        except Exception:
            raise NodesConfigError("node reference decode error")

        self.parent_node_ids = []
        self.child_nodes = []
        self.parent_nodes = []


class Node(object):
    def __init__(self, node):
        self.node = node
        self.attribute = NodeAttribute(node['attribute'])
        self.reference = NodeReference(node['reference'])
