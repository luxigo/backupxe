#!/bin/sh
. /pxe/etc/config

if [ -n "$QUERY_STRING" ] ; then
        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        async) ASYNC=$value ;;
                        register) page=register ;;
                        default) page=default ;;
                        reload) reload=1 ;;
                esac
        done
fi

cat /pxe/etc/pcicons.$page$reload

[ -f /var/run/pxe/getpcicons.pid ] && kill -0 `cat /var/run/pxe/getpcicons.pid` > /dev/null 2>&1 && exit 0 

exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &

exit

############################
exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &
if [ ! -f /pxe/etc/pcicons.$page$reload ] || [ /pxe/etc/pcstyle -nt /pxe/etc/pcicons.$page$reload ] ; then
	touch /pxe/etc/pcicons.$page$reload
	getpcicons.sh "$QUERY_STRING&async=0"
fi

cat /pxe/etc/pcicons.$page$reload

[ -f /var/run/pxe/getpcicons.pid ] && kill -0 `cat /var/run/pxe/getpcicons.pid` > /dev/null 2>&1 && exit 0 
exec /pxe/bin/getpcicons.sh "$QUERY_STRING&async=1" 1>&- &
