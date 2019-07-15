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

set +e

DAY=`date +%d | sed -r -e s/^0//`

while true ; do
	i=0
	one=
	while [ $i -lt 24 ] ; do
		i=`expr $i + 1`
		STATUS=`getrec /pxe/etc/pcstatus $i 2> /dev/null` || continue
		if [ "$STATUS" == "GM" ] ; then
			lanreboot.sh $i &
			one=1
		fi
	done
	[ -z "$one" ] && break
	sleep 10
done
