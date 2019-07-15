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

set -e

echo Content-Type: text/html
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
			pc|machine) PC=$value ;;
                esac
		if [ -n "$PC" ] ; then
			machines="$machines $PC"
			PC=
		fi
        done
fi

PXECFGDIR=/tftpboot/pxelinux/pxelinux.cfg

for PC in $machines ; do
#	sed -r -e 's/volume=[0-9]+/volume='$VOL'/' $PXECFGDIR/movies.d/film$PC > /tmp/film$PC.$$.tmp && cat /tmp/film$PC.$$.tmp > $PXECFGDIR/movies.d/film$PC
#	rm /tmp/*.$$.tmp 2> /dev/null || true

	hwaddr=`getrec /pxe/etc/machines $PC || true`
	ip=`dhcplease $hwaddr || true`

	if [ -n "$ip" ] ; then
		STATUS=`getrec /pxe/etc/pcstatus $PC`
		case $STATUS in
			G*)
				wget --tries=1 --timeout=10 http://$ip/cgi-bin/mixer.cgi?vol=0 || true
			;;
		esac
	fi
done
