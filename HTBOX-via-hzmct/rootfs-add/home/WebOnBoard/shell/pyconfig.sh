#!/bin/sh

case "$1" in
  start)
    echo -n "Starting WebOnBoard Config"
    cd /home/WebOnBoard
    python static_config2.py
    echo "."
    ;;
  *)
    echo "Usage: ./pyconfig.sh {start}"
    exit 1
esac