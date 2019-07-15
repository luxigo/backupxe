
function backupxe_onload(event) {
	xmlhttpgetsync('/cgi-bin/pxe/menus.cgi?backupxe','menus');
	document.getElementById("gui").appendChild(gui);
	showpclist();
	loadicons("default");
	SimpleContextMenu.setup({'preventDefault':true, 'preventForms':false});
	SimpleContextMenu.attach('pcIcon', 'menu1',menuUpdate);
	SimpleContextMenu.attach('map', 'menu1b',menuUpdate);
	SimpleContextMenu.attach('pclisthead', 'menu3',menuUpdate);
SimpleContextMenu.attach('pclisthead', 'menu3',menuUpdate);
SimpleContextMenu.attach('columnPXEconfig', 'menu6',menuUpdate);
SimpleContextMenu.attach('columnSave', 'menu5',menuUpdate);
SimpleContextMenu.attach('columnRestore', 'menu4',menuUpdate);
	Unselectable.enable(event);
	reloadIconsInterval=setInterval("reloadicons('default')",10000);
	loadGlobalsInterval=setInterval("xmlhttpget('/cgi-bin/pxe/loadglobals.cgi','eval');",30000);
}

