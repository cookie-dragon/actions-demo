#!/bin/sh

reset_password() {
	s_line=`cat /proc/cpuinfo | grep Serial`
	s=`echo ${s_line#*": "}`
	s_md5=`echo -n ${s}|md5sum |cut -d" " -f1`
	echo -e "${s_md5}\n${s_md5}" | passwd root
	echo "User 'root' password has changed! -> [${s_md5}]"
}

reset_user() {
	deluser user
	deluser admin

	mkdir -p /home

	adduser -g AdminUser -G root -D admin
	echo -e "ht@315800\nht@315800" | passwd admin

	adduser -g NormalUser -G users -D user
	echo -e "p@ssw0rd\np@ssw0rd" | passwd user
}

reset_config() {
	cp -f /etc/htbox/htbox.conf.def /etc/htbox/htbox.conf.tmp
	python /etc/init.d/S33htbox.py restart
}

case "$1" in
password)
	reset_password
	;;
user)
	reset_user
	;;
config)
	reset_config
	;;
*)
	reset_password
	reset_user
	;;
esac
