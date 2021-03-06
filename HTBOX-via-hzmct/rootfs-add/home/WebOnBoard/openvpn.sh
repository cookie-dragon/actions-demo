#!/bin/sh
openvpn=/usr/sbin/openvpn

test -x "$openvpn" || exit 0

case "$1" in
  start)
    if [[ $# != 2 ]]
    then
        echo "Usage: /etc/init.d/openvpn.sh {start} {iface}"
        exit 1
    fi
    iface=$2

    echo -n "Starting OpenVPN"
    openvpn --mktun --dev tap0
    brctl addbr br-vpn
    brctl addif br-vpn tap0 ${iface}
    ifconfig tap0 0.0.0.0 promisc up
    ifconfig ${iface} 0.0.0.0 promisc up
    ifup br-vpn
    route del default
    cd /etc/openvpn
    openvpn --config client.conf &
    echo "."
    ;;
  stop)
    if [[ $# != 2 ]]
    then
        echo "Usage: /etc/init.d/openvpn.sh {stop} {iface}"
        exit 1
    fi
    iface=$2

    echo -n "Stopping OpenVPN"
    kill -9 `ps | grep openvpn | head -1 | awk '{printf $1}'`
    ifdown br-vpn
    brctl delif br-vpn tap0
    brctl delif br-vpn ${iface}
    brctl delbr br-vpn
    openvpn --rmtun --dev tap0
    ifdown ${iface}
    ifup ${iface}
    route del default
    ./routeUG.sh
    echo "."
    ;;
  restart)
    echo -n "Stopping OpenVPN"
    kill -9 `ps | grep openvpn | head -1 | awk '{printf $1}'`
    ./routeUG.sh
    echo "."
    echo -n "Waiting for OpenVPN to die off"
    for i in 1 2 3 4 5;
    do
        sleep 1
        echo -n "."
    done
    echo ""
    echo -n "Starting OpenVPN"
    cd /etc/openvpn
    openvpn --config client.conf &
    echo "."
    ;;
  status)
    statstr=`ps | grep openvpn | head -1 | awk '{printf $7}'`
    if [[ ${statstr} != "client.conf" ]]; then
        echo -n "OpenVPN NOT started"
        echo "."
        exit 1
    fi
    echo -n "OpenVPN is STARTED"
    echo "."
    ;;
  getconfig)
    echo -n "Getting OpenVPN Config"
    if [[ $# != 5 ]]
    then
        echo "Usage: /etc/init.d/openvpn.sh {getconfig} {urlheader compId id token}"
        exit 1
    fi
    opt_head=$2
    opt_compId=$3
    opt_id=$4
    opt_token=$5

    curlresult=$(curl -X GET \
      "${opt_head}/service/getConfig?compId=${opt_compId}&id=${opt_id}" \
      -H "Authorization: ${opt_token}"
    )

    echo $curlresult

    result=$(echo ${curlresult} | jq '.result' | sed 's/^"//g' | sed 's/"$//g')
    if [[ ${result} != "true" ]]
    then
        exit 1
    fi

    mkdir -p /etc/openvpn

    client_conf=$(echo ${curlresult} | jq '.data.client_conf' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${client_conf} > /etc/openvpn/client.conf

    ca_crt=$(echo ${curlresult} | jq '.data.ca_crt' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${ca_crt} > /etc/openvpn/ca.crt

    crl_pem=$(echo ${curlresult} | jq '.data.crl_pem' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${crl_pem} > /etc/openvpn/crl.pem

    dh_pem=$(echo ${curlresult} | jq '.data.dh_pem' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${dh_pem} > /etc/openvpn/dh.pem

    ta_key=$(echo ${curlresult} | jq '.data.ta_key' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${ta_key} > /etc/openvpn/ta.key

    client_crt=$(echo ${curlresult} | jq '.data.client_crt' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${client_crt} > /etc/openvpn/client.crt

    client_key=$(echo ${curlresult} | jq '.data.client_key' | sed 's/^"//g' | sed 's/"$//g')
    echo -e ${client_key} > /etc/openvpn/client.key

    echo "."
    ;;
  *)
    echo "Usage: /etc/init.d/openvpn.sh {start|stop|restart|status|getconfig}"
    exit 1
esac

exit 0
