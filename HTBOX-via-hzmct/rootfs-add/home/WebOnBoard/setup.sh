#!/bin/sh

case "$1" in
  install)
    echo -n "Install WebOnBoard"

    find . -name "*.pyc" | xargs rm -rf

    python static_config2.py

    chmod +x ./openvpn.sh
    chmod +x ./static_config2.py
    chmod +x ./static_monitor.py

    chmod +x ./HtBoxMain
    chmod +x ./auto_start.sh

    rm -rf /etc/init.d/pyconfig.sh
    chmod +x ./shell/pyconfig.sh
    cp -rf ./shell/pyconfig.sh /etc/init.d/

    rm -rf /etc/rc5.d/S99pynet.sh
    rm -rf /etc/init.d/pynet.sh
    chmod +x ./shell/pynet.sh
    cp -rf ./shell/pynet.sh /etc/init.d/

    rm -rf ./shell

    cd /etc/rc5.d
    ln -s ../init.d/pynet.sh S99pynet.sh

    touch /etc/sysctl.conf

    echo "."
    ;;
  uninstall)
    echo -n "Uninstall WebOnBoard"
    rm -rf /etc/hostapd.conf
    rm -rf /etc/udhcpd*.conf
    rm -rf /etc/init.d/pyconfig.sh
    rm -rf /etc/rc5.d/S99pynet.sh
    rm -rf /etc/init.d/pynet.sh
    echo "."
    ;;
  *)
    echo "Usage: ./setup.sh {install|uninstall}"
    exit 1
esac