#!/bin/sh
if [ -d /sys/block/*/$MDEV ]; then
  if [[ $MDEV == mmcblk[0-9]p[0-9] ]]; then
    /opt/sbin/sys_mount_tools
    if [[ $? -eq 0 ]]; then
      mkdir -p /media/$MDEV
      mount /dev/$MDEV /media/$MDEV 
    fi
  elif [[ $MDEV == sd[a-z][0-9] ]]; then
    mkdir -p /media/$MDEV
    mount /dev/$MDEV /media/$MDEV 
  fi
fi
