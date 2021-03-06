#!/bin/sh

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
    openvpn --rmtun --dev $t
done

route del default
ifdown ${eth}
sleep 1
ifup ${eth}
route del default
