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

exit 1
. /pxe/etc/config

set -e

echo Content-type: text/html
echo

echo '<html><body>'
#echo "$0 $@"

if [ -n "$QUERY_STRING" ] ; then

	count=0
        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

                [ -z "$param" ] && continue

		if [ $count -eq 0 ] ; then
			debug=$param
			if [ "$debug" == 1 ] ; then
				echo "export DEBUG=1" > /pxe/etc/debug
				echo "set -x" >> /pxe/etc/debug
			else
				echo "export DEBUG=" > /pxe/etc/debug
				echo "set +x" >> /pxe/etc/debug
			fi
			break
			;;
                fi
        done
fi

echo '</body></html>'
