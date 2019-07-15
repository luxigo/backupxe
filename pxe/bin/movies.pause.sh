#!/bin/sh
. /pxe/etc/config
DAY=`date +%d | sed -r -e s/^0//`
DAY=25

i=0

while [ $i -lt 24 ] ; do
	i=`expr $i + 1`
	PAUSE=`getrec /pxe/etc/movie.pause $i`
	[ "$PAUSE" = "1" ] && continue
	hw=`getrec /pxe/etc/machines $i`
	ip=`dhcplease $hw`
	[ -z "$ip" ] && continue
	setrec /pxe/etc/movie.pause $ip 1
	if [ $i -le $DAY ] ; then
		wget --timeout=10 --tries=1 http://$ip/cgi-bin/killmplayer.cgi -O /dev/null
	fi

done
