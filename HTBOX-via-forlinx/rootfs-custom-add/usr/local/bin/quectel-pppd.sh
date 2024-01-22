#!/bin/sh

#quectel-pppd devname apn user password
echo "quectel-pppd options in effect:"
QL_DEVNAME=/dev/ttyUSB3
QL_APN=3gnet
QL_USER=user
QL_PASSWORD=passwd
if [ $# -ge 1 ]; then
	QL_DEVNAME=$1	
	echo "devname   $QL_DEVNAME    # (from command line)"
else
	echo "devname   $QL_DEVNAME    # (default)"
fi
if [ $# -ge 2 ]; then
	QL_APN=$2	
	echo "apn       $QL_APN    # (from command line)"
else
	echo "apn       $QL_APN    # (default)"
fi
if [ $# -ge 3 ]; then
	QL_USER=$3	
	echo "user      $QL_USER   # (from command line)"
else
	echo "user      $QL_USER   # (default)"
fi
if [ $# -ge 4 ]; then
	QL_PASSWORD=$4	
	echo "password  $QL_PASSWORD   # (from command line)"
else
	echo "password  $QL_PASSWORD   # (default)"
fi

CONNECTYY="'chat -s -v \
ABORT BUSY \
ABORT \"NO CARRIER\" \
ABORT \"NO DIALTONE\" \
ABORT ERROR \
ABORT \"NO ANSWER\" \
TIMEOUT 30 \
\"\" AT \
OK ATE0 \
OK ATI\;+CSUB\;+CSQ\;+CPIN?\;+COPS?\;+CGREG?\;\&D2 \
OK AT+CGDCONT=1,\\\"IP\\\",\\\"$QL_APN\\\",,0,0 \
OK ATD*99# \
CONNECT \
'"

CONNECTXY="'chat -s -v \
TIMEOUT 5 \
ECHO ON \
ABORT '\nBUSY\r' \
ABORT '\nERROR\r' \
ABORT '\nRINGING\r\n\r\nRINGING\r' \
ABORT '\nCOMMAND NO RESPONSE!\r' \
'' AT \
TIMEOUT 60 \
SAY \"Press CTRL-C to break the connection process.\n\" \
OK 'ATE0' \
OK 'AT+CGACT=0,1' \
OK 'AT+CGDCONT=1,\\\"IPV4V6\\\",\\\"$QL_APN\\\"' \
OK 'AT+CGACT=1,1' \
OK 'ATD*99***1#' \
TIMEOUT 60 \
SAY \"Waiting for connect...\n\" \
CONNECT '' \
SAY \"connect Success!\n\" \
'"

# 4G模块判断
exist_ec20_module=0
exist_ec200s_module=0
exist_xy200_module=0

exist_ec20=`lsusb | grep "2c7c:0125" | grep -v "grep"`
exist_ec200s=`lsusb | grep "2c7c:6002" | grep -v "grep"`
exist_xy200=`lsusb | grep "1782:4d10" | grep -v "grep"`

if [[ ! -z $exist_ec20 ]] ; then
	echo "There is a supported 4G module: EC20"
	exist_ec20_module=1
elif [[ ! -z $exist_ec200s ]]; then
	echo "There is a supported 4G module: EC200S"
	exist_ec200s_module=1
elif [[ ! -z $exist_xy200 ]]; then
	echo "There is a supported 4G module: XY200"
	exist_xy200_module=1
else
	echo "There is no supported 4G module"
fi

if [[ $exist_ec20_module -eq 1 ]] || [[ $exist_ec200s_module -eq 1 ]]; then
	pppd $QL_DEVNAME 115200 user "$QL_USER" password "$QL_PASSWORD" \
	connect "'$CONNECTYY'" \
	disconnect 'chat -s -v ABORT ERROR ABORT "NO DIALTONE" SAY "\nSending break to the modem\n" "" +++ "" +++ "" +++ SAY "\nGood bay\n"' \
	noauth debug defaultroute noipdefault novj novjccomp noccp ipcp-accept-local ipcp-accept-remote ipcp-max-configure 30 local lock modem dump nodetach nocrtscts usepeerdns &
elif [[ $exist_xy200_module -eq 1 ]]; then
	pppd $QL_DEVNAME 115200 user "$QL_USER" password "$QL_PASSWORD" \
	connect "'$CONNECTXY'" \
	nolock local debug nocrtscts nodetach noauth usepeerdns defaultroute &
else
	echo "There is no supported 4G module ERROR!!!!!!!!!!"
fi
