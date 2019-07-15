#!/bin/sh
set -e
echo --- copying files...
cd initrd.d
find . | cpio -o -H newc | gzip -9 > ../initrd.tmp || exit
cd ..
mv initrd.tmp initrd.img
echo --- done
ls -l initrd.img
#./bootsplash.sh
