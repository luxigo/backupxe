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
                	match)
                		PARAMS"=-m $value"
                		;;
                		
                esac
        done
fi

echo savlist=new Array\;

if [ -z "$PARAMS" ] ; then
	/pxe/bin/savlist.sh | sed -r -e 's/.*/savlist.push(\"\0\");/'
else
	/pxe/bin/savlist.sh $PARAMS
fi
