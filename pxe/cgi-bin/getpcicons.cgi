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

if [ -n "$QUERY_STRING" ] ; then
        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        async) ASYNC=$value ;;
                        register) page=register ;;
                        default) page=default ;;
                        reload) reload=1 ;;
                esac
        done
fi

cat /pxe/etc/pcicons.$page$reload

[ -f /var/run/pxe/getpcicons.pid ] && kill -0 `cat /var/run/pxe/getpcicons.pid` > /dev/null 2>&1 && exit 0

exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &

exit

############################
exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &
if [ ! -f /pxe/etc/pcicons.$page$reload ] || [ /pxe/etc/pcstyle -nt /pxe/etc/pcicons.$page$reload ] ; then
	touch /pxe/etc/pcicons.$page$reload
	getpcicons.sh "$QUERY_STRING&async=0"
fi

cat /pxe/etc/pcicons.$page$reload

[ -f /var/run/pxe/getpcicons.pid ] && kill -0 `cat /var/run/pxe/getpcicons.pid` > /dev/null 2>&1 && exit 0
exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &
