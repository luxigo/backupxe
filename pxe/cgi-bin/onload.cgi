#!/bin/sh

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
