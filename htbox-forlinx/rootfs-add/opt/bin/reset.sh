#!/bin/sh

reset_password() {
	s_line=`cat /proc/cpuinfo | grep Serial`

	s=`echo ${s_line#*": "}`
	# echo root:${s}|chpasswd
	# echo "User 'root' password has changed! -> [${s}]"

	s_md5=`echo -n ${s}|md5sum |cut -d" " -f1`
	echo root:${s_md5}|chpasswd
	# echo "User 'root' password has changed! -> [${s_md5}]"
}

reset_user() {
	deluser user
	deluser admin
	delgroup admin

	addgroup -S admin

  mkdir -p /home

	adduser -g AdminUser -G admin -S -D -H admin
	echo admin:ht@315800|chpasswd

	adduser -g NormalUser -G users -D user
	echo user:p@ssw0rd|chpasswd
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
	reset_config
	;;
esac
