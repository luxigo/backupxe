#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux, all rights reserved.
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

PXELINUXCFGDIR=/tftpboot/pxelinux/pxelinux.cfg/
. /pxe/etc/config


echo Content-Type: text/plain
echo Pragma: no-cache
echo

if [ -n "$QUERY_STRING" ] ; then

  MOVIE=`echo $QUERY_STRING | urldecode`

 #       for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
 #               [ -z "$param" ] && continue
 #               varname=`echo $param | cut -f 1 -d =`
 #               value=`echo $param | cut -f 2 -d =`
 #               case "$varname" in
 #                       mac) MAC=`echo $value | tr A-Z a-z | tr ':' '-'` ;;
 #                       *) MOVIE=$value ;;
 #               esac
 #       done
else
	exit 1
fi


if [ -f /tmp/dhcp.leases ] ; then
	MAC=`sed -r -n -e 's/:/-/g' -e 's/^.*(00\-[0-9a-f\-]+) '$REMOTE_ADDR' .*/\1/p' /tmp/dhcp.leases`
else
	MAC=`/usr/sbin/arp -an | sed -r -n -e 's/.*\('$REMOTE_ADDR'\)[^0-9]+([0-9a-zA-Z:]+).*/\1/p' | tr A-Z a-z | tr ':' '-'`
fi

[ -z "$MAC" ] && exit 1

set -x
old=`sed -r -n -e 's/^([0-9a-f\-]+) +CABINE'$MOVIE'$/\1/p' /pxe/etc/hosts.mac`
if [ -n "$old" ] && [ "$old" != "$MAC" ] ; then
	delrec /pxe/etc/hosts.mac $old
fi
setrec /pxe/etc/hosts.mac $MAC CABINE$MOVIE
cd $PXELINUXCFGDIR
ln -sf movies.d/film$MOVIE 01-$MAC
set +x

filename=`getrec /pxe/etc/movies $MOVIE`
[ -z "$filename" ] && exit 1
echo $filename
