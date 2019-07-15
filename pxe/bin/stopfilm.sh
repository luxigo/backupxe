#!/bin/sh
. /pxe/etc/config

set +e

DAY=`date +%d | sed -r -e s/^0//`

while true ; do
	i=0
	one=
	while [ $i -lt 24 ] ; do
		i=`expr $i + 1`
		STATUS=`getrec /pxe/etc/pcstatus $i 2> /dev/null` || continue
		if [ "$STATUS" == "GM" ] ; then
			lanreboot.sh $i &
			one=1
		fi
	done
	[ -z "$one" ] && break
	sleep 10
done
	
