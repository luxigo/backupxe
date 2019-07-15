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

echo Content-Type: text/plain
echo Pragma: no-cache
echo

cat /pxe/htdocs/menus.html
exit

cat << EOF

menu1=document.createElement('ul');
menu1.className="SimpleContextMenu";

var li=document.createElement('li');
var a=document.createElement('a');
a.name="contextOn";
a.href="javascript:action('on',numSuffix(SimpleContextMenu._attachedElement))";
a.innerHTML="Allumer";
li.appendChild(a);
menu1.appendChild(li);

		<!-- pc icon -->
		<ul id="menu1" class="SimpleContextMenu">
			<li><a name="contextOn" href="javascript:action('on',numSuffix(SimpleContextMenu._attachedElement))">Allumer</a></li>
			<li class="separator"><a name="contextOff" href="javascript:action('off',numSuffix(SimpleContextMenu._attachedElement))">Eteindre</a></li>
			<li class="separator"><a href="javascript:action('bootdsl',numSuffix(SimpleContextMenu._attachedElement))">Boot DSL</a></li>
			<li class="separator"><a href="javascript:action('register',numSuffix(SimpleContextMenu._attachedElement))">R&eacute;pertorier</a></li>
			<li><a name="contextSave" href="javascript:action('save',numSuffix(SimpleContextMenu._attachedElement))">Sauvegarder</a></li>
			<li class="separator"><a name="contextRestore" href="javascript:action('restore',numSuffix(SimpleContextMenu._attachedElement))">Restaurer</a></li>
			<li name="contextToSel"><a href="javascript:pcclickall(1)">Tout S&eacute;lectioner</a></li>
			<li name="contextSel"><a href="javascript:pcclickall(0)">Tout D&eacute;s&eacute;lectioner</a></li>
			<li class="separator"><a href="javascript:pcclickall('invert')">Inverser la S&eacute;lection</a></li>
			<li class="separator"><a href="javascript:switchIconMode()">Editer le Plan</a></li>
			<li class="separator" name="switchInfobulles"><a href="javascript:enableInfobulles()">Activer les Infobulles</a></li>
		</ul>
		<!-- map -->
		<ul id="menu1b" class="SimpleContextMenu">
			<li name="contextSel"><a href="javascript:action('on')">Allumer Selection</a></li>
			<li name="contextSel" class="separator"><a href="javascript:action('off')">Eteindre Selection</a></li>
			<li class="separator"><a href="javascript:action('bootdsl')">Boot DSL</a></li>
			<li class="separator"><a href="javascript:action('register')">R&eacute;pertorier</a></li>
			<li name="contextSel"><a href="javascript:action('save')">Sauvegarder Selection</a></li>
			<li name="contextSel" class="separator"><a href="javascript:action('restore')">Restaurer Selection</a></li>
			<li name="contextToSel"><a href="javascript:pcclickall(1)">Tout S&eacute;lectioner</a></li>
			<li name="contextSel"><a href="javascript:pcclickall(0)">Tout D&eacute;s&eacute;lectioner</a></li>
			<li class="separator"><a href="javascript:pcclickall('invert')">Inverser la S&eacute;lection</a></li>
			<li class="separator"><a href="javascript:switchIconMode()">Editer le Plan</a></li>
			<li class="separator" name="switchInfobulles"><a href="javascript:enableInfobulles()">Activer les Infobulles</a></li>
		</ul>
		<!-- pc register -->
		<ul id="menu2" class="SimpleContextMenu">
			<li class="separator"><a href="#">Changer l'Icone</a></li>
			<li class="separator"><a name="contextRemove" href="javascript:pcremove(numSuffix(SimpleContextMenu._attachedElement))">Enlever cette Machine</a></li>
			<li name="contextToSel"><a href="javascript:pcclickall(1)">Tout S&eacute;lectioner</a></li>
			<li name="contextSel"><a href="javascript:pcclickall(0)">Tout D&eacute;s&eacute;lectioner</a></li>
			<li class="separator"><a href="javascript:pcclickall('invert')">Inverser la S&eacute;lection</a></li>
			<li class="separator" name="quitEdit"><a href="javascript:switchIconMode()">Quitter l'Editeur</a></li>
		</ul>
		<!-- map register -->
		<ul id="menu2b" class="SimpleContextMenu">
			<li class="separator"><a href="javascript:alert('Double-cliquez dans une case vide de la premiere colonne de la liste (Id), entrez un numero de machine, puis placez la machine sur le plan.' )">Ajouter une Machine</a></li>
			<li class="separator"><a href="javascript:xmlhttpget('/pxe/mapupload.html','divmapupload');">Uploader un Plan</a></li>
			<li name="contextSel" class="separator"><a href="javascript:pcremove();">Enlever les machines selectionnees</a></li>
			<li name="contextToSel"><a href="javascript:pcclickall(1)">Tout S&eacute;lectioner</a></li>
			<li name="contextSel"><a href="javascript:pcclickall(0)">Tout D&eacute;s&eacute;lectioner</a></li>
			<li class="separator"><a href="javascript:pcclickall('invert')">Inverser la S&eacute;lection</a></li>
			<li class="separator" name="quitEdit"><a href="javascript:switchIconMode()">Quitter l'Editeur</a></li>
		</ul>
		<!-- columns list  -->
		<ul id="menu3" class="SimpleContextMenu">
			<li><a href="#"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/checkmark.png"></td><td>Id</td></tr></table></a></li>
			<li><a href="javascript:toggleColumns('name')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/checkmark.png"></td><td>Name</td></tr></table></a></li>
			<li><a href="javascript:toggleColumns('ip')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/checkmark.png"></td><td>IP</td></tr></table></a></li>
			<li><a href="javascript:toggleColumns('mac')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/checkmark.png"></td><td>MAC</td></tr></table></a></li>
			<li><a href="javascript:toggleColumns('pxeconfig')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/checkmark.png"></td><td>Network Boot</td></tr></table></a></li>
			<li><a href="javascript:toggleColumns('save')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/nomark.png"></td><td>Save</td></tr></table></a></li>
			<li class="separator"><a href="javascript:toggleColumns('restore')"><table cellspacing="0" cellpadding="0"><tr><td><img border="0" src="/pxe/pics/nomark.png"></td><td>Restore</td></tr></table></a></li>
		</ul>
		<!-- restore  -->
		<ul id="menu4" class="SimpleContextMenu">
			<li class="separator"><a href="#"><table><tr><td name="contextPcIcon"><img src='/pxe/pics/thumbs/pc.png'></td><td name="contextPcName"></td></tr></table></a></li>
			<li><a href="#">Sauvegarde&nbsp;&agrave;&nbsp;Restaurer:</a></li>
			<li class="separator"><table id="restorePath" cellborder="0" cellspacing="0" style="border-width: 0px; border-style: none;"></table></li>
			<li><a href="#">Disque&nbsp;&agrave;&nbsp;Disque depuis:</a></li>
			<li class="separator"><table id="srcList" cellspacing="0" cellpadding="0"></table></li>
			<li><a href="javascript:">Restaurer&nbsp;le&nbsp;MBR</a></li>
			<li class="separator"><a>Restaurer&nbsp;Table&nbsp;de&nbsp;Partitions</a></li>
		</ul>
		<!-- save  -->
		<ul id="menu5" class="SimpleContextMenu">
			<li class="separator"><a href="#"><table><tr><td name="contextPcIcon"><img src="/pxe/pics/thumbs/pc.png"></td><td name="contextPcName"></td></tr></table></a></li>
			<li><a href="#">Partitions&nbsp;&agrave;&nbsp;Sauvegarder:</a></li>
			<li class="separator"><table id="partList" cellspacing="0" cellpadding="0"></table></li>
			<li><a href="#">Destination Sauvegarde:</a></li>
			<li><a href="#"><table cellspacing="0" cellpadding="0"><tr><td><img style="border-style: none;" src="/pxe/pics/checkmark.png"></td><td>Network</td></tr></table></a></li>
			<li class="separator"><table id="destList" cellspacing="0" cellpadding="0"></table></li>
		</ul>
		<!-- pxeconfig  -->
		<ul id="menu6" class="SimpleContextMenu">
			<li><a href="#">D&eacute;marrage r&eacute;seau</a></li>
			<li class="separator"><table id="pxeconfig"></table></li>
		</ul>
