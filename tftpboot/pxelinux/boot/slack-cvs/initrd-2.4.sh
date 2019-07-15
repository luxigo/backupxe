#!/bin/sh
set -e
set -x
echo --- creating image file...
SIZE=`du -s initrd.d | cut  -f  1`
dd if=/dev/zero of=initrd bs=1024 count=$(( ( ($SIZE/1024)+($SIZE/1024)/8 ) * 1024 ))
mkfs.ext2 -q -b 1024 initrd
mkdir -p /mnt/initrd 
(mount | grep -w /mnt/initrd) && (echo --- unmounting /mnt/initrd ; umount /mnt/initrd )
echo --- mounting image...
mount -o loop initrd /mnt/initrd
echo --- copying files...
cd initrd.d
tar cp . | tar xp -C /mnt/initrd
cd ..
df /mnt/initrd
echo --- unmounting...
umount /mnt/initrd
sync
echo --- compressing...
gzip -9 initrd
mv initrd.gz initrd.img
echo --- done
ls -l initrd.img
#./bootsplash.sh
