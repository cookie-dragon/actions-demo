#!/bin/sh

reset_root() {
	s_line=`cat /proc/cpuinfo | grep Serial`
	s=`echo ${s_line#*": "}`
	s_md5=`echo -n ${s}|md5sum |cut -d" " -f1`
	echo -e "${s_md5}\n${s_md5}" | passwd root >/dev/null
}

reset_user() {
	deluser user
	deluser admin

	mkdir -p /home

	adduser -g AdminUser -G root -D admin
	echo -e "ht@315800\nht@315800" | passwd admin >/dev/null

	adduser -g NormalUser -G users -D user
	echo -e "p@ssw0rd\np@ssw0rd" | passwd user >/dev/null

	/opt/sbin/sys_admin_totp_show
}

reset_host() {
	s_line=`cat /proc/cpuinfo | grep Serial`
	s=`echo ${s_line#*": "}`
	s4=${s:0-4}

	sed -i "1c htbox-${s4}" /etc/hostname
	sed -i "2c 127.0.1.1	htbox-${s4}" /etc/hosts
	sed -i "9c Name = htbox-${s4}" /etc/bluetooth/main.conf
	sed -i "5c ssid=htbox-${s4}" /etc/hostapd_wlan0.conf
	sync
}

reset_factory() {
	touch /media/factory/update
	/opt/sbin/sys_update factory
}

case "$1" in
*)
	rm -rf /etc/*+
	reset_host
	reset_root
	reset_user
	reset_factory
	;;
esac

exit 0
