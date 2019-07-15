#!/bin/sh
. /pxe/etc/config
DAY=`date +%d | sed -r -e s/^0//`
DAY=25
i=1

set +e

while true; do

	one=0
	while [ $i -lt $DAY ] ; do
		hw=`getrec /pxe/etc/machines $i`
		i=`expr $i + 1`
		ip=`dhcplease $hw`
		[ -z "$ip" ] && continue
		setrec /pxe/etc/movie.pause $ip 0
		wget --timeout=10 --tries=2 http://$ip/cgi-bin/killmplayer.cgi -O /dev/null
		sleep 6
		
	done

	[ $one -eq 0 ] && break

done
