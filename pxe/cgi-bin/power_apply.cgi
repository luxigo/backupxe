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

WORKDIR=/pxe
PXEUSER=Administrateur

wakeupmachine () {
  while true ; do
    wakeonlan -i $destip -p 9 $mac
    if [ $? -ne 0 ] ; then
      echo `logprefix` error: cannot start the pc
      return 1
    fi
    [ -f $WORKDIR/$mac/ready ] && break
    sleep 10
  done
  return 0

}

if [ -z "$HTTP_HOST" ] ; then

  POSTDATA="$1"
  shift
  while [ -n "$1" ] ; do
    POSTDATA="$POSTDATA&$1"
    shift
  done
  nohtml=1

else

  echo Content-type: text/html
  echo

  POSTDATA=`cat`

fi

n=1
while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  case $pname in
   maclist) maclist=`echo $pval | urldecode` ;;
  esac

  if [ "$pval" = "on" ] ; then
    if [ -z "$onlist" ] ; then
      onlist=$pname
    else
      onlist="$onlist $pname"
    fi
    continue
  fi

done

[ -z "$nohtml" ] && echo '<html><body>'

for mac in $maclist ; do

  if grep -q $mac $WORKDIR/etc/hosts.mac ; then
    name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
  else
    name=$mac
  fi

  for mac2 in $onlist ; do
    if [ "$mac" = "$mac2" ] ; then
       break
    fi
  done

  if [ "$mac" = "$mac2" ] ; then
    echo "starting  $mac<br>"
    wakeonlan -i $destip -p 9 $mac

  else
    ip=`dhcplease $mac`
    if [ -n "$ip" ] ; then
      echo "shuting down $mac<br>"
      ssh -o PasswordAuthentication=no $PXEUSER@$ip halt &
    fi
  fi

done

[ -z "$nohtml" ] && echo '</body></html>'
