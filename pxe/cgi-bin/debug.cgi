#!/bin/sh
exit 1
. /pxe/etc/config

set -e

echo Content-type: text/html
echo 

echo '<html><body>'
#echo "$0 $@"

if [ -n "$QUERY_STRING" ] ; then

	count=0
        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

                [ -z "$param" ] && continue

		if [ $count -eq 0 ] ; then
			debug=$param
			if [ "$debug" == 1 ] ; then
				echo "export DEBUG=1" > /pxe/etc/debug
				echo "set -x" >> /pxe/etc/debug
			else
				echo "export DEBUG=" > /pxe/etc/debug
				echo "set +x" >> /pxe/etc/debug
			fi
			break
			;;
                fi
        done
fi

echo '</body></html>'

