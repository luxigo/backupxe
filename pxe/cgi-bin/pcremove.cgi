#!/bin/sh
. /pxe/etc/config

set -e

echo Content-type: text/html
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

	varname=`echo $param | cut -f 1 -d = | urldecode`
	value=`echo $param | cut -f 2 -d =  | urldecode`
	case "$varname" in 
		pc)
			pc="$value"
			mac=`getrec /pxe/etc/machines $pc`
			delrec /pxe/etc/machines $pc || true
			delrec /pxe/etc/pcstyle $pc || true
			delrec /pxe/etc/restorepath $pc || true
			delrec /pxe/etc/restorembr $pc || true
			delrec /pxe/etc/restoresf $pc || true
			delrec /pxe/etc/pcstatus $pc || true
			;;
	esac
done > /dev/null
echo 'busy();'
/pxe/bin/getpcicons.sh "default&async=0"
echo 'ready();'
exec /pxe/bin/getpcicons.sh "register&async=0" 1>&- &
