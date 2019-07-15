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
                        pc) PC=$value ;;
                        machine) PC=$value ;;
                esac
		if [ -n "$PC" ] ; then
			machines="$machines $PC"
			PC=
		fi
        done
fi

PXECFGDIR=/tftpboot/pxelinux/pxelinux.cfg

for PC in $machines ; do

	hwaddr=`getrec /pxe/etc/machines $PC || true` 
	ip=`dhcplease $hwaddr || true`

	if [ -n "$ip" ] ; then
		STATUS=`getrec /pxe/etc/pcstatus $PC`
		case $STATUS in 
			G*)
				VOL=`sed -r -n -e 's/.* volume=([0-9]+).*/\1/p' $PXECFGDIR/movies.d/film$PC`
				[ -z "$VOL" ] && VOL=50
				wget --tries=1 --timeout=10 http://$ip/cgi-bin/mixer.cgi?vol=$VOL || true
			;;
		esac
	fi
done
