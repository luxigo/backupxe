#!/bin/sh

. /pxe/etc/config

if [ -z "$1" ] ; then
  echo 'usage: makeicons.sh <count>' 2>&1
  exit 1
fi

i=1
while [ $i -le $1 ] ; do
  montage.sh $i
  i=`expr $i + 1`
done
