#!/bin/sh
package="HtBoxMain-0.1"

pwd=`pwd`

cd $pwd
rm -rf $pwd/control.tar.gz
cd $pwd/control
chmod +x postinst postrm preinst prerm
tar zcvf ../control.tar.gz ./*

cd $pwd
rm -rf $pwd/data.tar.gz
cd $pwd/data
tar zcvf ../data.tar.gz ./*

cd $pwd
rm -rf $pwd/*.ipk
tar zcvf $package.tar.gz control.tar.gz data.tar.gz debian-binary
mv $package.tar.gz ${package}.ipk

rm -rf control.tar.gz data.tar.gz

# opkg print-architecture
# opkg install ${package}.ipk
# opkg list
# opkg remove $package
