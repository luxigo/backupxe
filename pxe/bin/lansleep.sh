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

. /pxe/etc/config

PXEUSER=Administrateur

if [ -z "$1" ] ; then
  hwlist=`maclist.sh -all 2> /dev/null`
else
  hwlist="$@"
fi

for hwaddr in $hwlist ; do

  if echo $hwaddr | egrep -q '^[0-9]+$' ; then
   hwaddr=`getrec /pxe/etc/machines $hwaddr`
   [ -z "$hwaddr" ] && continue
  fi

  if echo $hwaddr | egrep -q '^[[:alnum:]]+$' ; then
    netbiosname=`echo $hwaddr | tr a-z A-Z`
    hwaddr=`egrep " $netbiosname\$" /pxe/etc/hosts.mac | cut -f 1 -d ' '`
    if [ -z "$hwaddr" ] ; then
      maclist.sh -more > /dev/null
      hwaddr=`egrep " $netbiosname\$" /pxe/etc/hosts.mac | cut -f 1 -d ' ' | tr a-z A-Z | tr '\-' ':'`
      if [ -z "$hwaddr" ] ; then
        echo "$netbiosname: cant guess ethernet hardware address<br>"
        continue
      fi
    fi
  fi

  ip=`dhcplease $hwaddr`
  if [ -n "$ip" ] ; then
#    ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no $PXEUSER@$ip shutdown -s -c Sorry -t 3 -f &
#    echo "/usr/local/bin/poweroff.sh &" | nc -i 1 $ip 23
	wget --tries=1 --timeout=10 http://$ip/cgi-bin/poweroff.cgi -O /dev/null &
 fi

done
