#!/bin/sh

DEBUG=

if [ -n "$DEBUG" ] ;	then
	set -x
fi

VER=`ls -1 initrd-2.*.sh | sed -r -n -e 's/.*([0-9]+.[0-9]+).*/\1/p'` 2> /dev/null
[ -z "$VER" ] && VER=2.6

URL=ftp://ftp.kernel.org/pub/linux/kernel/v$VER
WORKDIR=`pwd`
KVERSION=$1
[ -z "$KVERSION" ] && KVERSION=`( ls -1d linux-* || true ) | tail -n 1 | sed -r -e 's/.*-([0-9\.]+).*/\1/' -e 's/\.$//'`
echo $KVERSION

PROCS=`( cat /proc/cpuinfo | grep processor | wc -l ) || echo 1`
JOBS=-j`expr $PROCS + 1`

if [ -z "$KVERSION" ] ; then
	wget $URL/ -O _index.html
	KVERSION=`sed -r -n -e 's/.*LATEST-IS-([0-9\.]+).*/\1/p' _index.html | tail -n 1`
	[ -z "$KVERSION" ] && exit 1
	rm _index.html
fi

VER=`echo $KVERSION | sed -r -n -e 's/^([0-9]\.[0-9]+).*/\1/p'`

cd $WORKDIR

if [ ! -d linux-$KVERSION ] && [ ! -f linux-$KVERSION.tar.bz2 ] ; then
	wget -c $URL/linux-$KVERSION.tar.bz2 -O linux-$KVERSION.tar.bz2.tmp || exit
	mv linux-$KVERSION.tar.bz2.tmp linux-$KVERSION.tar.bz2
fi

if [ ! -d linux-$KVERSION ] || [ -f linux-$KVERSION.tar.bz2 ] ; then
	tar -jxvf linux-$KVERSION.tar.bz2 || exit
	rm linux-$KVERSION.tar.bz2
	
fi

if [ ! -f linux-$KVERSION/.config ] && [ ! -f linux-$KVERSION/.config.old ] ; then
	if [ -f config ] ; then
		cp config linux-$KVERSION/.config
	else
		wget http://mirror.switch.ch/ftp/mirror/slackware/slackware-current/kernels/huge.s/config -O linux-$KVERSION/.config.tmp || exit
		mv linux-$KVERSION/.config.tmp linux-$KVERSION/.config.old
	fi
	touch linux-$KVERSION/_oldconfig_
fi

cd linux-$KVERSION || exit

if [ -f _oldconfig_ ] ; then
	make oldconfig || exit
	rm _oldconfig_
	make menuconfig || exit
	[ -f $WORKDIR/config ] && mv $WORKDIR/config $WORKDIR/config.bak
	cp .config ../config

	[ -f $WORKDIR/bzImage ] && mv $WORKDIR/bzImage $WORKDIR/bzImage.bak
	[ -f $WORKDIR/vmlinuz ] && mv $WORKDIR/vmlinuz $WORKDIR/vmlinuz.bak
	[ -f $WORKDIR/System.map ] && mv $WORKDIR/System.map $WORKDIR/System.map.bak
fi

if [ ! -f $WORKDIR/vmlinuz ] && [ ! -f $WORKDIR/bzImage ] ; then
	case $VER in
		2.4)
			make dep || exit
			make $JOBS bzImage || exit
			make $JOBS modules || exit 
			cp arch/i386/boot/bzImage $WORKDIR/vmlinuz
			;;
		2.6)
			make $JOBS || exit
			cp arch/i386/boot/bzImage $WORKDIR/bzImage
			;;
	esac
	
	cd $WORKDIR

	cp linux-$KVERSION/System.map System.map
	
	mkdir -p initrd_overlay/mnt/boot/
	cp System.map config initrd_overlay/mnt/boot/ || exit

	[ -f $WORKDIR/modules/$KVERSION.bak ] && rm $WORKDIR/modules/$KVERSION.bak -r
	[ -d $WORKDIR/modules/$KVERSION ] && mv $WORKDIR/modules/$KVERSION $WORKDIR/modules/$KVERSION.bak
fi

if [ ! -f $WORKDIR/modules/$KVERSION ] ; then

	cd $WORKDIR/linux-$KVERSION
	INSTALL_MOD_PATH=$WORKDIR/modules.$$.tmp make modules_install || exit

	mkdir $WORKDIR/modules -p || exit
	[ -d "$WORKDIR/modules/$KVERSION" ] && rm $WORKDIR/modules/$KVERSION -r
	mv $WORKDIR/modules.$$.tmp/lib/modules/$KVERSION $WORKDIR/modules || exit
	rm $WORKDIR/modules.$$.tmp -r

fi

if [ true ] ; then

	cd $WORKDIR/modules || exit

	case "$VER" in
	2.4)
		# replace links
		suff=o
		cd  $KVERSION/pcmcia
		for f in *.o ; do
		  [ -z "$f" ] && continue
		  ln -sf `ls -l $f | sed -r -n -e 's/.*(\.\.\/kernel.*)/\1.gz/p'` . && rm "$f"
		done
		cd ../..

		;;
	2.6)
		suff=ko
		;;
	esac

	for f in `find $KVERSION/ -name *.$suff || true` ; do
	  gzip -9 "$f"
	done
	
fi

if [ true ] ; then
	cd $WORKDIR/modules || exit
	case "$VER" in
		2.4) suff=o ;;
		2.6) suff=ko ;;
	esac
	[ ! -d $WORKDIR/initrd_overlay/lib/modules/$KVERSION ] && cp -a `ls -1d $WORKDIR/initrd_overlay/lib/modules/?.* | tail -n 1`  $WORKDIR/initrd_overlay/lib/modules/$KVERSION
	for f in `find $WORKDIR/initrd_overlay/lib/modules/$KVERSION/ -name *.$suff.gz` ; do
	  mod=`echo $f | sed -r -n -e 's/.*('$KVERSION'\/.*)/\1/p'`
	  if [ -f $mod ] ; then
	    echo $f
	    cp -a $mod $f
	  else
	    rm $f && echo removed: $f
	  fi
	done
fi
