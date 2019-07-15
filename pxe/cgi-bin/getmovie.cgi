#!/bin/sh

PXELINUXCFGDIR=/tftpboot/pxelinux/pxelinux.cfg/
. /pxe/etc/config


echo Content-Type: text/plain
echo Pragma: no-cache
echo

if [ -n "$QUERY_STRING" ] ; then

  MOVIE=`echo $QUERY_STRING | urldecode`
  
 #       for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
 #               [ -z "$param" ] && continue
 #               varname=`echo $param | cut -f 1 -d =`
 #               value=`echo $param | cut -f 2 -d =`
 #               case "$varname" in
 #                       mac) MAC=`echo $value | tr A-Z a-z | tr ':' '-'` ;;
 #                       *) MOVIE=$value ;;
 #               esac
 #       done
else
	exit 1
fi


if [ -f /tmp/dhcp.leases ] ; then
	MAC=`sed -r -n -e 's/:/-/g' -e 's/^.*(00\-[0-9a-f\-]+) '$REMOTE_ADDR' .*/\1/p' /tmp/dhcp.leases`
else
	MAC=`/usr/sbin/arp -an | sed -r -n -e 's/.*\('$REMOTE_ADDR'\)[^0-9]+([0-9a-zA-Z:]+).*/\1/p' | tr A-Z a-z | tr ':' '-'`
fi

[ -z "$MAC" ] && exit 1

set -x
old=`sed -r -n -e 's/^([0-9a-f\-]+) +CABINE'$MOVIE'$/\1/p' /pxe/etc/hosts.mac`
if [ -n "$old" ] && [ "$old" != "$MAC" ] ; then
	delrec /pxe/etc/hosts.mac $old
fi
setrec /pxe/etc/hosts.mac $MAC CABINE$MOVIE
cd $PXELINUXCFGDIR
ln -sf movies.d/film$MOVIE 01-$MAC
set +x

filename=`getrec /pxe/etc/movies $MOVIE`
[ -z "$filename" ] && exit 1
echo $filename
