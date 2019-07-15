#!/bin/sh

URL=http://mirror.switch.ch/ftp/mirror/slackware/slackware-current
WORKDIR=`pwd`

if [ ! -f $WORKDIR/initrd.img.orig ] ; then
	echo downloading initrd
	wget -c $URL/isolinux/initrd.img -O initrd.img.orig.tmp || exit
	mv initrd.img.orig.tmp initrd.img.orig
fi

if [ ! -d $WORKDIR/initrd.d ] ; then
	echo extracting files from initrd
	gunzip initrd.img.orig -c > initrd.img || exit
	[ -d initrd.d.tmp ] && rmdir initrd.d.tmp
	mkdir initrd.d.tmp || exit
	cd initrd.d.tmp || exit 
	if file ../initrd.img | grep -q cpio ; then
		cat ../initrd.img | cpio -i -d -H newc --no-absolute-filenames
	else
		mkdir /tmp/mnt/initrd.$$ -p
		mount -o loop ../initrd.img /tmp/mnt/initrd.$$
		wd=`pwd`
		cd /tmp/mnt/initrd.$$
		tar cp . | tar xpv -C $wd
		cd $wd
		umount /tmp/mnt/initrd.$$
		rmdir /tmp/mnt/initrd.$$
	fi
	cd $WORKDIR
	mv initrd.d.tmp initrd.d
fi
