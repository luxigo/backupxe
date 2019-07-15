#!/bin/sh

. /pxe/etc/config

set -e

echo Content-Type: text/html
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
			pc|machine) PC=$value ;;
                esac
		if [ -n "$PC" ] ; then
			machines="$machines $PC"
			PC=
		fi
        done
fi

PXECFGDIR=/tftpboot/pxelinux/pxelinux.cfg

for PC in $machines ; do
#	sed -r -e 's/volume=[0-9]+/volume='$VOL'/' $PXECFGDIR/movies.d/film$PC > /tmp/film$PC.$$.tmp && cat /tmp/film$PC.$$.tmp > $PXECFGDIR/movies.d/film$PC
#	rm /tmp/*.$$.tmp 2> /dev/null || true

	hwaddr=`getrec /pxe/etc/machines $PC || true` 
	ip=`dhcplease $hwaddr || true`

	if [ -n "$ip" ] ; then
		STATUS=`getrec /pxe/etc/pcstatus $PC`
		case $STATUS in 
			G*)
				wget --tries=1 --timeout=10 http://$ip/cgi-bin/mixer.cgi?vol=0 || true
			;;
		esac
	fi
done
