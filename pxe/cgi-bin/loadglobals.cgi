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

. /pxe/etc/config

echo Content-type: text/javascript
echo Pragma: no-cache
echo Connection: close
echo

cat /pxe/etc/globals*

[ -f /var/run/pxe/loadglobals.pid ] && kill -0 `cat /var/run/pxe/loadglobals.pid` > /dev/null 2>&1 || exec /pxe/bin/loadglobals.sh "async=1" 1>&- &


exit

what=0
ASYNC=0

[ -z "$QUERY_STRING" ] && QUERY_STRING=$1

if [ -n "$QUERY_STRING" ] ; then
	for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
		[ -z "$param" ] && continue
		varname=`echo $param | cut -f 1 -d =`
		value=`echo $param | cut -f 2 -d =`
		case "$varname" in
			async) ASYNC=$value ;;
		esac
        done
fi

echo Content-type: text/javascript
echo Pragma: no-cache
echo

IMAGEDIR=/pxe/image
PCSTYLE=/pxe/etc/pcstyle
MACHINES=/pxe/etc/machines
HOSTSMAC=/pxe/etc/hosts.mac
LEASES=`cat /pxe/etc/leases` || true

DONE=0

#while true ; do
#	if [ $MACHINES -nt /pxe/etc/globals.pcname ] || \
#	   [ $HOSTSMAC -nt /pxe/etc/globals.hostsmac ] || \
#	   [ /tftpboot/pxelinux/pxelinux.cfg -nt /pxe/etc/globals.all ] || \
#	   [ /pxe/etc/restorepath -nt /pxe/etc/globals.all ] || \
#	   [ /pxe/etc/savepath -nt /pxe/etc/globals.all ]  || \
#	   ( [ -n "$LEASES" ] && [ "$LEASES" -nt /pxe/etc/globals ] ) || \
#	   [ /pxe/etc/boottime -nt /pxe/etc/globals ] || \
#	   [ /pxe/etc/uptimelog -nt /pxe/etc/globals ] ; then
#
#		if [ -f /var/run/pxe/loadglobals.pid ] ; then
#			if kill -0 `cat /var/run/pxe/loadglobals.pid` > /dev/null 2>&1 ; then
#				sleep 1
#				continue
#			fi
#		fi
#
#		/pxe/bin/loadglobals.sh "$QUERY_STRING&async=0"
#
#	fi

	cat /pxe/etc/globals*

	[ -f /var/run/pxe/loadglobals.pid ] && kill -0 `cat /var/run/pxe/loadglobals.pid` > /dev/null 2>&1 || exec /pxe/bin/loadglobals.sh "async=1" 1>&- &
	break

#done
