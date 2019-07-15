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
                	what)
                		what=$value
                		;;
                	pc)
                		pc=$value
                		;;

                esac
        done
fi

echo "partition$what[$pc]=new Array;"
mac=`getrec /pxe/etc/machines $pc`
/pxe/bin/partlist.sh $what $mac | sed -r -n -e 's/^#(.*)/partition'$what'['$pc'].push(new Array("\1",0));/p' -e t -e 's/.*/partition'$what'['$pc'].push(new Array(\"\0\",1));/p'
