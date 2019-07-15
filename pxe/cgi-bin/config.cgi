#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
