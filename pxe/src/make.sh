#!/bin/sh 

set -e

CC=gcc
STRIP=strip

[ -z "$ARCH" ] && ARCH="$1"
[ -z "$ARCH" ] && ARCH=`uname -m`

case $ARCH in
  mips) PREFIX=mipsel-linux-
	if ! which mipsel-linux-gcc 2> /dev/null > /dev/null ; then
		. /usr/local/src/whiterussian/openwrt/setenv.sh
	fi
	;;
esac

for f in `ls -1 *.c` ; do
	name=`basename $f .c`
	cd /pxe/src
	set -x
	$PREFIX$CC $name.c -w -O3 -o ../bin/$ARCH/$name-$ARCH
	$PREFIX$STRIP ../bin/$ARCH/$name-$ARCH
	set +x
	cd ../bin/$ARCH
	ln -sf $name-$ARCH $name
done
