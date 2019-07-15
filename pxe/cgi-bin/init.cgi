#!/bin/sh

PATH=/pxe/bin:/pxe/bin/`uname -m`:$PATH
env > /tmp/cgi.env
if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        js) JS=1 ; EXT=$value ;;
			html) JS="" ; EXT=$value ;;
			*) NAME=`basename $varname` ;;
                esac
        done
fi

if [ -z "$NAME" ] ; then
	echo Content-Type: text/javascript
	echo
	echo "alert('init.cgi: not enough parameters');"
	exit 1
fi

. /pxe/etc/config

echo Content-Type: text/javascript
echo Pragma: no-cache
echo

for scriptname in `sed -r -n -e '/^#/b' -e 's/^'$NAME' (.*\.'$EXT') *$/\1/p' /pxe/etc/modules` ; do
	  [ -z "$scriptname" ] && continue
	  cat $scriptname || exit 1
done
