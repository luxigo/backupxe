#!/bin/sh
. /pxe/etc/debug
. /pxe/bin/auth

set -e
echo Content-Type: text/html
echo

HOSTSMAC=/pxe/etc/hosts.mac
IMAGE_DIR=/pxe/image

count=`cat $HOSTSMAC | wc -l`

i=0
for dirname in `ls -1d $IMAGE_DIR/00* $IMAGE_DIR/global/* | sort -u` ; do
	echo -n "backupdir[$i]='$dirname';"
 	i=`expr $i + 1`
done

