#!/bin/sh

set -e

WORKDIR=`pwd`
echo $WORKDIR

[ -z "$KVERSION" ] && KVERSION="$1"
[ -z "$KVERSION" ] && KVERSION=`( ls -1d linux-* 2>/dev/null || true ) | tail -n 1 | sed -r -e 's/.*-([0-9\.]+).*/\1/' -e 's/\.$//'` || exit

mkdir -p $WORKDIR/initrd.d/mnt/boot

export ROOT=$WORKDIR/initrd.d
export PATH=/pxe/bin:$PATH
netinstallpkg `cat $WORKDIR/packages.list` 2> $ROOT/tmp/netinstallpkg.log
rm $ROOT/usr/doc -r
rm $ROOT/usr/man -r
rm $ROOT/usr/include -r


cp $WORKDIR/System.map $WORKDIR/initrd.d/mnt/boot

cd $WORKDIR/common/initrd_overlay || exit 
tar cp --exclude ./tmp . | tar xpv -C $WORKDIR/initrd.d


cd $WORKDIR/initrd_overlay || exit 
tar cp --exclude ./tmp . | tar xpv -C $WORKDIR/initrd.d

if [ -n "$KVERSION" ] ; then
	for d in $WORKDIR/initrd.d/lib/modules/* ; do
		if [ "`basename $d`" != "$KVERSION" ] ; then
			rm "$d" -r || true
		fi
	done
fi

[ "$USER" = "root" ] && chmod a+rwx /tmp
