#!/bin/sh

sudo apt-get -y install qemu-user-static
cp /usr/bin/qemu-arm-static ./rootfs/usr/bin/
./ms.sh -m rootfs
./ms.sh -u rootfs
