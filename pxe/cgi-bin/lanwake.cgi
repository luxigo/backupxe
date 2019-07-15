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

echo Content-type: text/html
echo

echo '<html><body>'

for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
  machine=`echo $param | cut -f 2 -d =`
  name=`egrep "^$machine " /pxe/etc/machines | cut -f 2 -d ' '`
  if [ -z "$name" ] ; then
    name=$machine
  fi
  namelist="$namelist$name "
done

if [ -n "$namelist" ] ; then
#  echo "/pxe/bin/lanwake.sh $namelist"
  eval "/pxe/bin/lanwake.sh -cgi $namelist"
else
  echo nothing to do
fi

echo '</body></html>'
