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

echo Content-type: text/html
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

	varname=`echo $param | cut -f 1 -d = | urldecode`
	value=`echo $param | cut -f 2 -d =  | urldecode`
	case "$varname" in
		pc)
			pc="$value"
			mac=`getrec /pxe/etc/machines $pc`
			delrec /pxe/etc/machines $pc || true
			delrec /pxe/etc/pcstyle $pc || true
			delrec /pxe/etc/restorepath $pc || true
			delrec /pxe/etc/restorembr $pc || true
			delrec /pxe/etc/restoresf $pc || true
			delrec /pxe/etc/pcstatus $pc || true
			;;
	esac
done > /dev/null
echo 'busy();'
/pxe/bin/getpcicons.sh "default&async=0"
echo 'ready();'
exec /pxe/bin/getpcicons.sh "register&async=0" 1>&- &
