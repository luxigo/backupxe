#!/bin/bash

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
                	what) what=$value ;;
                        pc) pc=$value ;;
                        partition) partition=$value ;;
                        enable) enable=$value ;;
                esac
        done
fi

[ -z "$pc" ] && exit 1
[ -z "$partition" ] && exit 1
[ -z "$enable" ] && exit 1

disk=`echo $partition | sed -r -n -e 's#^/dev/([a-z]+).*#\1#p'`

mac=`getrec /pxe/etc/machines $pc`
[ -z "$mac" ] && exit 1

case "$what" in
	save)
		if [ "$enable" = "1" ] ; then
			sed -r -e s#^\\\#$partition\$#$partition# /pxe/image/$mac/$disk/partitions.save > /tmp/partitions.save.$$.tmp && cat /tmp/partitions.save.$$.tmp > /pxe/image/$mac/$disk/partitions.save
		else
			sed -r -e s#^$partition\$#\\\#$partition# /pxe/image/$mac/$disk/partitions.save > /tmp/partitions.save.$$.tmp && cat /tmp/partitions.save.$$.tmp > /pxe/image/$mac/$disk/partitions.save
		fi
		rm /tmp/partitions.save.$$.tmp
		;;
	restore)
		if [ ! -f /pxe/image/$mac/$disk/partitions.restore ] ; then
		    cp -a /pxe/image/$mac/$disk/partitions.save /pxe/image/$mac/$disk/partitions.restore || exit 1
		fi
		if [ "$enable" = "1" ] ; then
			sed -r -e s#^\\\#$partition\$#$partition# /pxe/image/$mac/$disk/partitions.restore > /tmp/partitions.restore.$$.tmp && cat /tmp/partitions.restore.$$.tmp > /pxe/image/$mac/$disk/partitions.restore
		else
			sed -r -e s#^$partition\$#\\\#$partition# /pxe/image/$mac/$disk/partitions.restore > /tmp/partitions.restore.$$.tmp && cat /tmp/partitions.restore.$$.tmp > /pxe/image/$mac/$disk/partitions.restore
		fi
		rm /tmp/partitions.restore.$$.tmp
		;;
esac
