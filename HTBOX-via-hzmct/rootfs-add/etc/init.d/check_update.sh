#!/bin/sh
while [ 1 ]; do
  if [ -f "/media/card/htbox_update.tar.gz" ]; then
    if [ -d "/home/WebOnBoard" ]; then

      # 备份
      if [ -f "/home/WebOnBoard/config.json" ]; then
        cp /home/WebOnBoard/config.json /home/
      fi
      if [ -f "/home/WebOnBoard/nodes_config.json" ]; then
        cp /home/WebOnBoard/nodes_config.json /home/
      fi
      cp /home/WebOnBoard/identifier.sqlite /home/
      cp -r /home/WebOnBoard/Log /home/

      # 删除
      rm -rf /home/WebOnBoard
    fi

    # 解压
    cd /home
    mv /media/card/htbox_update.tar.gz /home/
    dd if=htbox_update.tar.gz | openssl des3 -d -k ht@315800 | tar zxf -
    rm htbox_update.tar.gz
    chown -R root:root WebOnBoard/
    chmod 750 WebOnBoard/

    # 恢复
    if [ -f "/home/config.json" ]; then
      mv /home/config.json /home/WebOnBoard/
    fi
    if [ -f "/home/nodes_config.json" ]; then
      mv /home/nodes_config.json /home/WebOnBoard/
    fi
    if [ -f "/home/identifier.sqlite" ]; then
      mv /home/identifier.sqlite /home/WebOnBoard/
    fi
    if [ -d "/home/Log" ]; then
      mv /home/Log/* /home/WebOnBoard/Log/
      rm -rf /home/Log
    fi

    # 初始化
    cd /home/WebOnBoard
    sh setup.sh install

    # autorun
    cd /home/WebOnBoard
    if [ -f "/home/WebOnBoard/autorun.sh" ]; then
      sh /home/WebOnBoard/autorun.sh
      rm /home/WebOnBoard/autorun.sh
    fi

    # reboot
    reboot
    break
  fi
  sleep 5
done
