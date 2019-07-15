#!/bin/bash
. /pxe/etc/config
MACHINES="/pxe/etc/machines"
RESTOREPATH="/pxe/etc/restorepath"
set -e

echo Content-Type: text/html
echo

. /pxe/bin/auth
#. /pxe/bin/jsauth

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        pc) pc=$value ;;
                        what) what=$value ;;
                esac
        done
fi

mac=`getrec $MACHINES $pc`
backupdir=`getrec $RESTOREPATH $mac`

cd $backupdir
