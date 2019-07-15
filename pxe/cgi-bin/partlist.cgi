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
                	what)
                		what=$value
                		;;
                	pc)
                		pc=$value
                		;;
                		
                esac
        done
fi

echo "partition$what[$pc]=new Array;"
mac=`getrec /pxe/etc/machines $pc`
/pxe/bin/partlist.sh $what $mac | sed -r -n -e 's/^#(.*)/partition'$what'['$pc'].push(new Array("\1",0));/p' -e t -e 's/.*/partition'$what'['$pc'].push(new Array(\"\0\",1));/p'
