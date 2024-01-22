#!/bin/sh

reset_when_miss() {
	hostname=`cat /etc/hostname`
    sed -i "/htbox-undefined/c\"ssid\": \"${hostname}\"," /etc/htbox/htbox.conf.def
    sync
	cp -f /etc/htbox/htbox.conf.def /etc/htbox/htbox.conf
}

reset_config() {
	cp -f /etc/htbox/htbox.conf.def /etc/htbox/htbox.conf.tmp
	/opt/bin/box_init restart
}

case "$1" in
miss)
	reset_when_miss
	;;
*)
	reset_config
	;;
esac

exit 0
