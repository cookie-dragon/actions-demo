```
wget https://developer.arm.com/-/media/Files/downloads/gnu-a/8.3-2019.03/binrel/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz
tar xf gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz
mv gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf toolchain
cd toolchain
export TOOLCHAIN=`pwd`
export PREFIX=arm-linux-gnueabihf
export CROSS_COMPILE=${PREFIX}-
export PATH=${TOOLCHAIN}/bin:$PATH
```

```
wget https://software-dl.ti.com/processor-sdk-linux/esd/AM335X/latest/exports/am335x-evm-linux-sdk-src-06.03.00.106.tar.xz
tar xf am335x-evm-linux-sdk-src-06.03.00.106.tar.xz
```

```
cd board-support/u-boot-2019.01+gitAUTOINC+333c3e72d3-g333c3e72d3

cp -rf /Users/cooky/Documents/Project/InCtrl/Private/GitHubCtrl/actions-demo/htbox-ti/uboot-add/* ./
make CROSS_COMPILE=${CROSS_COMPILE} distclean
rm -rf ./am335x_htbox
make CROSS_COMPILE=${CROSS_COMPILE} O=am335x_htbox am335x_evm_defconfig
make -j$(nproc) CROSS_COMPILE=${CROSS_COMPILE} O=am335x_htbox

cp -rf am335x_htbox/MLO /Users/cooky/Documents/output
cp -rf am335x_htbox/u-boot.img /Users/cooky/Documents/output

```

```
cd board-support/linux-4.19.94+gitAUTOINC+be5389fd85-gbe5389fd85

cp -rf /Users/cooky/Documents/Project/InCtrl/Private/GitHubCtrl/actions-demo/htbox-ti/kernel-add/* ./
make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} distclean
make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} tisdk_am335x-evm_defconfig
make -j$(nproc) ARCH=arm CROSS_COMPILE=${CROSS_COMPILE}

make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} zImage
make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} am335x-htbox.dtb
make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} am335x-ok335xd.dtb
make ARCH=arm CROSS_COMPILE=${CROSS_COMPILE} modules
sudo make ARCH=arm INSTALL_MOD_PATH=<path to root of file system> modules_install

cp -rf arch/arm/boot/zImage /Users/cooky/Documents/output
cp -rf arch/arm/boot/dts/am335x-htbox.dtb /Users/cooky/Documents/output
cp -rf arch/arm/boot/dts/am335x-ok335xd.dtb /Users/cooky/Documents/output

```


```
sudo ./create-sdcard.sh

Enter Device Number or n to exit: 1
Number of partitions needed [2/3] : 2

Enter path for Boot Partition : 
/home/cooky/prebuilt-images/

Enter path for kernel image and device tree files : 
/home/cooky/prebuilt-images/

Enter path for Rootfs Partition : 
/home/cooky/rootfs.tar.xz
```