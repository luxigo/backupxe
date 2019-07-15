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
IMGDIR=/pxe/image/

case "$1" in
	-m)
		match="$2"
		;;

esac

( for sav in `find $IMGDIR -name _ok` ; do

    mac=`echo $sav | sed -r -n -e 's/.*\/([0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2})\/.*/\1/p'`

    name=`getrec /pxe/etc/hosts.mac $mac 2> /dev/null`
    savdate=`cat $sav`


  if [ -n "$match" ] ; then
  	if [ "$match" = "$name $savdate" ] ; then
  	  echo `dirname $sav`
      	  break
      	fi
  else
#    echo "$name $disk $savdate"
    echo "$name $savdate"
  fi

done )
# | /pxe/bin/sort -u -k 3,4 -r
