#!/bin/sh

bitrate=250000
if [[ -n $2 ]]; then
  bitrate=$2
fi

index=0
if [[ -n $3 ]]; then
  index=$3
fi

start() {
  printf "Starting CAN${index} ${bitrate}: "
  ip link set can${index} up type can bitrate ${bitrate}
  echo "OK"
}
stop() {
  printf "Stopping CAN${index}: "
  ip link set can${index} down
  echo "OK"
}
restart() {
  stop
  start
}

case "$1" in
start)
  start
  ;;
stop)
  stop
  ;;
restart | reload)
  restart
  ;;
*)
  echo "Usage: $0 {start|stop|restart}"
  exit 1
  ;;
esac

exit $?
