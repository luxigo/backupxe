#!/bin/sh

if echo $1 | grep -q ^/ ; then
	exec mount $@
	exit
fi

case "$BPXE_NETFS" in
	sshfs)
		exec shfsmount $@ ;;
	*)
		exec mount $@ ;;
esac
