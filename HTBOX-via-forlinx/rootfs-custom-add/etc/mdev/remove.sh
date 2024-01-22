#!/bin/sh

mdir=${MDEV}
if [[ $MDEV == mmcblk[0-9] ]]; then
	mdir=${MDEV}p[0-9]
elif [[ $MDEV == sd[a-z] ]]; then
	mdir=${MDEV}[0-9]
fi

sync
umount -l /media/${mdir}
rm -rf /media/${mdir}
