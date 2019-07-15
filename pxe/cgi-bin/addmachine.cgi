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

. /pxe/etc/config

set -e

echo Content-type: text/html
echo

echo addmachine_ok=false;

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        pc) pc=$value ;;
                        name) name=$value ;;
                esac
        done
fi

hwaddr=`(egrep \ $name\$ /pxe/etc/hosts.mac || true) | cut -f 1 -d ' '`
if [ `echo $hwaddr | wc -l` -gt 1 ] ; then
	echo "alert(\"error: duplicate machine name ! '$name': '$hwaddr>\");"
	exit 0
fi

if [ -z "$hwaddr" ] ; then
	name2=`getrec /pxe/etc/hosts.mac $name` || true
	if [ -n "$name2" ] ; then
		hwaddr=$name
	else
		echo "alert('error: cannot guess hardware address ($name) ($hwaddr) !');"
		exit 0
	fi
fi

if egrep -q "$hwaddr\$" /pxe/etc/machines ; then
	echo "alert('$name existe deja ! ($name=pc"`egrep "$hwaddr\$"  /pxe/etc/machines | cut -f 1 -d ' '`")');"
	exit 0
fi

if ! getrec /pxe/etc/machines $pc > /dev/null 2> /dev/null ; then
	echo $pc $hwaddr >> /pxe/etc/machines
	if ! getrec /pxe/etc/pcstyle $pc > /dev/null 2> /dev/null ; then
		echo "$pc left: 750px; top: 120px;" >> /pxe/etc/pcstyle
	fi

else
	existingmac=`getrec /pxe/etc/machines $pc || true`
	existingname=`getrec /pxe/etc/hosts.mac $existingmac || true`
	echo "alert('pc$pc existe deja ! (pc$pc=$existingname)');"
	exit 0
fi

echo addmachine_ok=true;

montage.sh $pc

exec /pxe/bin/getpcicons.sh "default&async=0" 1>&- &
