#!/bin/sh
. /pxe/etc/config
DAY=`date +%d | sed -r -e s/^0//`

i=0

while [ $i -lt $DAY ] ; do
	i=`expr $i + 1`
	hw=`getrec /pxe/etc/machines $i`
	ip=`dhcplease $hw`
	[ -z "$ip" ] && continue
	wget --timeout=10 --tries=1 http://$ip/cgi-bin/reboot.cgi &
done

sleep 180

lanwake.sh 3

