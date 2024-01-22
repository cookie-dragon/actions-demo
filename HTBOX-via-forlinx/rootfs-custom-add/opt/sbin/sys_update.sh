#!/bin/sh

MDEV=mmcblk0p1
if [[ -n $1 ]]; then
	MDEV=$1
fi

s_line=`cat /proc/cpuinfo | grep Serial`
s=`echo ${s_line#*": "}`

if [[ -f /media/$MDEV/update ]]; then

	if [[ -f /media/$MDEV/factory_card ]]; then
		fc=`cat /media/$MDEV/factory_card`
		if [[ $s == $fc ]]; then
			exit 0
		else
			echo $s > /media/$MDEV/factory_card
		fi
	else
		rm -rf /media/$MDEV/update
	fi

	echo "Updating..."

	# 停止HtBoxMain主程序
	if [[ -f /etc/init.d/S99HtBoxMainApp ]]; then
		/etc/init.d/S99HtBoxMainApp stop
	fi

	# 停止KeyMonitor灯键程序
	if [[ -f /etc/init.d/S98KeyMonitor ]]; then
		/etc/init.d/S98KeyMonitor stop
	fi

	# 开启LED
	/opt/sbin/dev_led --state=update >/dev/null &

	printf "Update Packages: "

	for file in `ls -a /media/$MDEV`
	do
		if [[ -f /media/$MDEV/$file ]]; then
			if [[ "${file##*.}"x = "ipk"x ]]; then
				cd /media/$MDEV
				if [[ -f /media/$MDEV/reset ]] || [[ -f /media/$MDEV/factory_card ]]; then
					opkg install $file --force-downgrade --force-reinstall
				else
					opkg install $file
				fi
			fi
		fi
	done

	echo "OK"

	if [[ ! -f /media/$MDEV/factory_card ]]; then

		if [[ -f /media/$MDEV/MLO ]]; then
			printf "Update MLO: "
			
			spl_mtdindex_line=`cat /proc/mtd | grep \"SPL\"`
	        spl_mtdindex=${spl_mtdindex_line%%:*}

	        spl_size_line=`mtd_debug info /dev/${spl_mtdindex} | grep mtd.size`
	        spl_size_line_l=`echo ${spl_size_line%% (*}`
	        spl_size=`echo ${spl_size_line_l#*= }`

	        spl_erasesize_line=`mtd_debug info /dev/${spl_mtdindex} | grep mtd.erasesize`
	        spl_erasesize_line_l=`echo ${spl_erasesize_line%% (*}`
	        spl_erasesize=`echo ${spl_erasesize_line_l#*= }`

	        spl_blockcnt=$[spl_size/spl_erasesize]

			flash_erase /dev/${spl_mtdindex} 0x0 ${spl_blockcnt}
			nandwrite -p /dev/${spl_mtdindex} /media/$MDEV/MLO

			echo "OK - "${spl_mtdindex}" blockcnt: "${spl_blockcnt}
		fi

		if [[ -f /media/$MDEV/u-boot.img ]]; then
			printf "Update u-boot.img: "

			uboot_mtdindex_line=`cat /proc/mtd | grep \"U-Boot\"`
			uboot_mtdindex=${uboot_mtdindex_line%%:*}

	        uboot_size_line=`mtd_debug info /dev/${uboot_mtdindex} | grep mtd.size`
	        uboot_size_line_l=`echo ${uboot_size_line%% (*}`
	        uboot_size=`echo ${uboot_size_line_l#*= }`

	        uboot_erasesize_line=`mtd_debug info /dev/${uboot_mtdindex} | grep mtd.erasesize`
	        uboot_erasesize_line_l=`echo ${uboot_erasesize_line%% (*}`
	        uboot_erasesize=`echo ${uboot_erasesize_line_l#*= }`

	        uboot_blockcnt=$[uboot_size/uboot_erasesize]

			flash_erase /dev/${uboot_mtdindex} 0x0 ${uboot_blockcnt}
			nandwrite -p /dev/${uboot_mtdindex} /media/$MDEV/u-boot.img

			echo "OK - "${uboot_mtdindex}" blockcnt: "${uboot_blockcnt}
		fi
		
		if [[ -f /media/$MDEV/uImage ]]; then
			printf "Update uImage: "

			kernel_mtdindex_line=`cat /proc/mtd | grep \"Kernel\"`
			kernel_mtdindex=${kernel_mtdindex_line%%:*}

	        kernel_size_line=`mtd_debug info /dev/${kernel_mtdindex} | grep mtd.size`
	        kernel_size_line_l=`echo ${kernel_size_line%% (*}`
	        kernel_size=`echo ${kernel_size_line_l#*= }`

	        kernel_erasesize_line=`mtd_debug info /dev/${kernel_mtdindex} | grep mtd.erasesize`
	        kernel_erasesize_line_l=`echo ${kernel_erasesize_line%% (*}`
	        kernel_erasesize=`echo ${kernel_erasesize_line_l#*= }`

	        kernel_blockcnt=$[kernel_size/kernel_erasesize]

			flash_erase /dev/${kernel_mtdindex} 0x0 ${kernel_blockcnt}
			nandwrite -p /dev/${kernel_mtdindex} /media/$MDEV/uImage

			echo "OK - "${kernel_mtdindex}" blockcnt: "${kernel_blockcnt}
		fi

		if [[ ! -f /media/$MDEV/reset ]]; then
			rm -rf /media/$MDEV/*.ipk
			rm -rf /media/$MDEV/MLO /media/$MDEV/u-boot.img /media/$MDEV/uImage
		fi
	fi

	if [[ -f /media/$MDEV/reset ]]; then
		rm -rf /media/$MDEV/factory_card
	fi

	echo "Rebooting..."
	reboot
fi
