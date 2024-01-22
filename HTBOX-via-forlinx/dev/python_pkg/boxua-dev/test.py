#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging
import threading

from boxua import boxua_global_v
from boxua.client.bxoua_client import BoxUaClient
from hnpc import hnpc_global_v
from hnpc.hnpc_global_f import trans_nodes_config2dict


async def main():
    try:

        trans_nodes_config2dict()

        for product_node_attribute_id in hnpc_global_v.d_product:
            product_node = hnpc_global_v.d_product[product_node_attribute_id]
            if product_node.product.protocol == 5 and product_node.product.port == 3:  # 采集方式OPCUA
                l_device_node = product_node.reference.parent_nodes
                if len(l_device_node) == 1:
                    boxuaclient = BoxUaClient(l_device_node[0], product_node)
                    boxuaclient.setDaemon(True)
                    boxuaclient.start()
                    await asyncio.sleep(5)
                    await boxuaclient.test()
                else:
                    continue
            else:  # 非OPCUA采集
                pass

        condition = threading.Condition()
        condition.acquire()
        condition.wait()
    except Exception as e:
        print(e)
    finally:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
