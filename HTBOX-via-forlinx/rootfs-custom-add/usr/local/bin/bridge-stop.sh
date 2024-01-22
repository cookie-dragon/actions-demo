#!/bin/sh
openvpn_path=/usr/sbin/openvpn

####################################
# Tear Down Ethernet bridge on Linux
####################################

# Define Bridge Interface
br="br-vpn"

# Define list of TAP interfaces to be bridged together
tap="tap0"

# Define physical ethernet interface to be bridged
# with TAP interface(s) above.
eth="eth1"

ifconfig $br down
brctl delbr $br

for t in $tap; do
    ${openvpn_path} --rmtun --dev $t
done

route del default

etho=""
if [ $eth = "eth1" ]; then
  etho="eth0"
fi

if [ $eth = "eth0" ]; then
  etho="eth1"
fi

# etho not empty
if [ -n "$etho" ]; then
  ifdown ${etho}
  ifconfig ${etho} down
  sleep 1
fi

ifdown ${eth}
ifconfig ${eth} -promisc down
sleep 1
ifup ${eth}
sleep 1

if [ -n "$etho" ]; then
  ifup ${etho}
  sleep 1
fi

route del default
