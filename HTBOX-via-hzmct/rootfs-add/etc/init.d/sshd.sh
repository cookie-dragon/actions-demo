#!/bin/sh

case "$1" in
	start)
		echo -n "Starting SSHD"
		/usr/local/sbin/sshd
		echo .
		;;
	*)
		echo "Uasges: ./sshd.sh {start}"
		exit 1
esac

