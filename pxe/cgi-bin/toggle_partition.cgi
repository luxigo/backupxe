#!/bin/bash
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
                	what) what=$value ;;
                        pc) pc=$value ;;
                        partition) partition=$value ;;
                        enable) enable=$value ;;
                esac
        done
fi

[ -z "$pc" ] && exit 1
[ -z "$partition" ] && exit 1
[ -z "$enable" ] && exit 1

disk=`echo $partition | sed -r -n -e 's#^/dev/([a-z]+).*#\1#p'`

mac=`getrec /pxe/etc/machines $pc`
[ -z "$mac" ] && exit 1

case "$what" in
	save)
		if [ "$enable" = "1" ] ; then
			sed -r -e s#^\\\#$partition\$#$partition# /pxe/image/$mac/$disk/partitions.save > /tmp/partitions.save.$$.tmp && cat /tmp/partitions.save.$$.tmp > /pxe/image/$mac/$disk/partitions.save
		else
			sed -r -e s#^$partition\$#\\\#$partition# /pxe/image/$mac/$disk/partitions.save > /tmp/partitions.save.$$.tmp && cat /tmp/partitions.save.$$.tmp > /pxe/image/$mac/$disk/partitions.save
		fi
		rm /tmp/partitions.save.$$.tmp
		;;
	restore)
		if [ ! -f /pxe/image/$mac/$disk/partitions.restore ] ; then
		    cp -a /pxe/image/$mac/$disk/partitions.save /pxe/image/$mac/$disk/partitions.restore || exit 1
		fi
		if [ "$enable" = "1" ] ; then
			sed -r -e s#^\\\#$partition\$#$partition# /pxe/image/$mac/$disk/partitions.restore > /tmp/partitions.restore.$$.tmp && cat /tmp/partitions.restore.$$.tmp > /pxe/image/$mac/$disk/partitions.restore
		else
			sed -r -e s#^$partition\$#\\\#$partition# /pxe/image/$mac/$disk/partitions.restore > /tmp/partitions.restore.$$.tmp && cat /tmp/partitions.restore.$$.tmp > /pxe/image/$mac/$disk/partitions.restore
		fi
		rm /tmp/partitions.restore.$$.tmp
		;;
esac
