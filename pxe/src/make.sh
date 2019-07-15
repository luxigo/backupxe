#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
