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
                        pc) pc=$value ;;
                        path) path=$value ;;
                        sav) sav=`echo $value | tr '_' ' '` ;;
                esac
        done
fi

[ -z "$pc" ] && exit 1
mac=`getrec /pxe/etc/machines $pc`
[ -z "$mac" ] && exit 1

if [ -n "$path" ] ; then
  setrec /pxe/etc/restorepath $mac $path
  exit 0
fi

if [ -n "$sav" ] ; then
	path=`savlist.sh -m "$sav"`
	
	if [ "$path" = "/pxe/image/$mac" ] ; then
		delrec /pxe/etc/restorepath $mac
	else
		if [ -z  "$path" ] ; then
		  echo "$0: $sav: not found"
		  exit 1
		fi
		setrec /pxe/etc/restorepath $mac $path
	fi
	exit 0
fi

exit 1
