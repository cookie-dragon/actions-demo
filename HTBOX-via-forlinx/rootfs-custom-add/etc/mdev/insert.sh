#!/bin/sh
if [[ -d /sys/block/*/$MDEV ]]; then
  /opt/sbin/sys_mount_tools
  if [[ $? -eq 0 ]]; then
    mkdir -p /media/$MDEV
    mount /dev/$MDEV /media/$MDEV 
  fi
fi
