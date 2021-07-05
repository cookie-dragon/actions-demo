#!/bin/sh

channel=1
if [[ -n $2 ]]; then
  channel=$2
fi

dev="hci0"
if [[ -n $3 ]]; then
  dev=$3
fi
boot() {
  echo -e "\nStarting Bluetooth..."
  bluetoothd
  hciconfig hci0 up
  sdptool add SP
  echo -e "\nStarting Bluetooth: OK"
}
start() {
  printf "Starting BT ${dev} Channel ${channel}: "
  rfcomm watch ${dev} ${channel} > /dev/null &
  echo "OK"
}
stop() {
  printf "Stopping BT ${dev} Channel ${channel}: "
  kill -9 `ps | grep "rfcomm watch ${dev} ${channel}" | grep -v "grep" | head -1 | awk '{printf $1}'`
  echo "OK"
}
pscan() {
	printf "Setting BT ${dev} pscan: "
	hciconfig ${dev} pscan
	echo "OK"
}
iscan() {
	printf "Setting BT ${dev} iscan: "
	hciconfig ${dev} iscan
	echo "OK"
}
piscan() {
	printf "Setting BT ${dev} piscan: "
	hciconfig ${dev} piscan
	echo "OK"
}
noscan() {
	printf "Setting BT ${dev} noscan: "
	hciconfig ${dev} noscan
	echo "OK"
}
restart() {
  stop
  start
}

case "$1" in
boot)
  boot
  ;;
start)
  start
  ;;
stop)
  stop
  ;;
restart | reload)
  restart
  ;;
pscan)
  pscan
  ;;
iscan)
  iscan
  ;;
piscan)
  piscan
  ;;
noscan)
  noscan
  ;;
*)
  echo "Usage: $0 {boot|start|stop|restart|pscan|iscan|piscan|noscan}"
  exit 1
  ;;
esac

exit $?
