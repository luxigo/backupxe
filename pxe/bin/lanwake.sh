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

if [ -n "$REMOTE_SERVER" ] ; then
  CGI=yes
fi

if [ -z "$1" ] ; then
  hwlist=`maclist.sh -all`
else
  hwlist="$@"
fi

for hwaddr in $hwlist ; do

  if echo $hwaddr | egrep -q '^[0-9]+$' ; then
    hwaddr=`getrec /pxe/etc/machines $hwaddr`
    [ -z "$hwaddr" ] && continue
  fi

  [ -n "$notfirst" ] && sleep 3

  if echo $hwaddr | egrep -q '^[[:alnum:]]+$' ; then
    netbiosname=`echo $hwaddr | tr a-z A-Z`
    hwaddr=`egrep " $netbiosname\$" /pxe/etc/hosts.mac | cut -f 1 -d ' '`
    if [ -z "$hwaddr" ] ; then
      maclist.sh -more > /dev/null
      hwaddr=`egrep " $netbiosname\$" /pxe/etc/hosts.mac | cut -f 1 -d ' ' | tr a-z A-Z | tr '\-' ':'`
      if [ -z "$hwaddr" ] ; then
        echo "$netbiosname: not found in hosts.mac<br>"
        continue
      fi
    fi
  fi

  hwaddr=`echo $hwaddr | tr '\-' ':'`

  ip=`dhcplease $hwaddr`
  if [ -n "$ip" ] ; then
     bcast=`echo $ip | sed -r -n -e 's/^([0-9]+\.[0-9]+\.[0-9]+\.).*/\1/p'`255
     if [ -n "$CGI" ] ; then
       wakeonlan -p 9 -i $bcast $hwaddr > /dev/null
     else
       wakeonlan -p 9 -i $bcast $hwaddr
     fi
  else
     if [ -n "$CGI" ] ; then
       wakeonlan -p 9 $hwaddr > /dev/null
     else
       wakeonlan -p 9 $hwaddr
     fi
     for destip in `cat /pxe/etc/wakeonlan.destip` ; do
       if [ -n "$CGI" ] ; then
         wakeonlan -p 9 -i $destip $hwaddr > /dev/null
       else
         wakeonlan -p 9 -i $destip $hwaddr
       fi
     done
  fi
   notfirst=1
done
