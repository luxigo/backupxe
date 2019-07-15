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

i=0

while [ $i -lt 24 ] ; do
	i=`expr $i + 1`
	PAUSE=`getrec /pxe/etc/movie.pause $i`
	[ "$PAUSE" = "1" ] && continue
	hw=`getrec /pxe/etc/machines $i`
	ip=`dhcplease $hw`
	[ -z "$ip" ] && continue
	setrec /pxe/etc/movie.pause $ip 1
	if [ $i -le $DAY ] ; then
		wget --timeout=10 --tries=1 http://$ip/cgi-bin/killmplayer.cgi -O /dev/null
	fi

done
