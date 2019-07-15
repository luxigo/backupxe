#!/bin/sh
. /pxe/etc/config

echo Content-Type: text/plain
echo Pragma: no-cache
echo

env > /tmp/enable.env

HOUR=`date +%H`
PAUSE=`getrec /pxe/etc/movie.pause $REMOTE_ADDR || true`

if [ "$PAUSE" = "1" ] || [ -z "$PAUSE" ] ; then
	echo NO
else
	echo YES
fi
exit 0
