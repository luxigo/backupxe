#!/bin/sh
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
#    echo "/usr/local/bin/reboot.sh &" | nc -i 1 $ip 23
	wget --tries=1 --timeout=10 http://$ip/cgi-bin/reboot.cgi -O /dev/null &
 fi

done
