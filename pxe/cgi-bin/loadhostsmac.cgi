#!/bin/sh
. /pxe/etc/config

set -e
echo Content-Type: text/html
echo

HOSTSMAC=/pxe/etc/hosts.mac

count=`cat $HOSTSMAC | wc -l`

i=0
while [ $i -lt $count ] ; do

  i=`expr $i + 1`
  line=`sed -r -n -e ${i}p -e ${i}q $HOSTSMAC`

  mac=`echo $line | cut -f 1 -d ' '`
  [ -z "$mac" ] && continue

  name=`echo $line | cut -f 2 -d ' '`

  echo -n "namelist[$i]='$name';maclist[$i]='$mac';"

done


