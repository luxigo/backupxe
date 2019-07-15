#!/bin/sh
. /pxe/etc/config

echo Content-Type: text/plain
echo

case "$QUERY_STRING" in
	df)
		exec rundf.sh ;;
	nbtscan)
		exec nbtscan.sh ;;
	pingall)
		exec pingall ;;
		
esac

