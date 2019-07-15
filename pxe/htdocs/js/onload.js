/*
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
*/

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
