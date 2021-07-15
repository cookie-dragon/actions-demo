#!/bin/sh

case "$1" in
  start)
    echo -n "Starting WebOnBoard"
    cd /home/WebOnBoard
    python static_start2.py
    echo "."
    ;;
  *)
    echo "Usage: ./pynet.sh {start}"
    exit 1
esac