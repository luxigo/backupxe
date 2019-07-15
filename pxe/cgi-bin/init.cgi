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


PATH=/pxe/bin:/pxe/bin/`uname -m`:$PATH
env > /tmp/cgi.env
if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        js) JS=1 ; EXT=$value ;;
			html) JS="" ; EXT=$value ;;
			*) NAME=`basename $varname` ;;
                esac
        done
fi

if [ -z "$NAME" ] ; then
	echo Content-Type: text/javascript
	echo
	echo "alert('init.cgi: not enough parameters');"
	exit 1
fi

. /pxe/etc/config

echo Content-Type: text/javascript
echo Pragma: no-cache
echo

for scriptname in `sed -r -n -e '/^#/b' -e 's/^'$NAME' (.*\.'$EXT') *$/\1/p' /pxe/etc/modules` ; do
	  [ -z "$scriptname" ] && continue
	  cat $scriptname || exit 1
done
