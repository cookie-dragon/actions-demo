#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
import json
import sys

if __name__ == '__main__':
    exit_sys = 1

    if len(sys.argv) == 2:
        try:
            d = json.loads(sys.argv[1])
            if d['result']:
                with open('/etc/openvpn/client.conf', 'w') as f:
                    f.write(d['data']['client_conf'])
                with open('/etc/openvpn/ca.crt', 'w') as f:
                    f.write(d['data']['ca_crt'])
                with open('/etc/openvpn/crl.pem', 'w') as f:
                    f.write(d['data']['crl_pem'])
                with open('/etc/openvpn/dh.pem', 'w') as f:
                    f.write(d['data']['dh_pem'])
                with open('/etc/openvpn/ta.key', 'w') as f:
                    f.write(d['data']['ta_key'])
                with open('/etc/openvpn/client.crt', 'w') as f:
                    f.write(d['data']['client_crt'])
                with open('/etc/openvpn/client.key', 'w') as f:
                    f.write(d['data']['client_key'])
                exit_sys = 0
        except Exception as e:
            pass

    sys.exit(exit_sys)
