#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux, all rights reserved.
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

if [ -n "$REMOTE_ADDR" ] ; then
        echo Content-Type: text/javascript
        echo
else
        echo // DONT MODIFY !! this file has been generated
        echo //
        echo // Edit $0 instead !
        echo
fi

cat << EOF

function backupxe_onload(event) {
	//xmlhttpgetsync('/cgi-bin/pxe/menus.cgi?backupxe','menus');
	xmlhttpgetsync('/pxe/menus.html','menus');
	document.getElementById("gui").appendChild(gui);
	loadicons("default");
	SimpleContextMenu.setup({'preventDefault':true, 'preventForms':false});
	SimpleContextMenu.attach('pcIcon', 'menu1',menuUpdate);
	SimpleContextMenu.attach('map', 'menu1b',menuUpdate);
	SimpleContextMenu.attach('body', 'menu1b',menuUpdate);
	SimpleContextMenu.attach('pclist', 'menu1b',menuUpdate);
	SimpleContextMenu.attach('pclisthead', 'menu3',menuUpdate);
	SimpleContextMenu.attach('menuMovie','menuMovie',menuUpdate);
	SimpleContextMenu.attach('menuGeexbox','menuGeexbox',menuUpdate);
	SimpleContextMenu.attach('menuGeexbox2','menuGeexbox2',menuUpdate);
	SimpleContextMenu.attach('menuVol','menuVol',menuUpdate);
	SimpleContextMenu.attach('menuVol2','menuVol2',menuUpdate);
	SimpleContextMenu.attach('menuPartimage','menuPartimage',menuUpdate);
	SimpleContextMenu.attach('menuPartimage2','menuPartimage2',menuUpdate);
	SimpleContextMenu.attach('menupc','menupc',menuUpdate);
	SimpleContextMenu.attach('menusel','menusel',menuUpdate);
EOF

for col in `cat /pxe/etc/pclist/columns` ; do
	 [ -s /pxe/etc/pclist/$col/onload ] && . /pxe/etc/pclist/$col/onload
done

cat << EOF
	Unselectable.enable(event);
	reloadIconsInterval=setInterval("reloadicons('default')",10000);
	loadGlobalsInterval=setInterval("xmlhttpget('/cgi-bin/pxe/loadglobals.cgi','eval');",30000);
	showpclist();
}

EOF
