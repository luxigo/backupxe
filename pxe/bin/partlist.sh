#!/bin/sh

. /pxe/etc/config

WORKDIR=/pxe
what=$1
MAC=$2

cd $WORKDIR/image/$MAC || exit 1

if [ "$what" = "restore" ] && [ ! -f ./partitions.$what ] ; then
  what='save'
fi

for part in `cat ./*/partitions.$what` ; do
  echo $part
done
