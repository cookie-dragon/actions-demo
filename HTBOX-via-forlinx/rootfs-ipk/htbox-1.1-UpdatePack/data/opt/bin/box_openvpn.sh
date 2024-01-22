#!/bin/sh
openvpn_path=/usr/sbin/openvpn
defroute_monitor_path=/opt/bin/defroute_monitor

test -x "$openvpn_path" || exit 0

start() {
  kill -9 `ps | grep "${defroute_monitor_path}" | grep -v "grep" | head -1 | awk '{printf $1}'`
  sleep 1
  route del default

  /usr/local/bin/bridge-start.sh
  cd /etc/openvpn
  ${openvpn_path} --config client.conf > /dev/null &

  route del default
  ${defroute_monitor_path} > /dev/null &
}

stop() {
  kill -9 `ps | grep "${defroute_monitor_path}" | grep -v "grep" | head -1 | awk '{printf $1}'`
  sleep 1
  route del default

  kill -9 `ps | grep "${openvpn_path}" | grep -v "grep" | head -1 | awk '{printf $1}'`
  /usr/local/bin/bridge-stop.sh

  route del default
  ${defroute_monitor_path} > /dev/null &
}

case "$1" in
  start)
    echo -n "Starting OpenVPN"
    start
    echo "."
    ;;
  stop)
    echo -n "Stopping OpenVPN"
    stop
    echo "."
    ;;
  restart)
    stop
    echo -n "Waiting for OpenVPN to die off"
    for i in 1 2 3 4 5;
    do
      sleep 1
      echo -n "."
    done
    echo ""
    start
    ;;
  status)
    statstr=`ps | grep "${openvpn_path}" | grep -v "grep" | head -1 | awk '{printf $5}'`
    if [[ ${statstr} != "client.conf" ]]; then
      echo "OpenVPN is NOT started"
    else
      echo "OpenVPN is STARTED"
    fi
    ;;
  getconfig)
    echo -n "Getting OpenVPN Config"

    if [[ $# != 5 ]]
    then
        echo "Usage: $0 {getconfig} {urlheader compId id token}"
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

    # result=$(echo ${curlresult} | jq '.result' | sed 's/^"//g' | sed 's/"$//g')
    # if [[ ${result} != "true" ]]
    # then
    #     exit 1
    # fi

    mkdir -p /etc/openvpn
    
    /opt/bin/box_set_vpn_cert "${curlresult}"
    if [[ $? -ne 0 ]]; then
      exit 1
    fi

    # client_conf=$(echo ${curlresult} | jq '.data.client_conf' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${client_conf} > /etc/openvpn/client.conf

    # ca_crt=$(echo ${curlresult} | jq '.data.ca_crt' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${ca_crt} > /etc/openvpn/ca.crt

    # crl_pem=$(echo ${curlresult} | jq '.data.crl_pem' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${crl_pem} > /etc/openvpn/crl.pem

    # dh_pem=$(echo ${curlresult} | jq '.data.dh_pem' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${dh_pem} > /etc/openvpn/dh.pem

    # ta_key=$(echo ${curlresult} | jq '.data.ta_key' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${ta_key} > /etc/openvpn/ta.key

    # client_crt=$(echo ${curlresult} | jq '.data.client_crt' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${client_crt} > /etc/openvpn/client.crt

    # client_key=$(echo ${curlresult} | jq '.data.client_key' | sed 's/^"//g' | sed 's/"$//g')
    # echo -e ${client_key} > /etc/openvpn/client.key

    echo "."
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|getconfig}"
    exit 1
esac

exit 0
