#!/bin/sh

case "$1" in
  start)
    echo -n "Starting Mosquitto"
    mosquitto -c /etc/mosquitto/mosquitto.conf &
    echo "."
    ;;
  *)
    echo "Usage: ./mosquitto.sh {start}"
    exit 1
esac