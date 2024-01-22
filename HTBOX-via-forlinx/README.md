# htbox-forlinx

## 独立C文件编译
```
arm-linux-gnueabihf-gcc -o main main.c -lpthread
```

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

* 修改action内压缩模块的代码

### executable
* 更新dev/python_public_executable/executable内的文件（可执行文件）
* 更新dev/python_public_executable/executable-cython-build.sh内的可执行文件数组

* 修改action内ipk打包的代码，移动可执行文件到指定目录

### HtBoxMain
* 更新rootfs-ipk/HtBoxMain/data内的文件
* 根据功能修改rootfs-ipk/HtBoxMain/control/prerm内备份配置文件代码
* 根据重置包/更新包修改rootfs-ipk/HtBoxMain/control/postinst内的恢复配置文件代码
* 修改rootfs-ipk/HtBoxMain/control/control内的版本信息

## 文件系统说明

### /usr/bin/frpc
* frp 客户端
* -c 配置文件
* 默认配置文件 /etc/frp/frpc.ini
* 配置文件模板以及自启动程序 /usr/share/frpc

### /etc/boxid
固化的BoxID

### /etc/sysreset
* 系统重置标志文件，内容无意义
* 启动时检查到该文件则执行/opt/sbin/sys_reset

### /media/factory
* 系统初始化固件，用于系统恢复，由opt/sbin/sys_update控制

### /media/update
* 系统更新固件，用于系统更新，由opt/sbin/sys_update控制

### /opt/sbin/dev_bt
* 蓝牙控制程序
* Usage: $0 {boot|start|stop|restart|pscan|iscan|piscan|noscan} $channel $dev

### /opt/sbin/dev_can
* can控制程序
* Usage: $0 {start|stop|restart} $bitrate $index

### /opt/sbin/KeyMonitor
* 灯键控制程序
* 长按UserKey，执行/opt/sbin/sys_update factory

### /opt/sbin/sys_init
* 开机自启
* 暂无内容

### /opt/sbin/sys_reset
* 系统重置
* 重置root密码
* 重置admin密码并打印totp二维码
* 重置hostname、hosts、蓝牙名称、WiFi-AP名称
* 重置uboot、kernel、程序包

### /opt/sbin/sys_update
* 系统更新（支持TF卡更新）
* 默认更新/media/mmcblk0p1
* 其他更新需要加参数 factory或者update（对应恢复和在线更新）

## py编译的功能程序说明

### /opt/bin/box_set_vpn_cert
* openvpn配置及证书json转文件存储

### /opt/sbin/dev_led
* py灯控
* 现只有“更新”一种模式
* Usage: $0 --state [update|test]

### /opt/sbin/sys_admin_totp_chpwd
* totp密码修改

### /opt/sbin/sys_admin_totp_show
* totp二维码显示

### /opt/sbin/sys_mount_tools
* 专用tf卡创建/挂载
* Usage: $0 --cb [build|check] --auth [0|1|2|3|4]
* auth - 0:No Auth;1:Check Card Only;2:Check BOXID;3:Check Serial;4:Check All

## htbox软件包文件说明

### /opt/bin/box_init
* box网络环境主功能
* Usage: $0 [check] $config_file_path
* Usage: $0 [config|start|restart|reload|stop]
* 重新配置并重启：需要存在/etc/htbox/htbox.conf.tmp并手动check，否则则是原配置重启网络环境

### /opt/bin/defroute_monitor
* 默认路由监控程序

### /opt/bin/box_openvpn
* openvpn主操作程序
* Usage: $0 [start|stop|restart|status]
* Usage: $0 {getconfig} {urlheader compId id token}

### /opt/bin/box_reset
* box配置文件重置
* 当配置文件不存在时 - Usage: $0 [miss] 
* 单纯用def配置恢复时，不带参数

### /etc/htbox/htbox.conf.def
* 默认配置文件

### /etc/htbox/htbox.conf.sample
* 配置文件例子

## kernel
```
Networking support  --->
	Networking options  --->
		[*] TCP/IP networking
		[*]   IP: advanced router
		[*]     FIB TRIE statistics
		[*]     IP: policy routing
		[*]     IP: equal cost multipath
		[*]     IP: verbose route monitoring
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
		<*>   USB Gadget Support  --->
			<M>   USB Gadget Drivers
			<M>     Ethernet Gadget (with CDC Ethernet support)
			[*]       RNDIS support
			[*]       Ethernet Emulation Model (EEM) support
			<M>     Network Control Model (NCM) support
			<M>     Mass Storage Gadget
			<M>     Serial Gadget (with CDC ACM and CDC OBEX support)
			<M>     CDC Composite Device (Ethernet and ACM)
			<M>     CDC Composite Device (ACM and mass storage)
			<M>     HID Gadget
File systems  --->
	Network File Systems  --->
		<*>   NFS server support
		[*]     NFS server support for NFS version 3
		[*]       NFS server support for the NFSv3 ACL protocol extension
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
				[*] nfs-utils
			Hardware handling  --->
				[ ] i2c-tools
			Interpreter languages and scripting  --->
				[*] python3
					  core python3 modules  --->
					External python modules  --->
						[ ] python-htbox
						[*] python-pyotp
						[*] python-asyncua
						-*- python-aiofiles
						-*- python-aiosqlite
						-*- python-asn1crypto
						-*- python-babel
						[*] python-can
						-*- python-cffi
						-*- python-click
						-*- python-cryptography
						-*- python-dateutil
						-*- python-dnspython
						-*- python-flask
						[*] python-flask-cors
						[*] python-flask-babel
						[*] python-flask-jsonrpc
						[*] python-flask-login
						[*] python-flask-sqlalchemy
						[*] python-gunicorn
						-*- python-idna
						[*] python-ipy
						-*- python-itsdangerous
						-*- python-jinja2
						[*] python-lxml
						-*- python-markdown
						-*- python-markupsafe
						[*] python-paho-mqtt
						[*] python-pip
						-*- python-pycparser
						[*] python-pyqrcode
						-*- python-pytz
						[*] python-serial
						-*- python-setuptools
						-*- python-six
						[ ] python-smbus-cffi
						-*- python-sortedcontainers
						-*- python-sqlalchemy
						[*] python-websockets
						-*- python-werkzeug
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
				[ ]   sntp
				[ ]   ntp-keygen
				[ ]   SHM clock support
				[*]   ntpd
				[ ]     PPS support
				[ ]   ntpdate
				[ ]   ntpdc
				[ ]   ntpq
				[ ]   ntpsnmpd
				[ ]   ntptime
				[ ]   tickadj
				[*] openssh
				[*] openvpn
				[*]   LZ4 compression
				[*]   LZO compression
				[ ]   Optimize for small size
				[*] pppd
				[*]   overwrite /etc/resolv.conf
				[*] samba4
				[*]   AD DC
				-*-   ADS
				[*]   smbtorture
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
