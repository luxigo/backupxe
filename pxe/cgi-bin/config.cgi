#!/bin/sh
. /pxe/etc/config

set -e

HOSTSMAC=/pxe/etc/hosts.mac

echo Content-type: text/html
echo

maclist.sh -more > /dev/null

machinesEdit () {
	echo '<html><body>'

	echo '<table>'
	echo '<tr><td>'


	echo '<h4>Machines</h4>'
	echo '</td><td>'
	echo '</td></tr>'

	echo '<tr><td>'
	for m in `cat /pxe/etc/machines | sort -n | sed -r -n -e 's/^([0-9]+)[\ \t]+(.*)/\1_\2/p'` ; do

		pc=`echo $m | cut -f 1 -d _`
		hwaddr=`echo $m | cut -f 2 -d _ | tr : - | tr A-Z a-z`
	
		name=`(egrep ^$hwaddr $HOSTSMAC || true) | cut -f 2 -d ' '`;
		if [ -z "$name" ] ; then
			name=$hwaddr
		fi

		echo '<img src="/pxe/thumbs/pc'$pc'_24x24.png">&nbsp;'$name
		echo '<br>'

	done
	echo '</tr>'

}

machinesEdit

echo '</body></html>'
