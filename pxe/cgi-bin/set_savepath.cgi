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
                        pc) pc=$value ;;
                        path) path=$value ;;
                esac
        done
fi

[ -z "$pc" ] && exit 1
mac=`getrec /pxe/etc/machines $pc`
[ -z "$mac" ] && exit 1

if [ -n "$path" ] ; then
	setrec /pxe/etc/savepath $mac $path
else
	delrec /pxe/etc/savepath $mac
fi
