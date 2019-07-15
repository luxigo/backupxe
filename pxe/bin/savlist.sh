#!/bin/sh
. /pxe/etc/config
IMGDIR=/pxe/image/

case "$1" in
	-m)
		match="$2"
		;;
		
esac

( for sav in `find $IMGDIR -name _ok` ; do

    mac=`echo $sav | sed -r -n -e 's/.*\/([0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2}\-[0-9a-f]{2})\/.*/\1/p'`

    name=`getrec /pxe/etc/hosts.mac $mac 2> /dev/null`
    savdate=`cat $sav`
    

  if [ -n "$match" ] ; then
  	if [ "$match" = "$name $savdate" ] ; then
  	  echo `dirname $sav` 
      	  break
      	fi
  else
#    echo "$name $disk $savdate"
    echo "$name $savdate"
  fi  
  
done )
# | /pxe/bin/sort -u -k 3,4 -r
