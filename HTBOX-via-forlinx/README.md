# htbox-forlinx

## 软件版本更新操作

### htbox
* 更新dev/python_pkg/htbox-dev内的文件，包括htbox包内文件以及包外的依赖htbox的可执行文件
* 更新dev/python_pkg/htbox-dev-cython-build.sh内的可执行文件数组
* 修改buildroot-add/package/python-htbox/htbox/setup.py的版本号
* 修改buildroot-add/package/python-htbox/python-htbox.mk内的版本号及路径
* 更新rootfs-ipk/htbox/data内的文件
* 根据功能修改rootfs-ipk/htbox/control/prerm内备份配置文件代码
* 根据重置包/更新包修改rootfs-ipk/htbox/control/postinst内的恢复配置文件代码
* 修改rootfs-ipk/htbox/control/control内的版本信息

### executable
* 更新dev/python_public_executable/executable内的文件（可执行文件）
* 更新dev/python_public_executable/executable-cython-build.sh内的可执行文件数组
* 修改action内压缩模块的代码

### HtBoxMain
* 更新rootfs-ipk/HtBoxMain/data内的文件
* 根据功能修改rootfs-ipk/HtBoxMain/control/prerm内备份配置文件代码
* 根据重置包/更新包修改rootfs-ipk/HtBoxMain/control/postinst内的恢复配置文件代码
* 修改rootfs-ipk/HtBoxMain/control/control内的版本信息

## kernel
```
Networking support  --->
	Networking options  --->
		[*]   IP: advanced router
		[*]     IP: policy routing
		[*] Network packet filtering framework (Netfilter)  --->
			      Core Netfilter Configuration  --->
				      <*> Netfilter connection tracking support
				      <*>   NetBIOS name service protocol support
				      -*- Netfilter Xtables support (required for ip_tables)
			      IP: Netfilter Configuration  --->
				      <*> IPv4 connection tracking support (required for NAT)
				      <*> IP tables support (required for filtering/masq/NAT)
				      <*>   Full NAT
				      <*>     MASQUERADE target support
				      <*>     REDIRECT target support
		<*> 802.1d Ethernet Bridging
	Bluetooth subsystem support  --->
		[*]   L2CAP protocol support
		[*]   SCO links support
		<*>   RFCOMM protocol support
		[*]     RFCOMM TTY support
		<*>   BNEP protocol support
		[*]     Multicast filter support
		[*]     Protocol filter support
		<*>   HIDP protocol support
		      Bluetooth device drivers  --->
		    	<*> RTK HCI USB driver
	Wireless  --->
		<*>   cfg80211 - wireless configuration API
		<*>   Generic IEEE 802.11 Networking Stack (mac80211)
	<*>   RF switch subsystem support
Device Drivers  --->
	Generic Driver Options  --->
		-*- Userspace firmware loading support
		[*]   Include in-kernel firmware blobs in kernel binary
	Network device support  --->
		<*>     Universal TUN/TAP device driver support
		<*>   PPP (point-to-point protocol) support
			<*>     PPP BSD-Compress compression
			<*>     PPP Deflate compression
			[*]     PPP filtering
			<*>     PPP MPPE compression (encryption) (EXPERIMENTAL)
			[*]     PPP multilink support (EXPERIMENTAL)
			<*>     PPP over Ethernet (EXPERIMENTAL)
			<M>     PPP on L2TP Access Concentrator
			<M>     PPP on PPTP Network Server
			<*>     PPP support for async serial ports
			<*>     PPP support for sync tty ports
		      USB Network Adapters  --->
						<*> Multi-purpose USB Networking Framework
						<*>   Host for RNDIS and ActiveSync devices
		[*]   Wireless LAN  --->
			<*>   IEEE 802.11 for Host AP (Prism2/2.5/3 and WEP/TKIP/CCMP)
			<*>   Realtek wifi  --->
				<*>   select wifi type (Realtek 8723D USB WiFi)
	Input device support  --->
		Miscellaneous devices  --->
			<*>   User level driver support
	USB support  --->
		-*-   Support for Host-side USB
		<*>   EHCI HCD (USB 2.0) support
		<*>   OHCI HCD support
		<*>   USB Mass Storage support
		<*>   USB Serial Converter support  --->
			<*>   USB driver for GSM and CDMA modems
```

## buildroot
```
	Target options  --->
			Target Architecture (ARM (little endian))
			Target Architecture Variant (cortex-A8)
			Target ABI (EABIhf)
    Build options  --->
		($(TOPDIR)/../dl) Download dir
			libraries (shared only)  --->
    Toolchain  --->
			Toolchain type (External toolchain)  --->
			Toolchain (Custom toolchain)  --->
			Toolchain origin (Pre-installed toolchain)  --->
		()  Toolchain path
		($(ARCH)-linux) Toolchain prefix
			External toolchain gcc version (4.7.x)  --->
			External toolchain kernel headers series (3.2.x)  --->
			External toolchain C library (glibc/eglibc)  --->
		[*] Toolchain has SSP support?
		[*] Toolchain has RPC support?
		[*] Toolchain has C++ support?
	System configuration  --->
		(htbox-undefined) System hostname
		(Welcome to HT-BOX) System banner
			/dev management (Dynamic using devtmpfs + mdev)  --->
		[*] Enable root login with password
		()    Root password
			/bin/sh (bash)  --->
		[*] Run a getty (login prompt) after boot  --->
			(ttyO0) TTY port
		(eth0) Network interface to configure through DHCP
		(/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/opt/bin:/opt/sbin) Set the system's default PATH
	Target packages  --->
		[*]   Show packages that are also provided by busybox
			Compressors and decompressors  --->
				[*] gzip
			Development tools  --->
				[*] jq
			Filesystem and flash utilities  --->
				[*] mtd, jffs2 and ubi/ubifs tools
			Hardware handling  --->
				[ ] i2c-tools
			Interpreter languages and scripting  --->
				[*] python3
					  core python3 modules  --->
					External python modules  --->
						[ ] python-htbox
						[*] python-pyotp
						[*] python-can
						[*] python-cffi
						[*] python-ipy
						[*] python-lxml
						[*] python-pip
						-*- python-pycparser
						[*] python-pyqrcode
						[*] python-serial
						-*- python-setuptools
						[ ] python-smbus-cffi
						-*- python-wrapt
			Libraries  --->
				Database  --->
					[*] redis
				Graphics
					[*] libqrencode
					[*]   libqrencode tools
				JSON/XML  --->
					[*] cJSON
				Networking  --->
					[*] libcurl
					[*]   curl binary
					[*] libmodbus
					[*] libsocketcan
					[*] paho-mqtt-c
			Networking applications  --->
				[*] bluez-tools
				[*] bluez-utils
				[*] bridge-utils
				[*] can-utils
				[ ] hostapd
				[*] iperf3
				[*] iproute2
				[*] iptables
				[*] mosquitto
				[*] net-tools
				[*] nginx  --->
				[*] ntp
				[*] openssh
				[*] openvpn
				[*] pppd
				[*] wget
				[ ] wireless tools
				[ ] wpa_supplicant
			Package managers  --->
				[*] opkg
				[*]   gnupg support
				[*] rpm
			Shell and utilities  --->
				[*] sudo
```

## busybox
```
	Settings  --->
		[*]   vi-style line editing commands
		[*]     Username completion
		[*]   Fancy shell prompts
	Archival Utilities  --->
		[*] Make tar, rpm, modprobe etc understand .xz data
		[*] Make tar, rpm, modprobe etc understand .lzma data
		[*] Make tar, rpm, modprobe etc understand .bz2 data
		[*] Make tar, rpm, modprobe etc understand .gz data
		[*] Make tar, rpm, modprobe etc understand .Z data
	Linux Module Utilities  --->
		[*] depmod
	Networking Utilities  --->
		[*] udhcpd
```
