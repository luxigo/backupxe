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

HOSTSMAC=/pxe/etc/hosts.mac

count=`cat $HOSTSMAC | wc -l`

i=0
while [ $i -lt $count ] ; do

  i=`expr $i + 1`
  line=`sed -r -n -e ${i}p -e ${i}q $HOSTSMAC`

  mac=`echo $line | cut -f 1 -d ' '`
  [ -z "$mac" ] && continue

  name=`echo $line | cut -f 2 -d ' '`

  echo -n "namelist[$i]='$name';maclist[$i]='$mac';"

done
