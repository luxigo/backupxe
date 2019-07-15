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
DAY=`date +%d | sed -r -e s/^0//`
DAY=25
i=1

set +e

while true; do

	one=0
	while [ $i -lt $DAY ] ; do
		hw=`getrec /pxe/etc/machines $i`
		i=`expr $i + 1`
		ip=`dhcplease $hw`
		[ -z "$ip" ] && continue
		setrec /pxe/etc/movie.pause $ip 0
		wget --timeout=10 --tries=2 http://$ip/cgi-bin/killmplayer.cgi -O /dev/null
		sleep 6

	done

	[ $one -eq 0 ] && break

done
