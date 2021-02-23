#!/bin/sh

MDEV=$1

if [[ -f /media/$MDEV/update ]]; then
	echo "Updating..."
	if [[ -f /media/$MDEV/rm.list ]]; then
		echo "Remove Files"
		cat /media/$MDEV/rm.list | xargs rm -rf
	fi
	if [[ -d /media/$MDEV/rootfs ]]; then
		echo "Replace Root File System"
		cp -rf /media/$MDEV/rootfs/* /
	fi

	if [[ -d /media/$MDEV/python_pkg ]]; then
		echo "Update Python Packages"
	fi

	if [[ -f /media/$MDEV/MLO ]]; then
		echo "Update MLO"
	fi
	if [[ -f /media/$MDEV/u-boot.img ]]; then
		echo "Update u-boot.img"
	fi
	if [[ -f /media/$MDEV/uImage ]]; then
		echo "Update uImage"
	fi
fi