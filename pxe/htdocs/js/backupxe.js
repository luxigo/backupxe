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
var selection=new Array;
var listselection=new Array;
var listselectionName=new Array;
var pcpartitionssaved=new Array;
var pcdatesaved=new Array;
var pcdaterestored=new Array;
var pcdatebackuped=new Array;
var pcimagetorestore=new Array;
var cursav=new Array;
var pcsavepath=new Array;
var pcdiskspaceleft=new Array;
var pcname=new Array;
var pcmac=new Array;
var pcrestorembr=new Array;
var pcsavembr=new Array;
var pcrestoresf=new Array;
var pcsavesf=new Array;
var setglobals;
var pcuptime=new Array;
var pcip=new Array;
var backupdir=new Array;
var showdetails=new Array;
var enableclick=1;
var savlist=new Array;
var hostsmac=new Array;
var pcStyle=new Array;
var pcStyleElem=null;
var pcstylechanged=0;
var innerHTML_backup=new Array;
var divedit_file=new Array;
var divedit_menu=new Array;
var currentTab='on';
var actionConfirm=true;
var linkArray = new Array();
var busylevel=0;
var table_edit_backup;
var table_edit_td;
var table_edit_validate;
var addmachine_table_edit_td;
var addmachine_ok;
var addmachine_hostsmacIndex;
var reloadIconsInterval;
var loadGlobalsInterval;
var iconMode='default';
var _IBenable=false;
var mapselrect;
var partlist=new Array();
var partitionsave=new Array;
var partitionrestore=new Array;

mapselrect=new SelRect('mapselrect','map',mapselrect_callback);

function selectionGroup(_this) {

	var pc=numSuffix(_this);
	var group=new Array(_this);

	if (selection[pc]==0)
		return group;

	for (var i=1; i<selection.length; ++i) {

		if (i==pc || selection[i]!=1)
			 continue;

		var a=document.getElementsByName('machine'+i);
		for (j=0 ; j<a.length; ++j) {
			group.push(a[j]);
		}
		var a=document.getElementsByName('selection'+i);
		for (j=0 ; j<a.length; ++j) {
			group.push(a[j]);
		}
	}
	return group;
}

function getElementsByClassName(searchClass,node,tag) {
	return getElementsByClass(searchClass,node,tag);
}

function getElementsByClass(searchClass,node,tag) {
	var classElements = new Array();
	if ( node == null || node==undefined)
		node = document;
	if ( tag == null || tag==undefined)
		tag = '*';
	var els = node.getElementsByTagName(tag);
	var pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)");
	for (i = 0; i < els.length; i++) {
		if ( pattern.test(els[i].className) ) {
			classElements.push(els[i]);
		}
	}
	return classElements;
}

function mapselrect_callback(what) {
	switch(what) {
		case 'init':
			selrect._this.zIndex=dragObj.zIndex;
			break;
		case 'drag':
			break;

		case 'done':
			var _this=selrect._this;
			var d=document.getElementById(_this.selrect);
			selrect.top=parseInt(d.style.top,10);
			selrect.left=parseInt(d.style.left,10);
			selrect.bottom=selrect.top+parseInt(d.style.height,10);
			selrect.right=selrect.left+parseInt(d.style.width,10);
			pcIconList=getElementsByClass("pcIcon",document.getElementById("divicons"),'IMG');
			for (var i=0; i<pcIconList.length; ++i) {
				var img=pcIconList[i];
				var top=parseInt(img.style.top,10);
				if (top=="NaN") continue;
				var left=parseInt(img.style.left,10);
				var bottom=top+48;
				var right=left+48;
				if (selrect.top<top && selrect.left<left && selrect.bottom>bottom && selrect.right>right) {
					pcclick(numSuffix(pcIconList[i]));
					continue;
				}
				if (selrect.top>top && selrect.top<bottom && selrect.left<right && selrect.right>left) {
					pcclick(numSuffix(pcIconList[i]));
					continue;
				}
				if (selrect.bottom>top && selrect.bottom<bottom && selrect.left<right && selrect.right>left) {
					pcclick(numSuffix(pcIconList[i]));
					continue;
				}
				if (selrect.left>left && selrect.left<right && selrect.top<bottom && selrect.bottom>top) {
					pcclick(numSuffix(pcIconList[i]));
					continue;
				}
				if (selrect.right>left && selrect.right<right && selrect.top<bottom && selrect.bottom>top) {
					pcclick(numSuffix(pcIconList[i]));
					continue;
				}

			}
			break;
	}
}

function reselect() {
  var pc=1;
  while (pc<pcname.length) {
        if (selection[pc]==1) {
                eval('document.selection' + pc + '.src="/pxe/pics/white_coche.png"');
        }
        ++pc;
  }
}

function time2html(t) {
  var years=t/31536000.0;
  var days=t%31536000/86400.0;
  var hours=t%86400/3600.0;
  var mins=t%3600/60.0;
  var html="";
  if (years>=1) html+=years.toFixed() + " Ann&eacute;es ";
  if (days>=1) html+=days.toFixed() + " Jours ";
  if (hours>=1) html+=hours.toFixed() + " Heures ";
  if (mins>=1) html+=mins.toFixed() + " Minutes ";
  if (html=="") html="n/a";
  return html;
}

function getpcbull(pc) {
   return '\
<table class="bullHead">\
   <tr>\
   	<td><img src="/pxe/thumbs/pc'+pc+'_24x24.png"></td>\
   	<td valign="center" align="left" width="100%">\
   	  <strong>' + ((pcname[pc]=='')?'n/a':pcname[pc]) + '</strong>\
   	</td>\
   </tr>\
</table>\
<table class="bullBody">\
   <tr>\
	<td>Addresse:</td>\
	<td>'+((pcip[pc]=="")?'n/a':pcip[pc])+'</td>\
  </tr>\
  <tr>\
  	<td>Mac:</td>\
  	<td>' + pcmac[pc] + '</td>\
  </tr>\
  <tr>\
  	<td>Sauvegard&eacute;:</td>\
  	<td>' + ((pcdatesaved[pc]=="")?'n/a':pcdatesaved[pc]) + "</td>\
  </tr>\
  <tr>\
  	<td>Libre:</td>\
  	<td>" + ((pcdiskspaceleft[pc]=="")?'n/a':pcdiskspaceleft[pc]) + "</td>\
  </tr>\
  <tr>\
  	<td>UpTime:</td>\
  	<td>"+time2html(pcuptime[pc])+"</td>\
  </tr>\
</table>"

}

function selection_init() {
	for (var pc=1;pc<=pcname.length;pc++) {
		if (pcname[pc]!=undefined && selection[pc]==undefined)
			selection[pc]=0;
		else if (selection[pc]==1) {
			document.getElementsByName('selection'+pc)[0].src="/pxe/pics/white_coche.png";
//			eval('document.selection' + pc + '.src="/pxe/pics/white_coche.png"');
		}
	 }
}

function pcclick (pc) {

	if (!enableclick) return;

	if (selection[pc]==1) {
		document.getElementsByName('selection'+pc)[0].src="/pxe/pics/transparent.png";
		var lpc=document.getElementsByName('lpc'+pc);
		for (var i=0; i<lpc.length; ++i) {
			lpc[i].style.background="#f0f0f0";
		}
		selection[pc]=0;
	} else {
		document.getElementsByName('selection'+pc)[0].src="/pxe/pics/white_coche.png";
		var lpc=document.getElementsByName('lpc'+pc);
		for (var i=0; i<lpc.length; ++i) {
			lpc[i].style.background="#aaaadd";
		}
		selection[pc]=1;
	}
//	if (arguments[1]!='noEffect') new Effect.Pulsate(document.getElementsByName('selection' + pc)[0]);
}


function pcclickall (all) {
	if (!enableclick) return;
	for( var pc=1 ; pc<pcname.length ; pc++) {
  		if (selection[pc]==undefined) {
			continue;
		}
		if ( all == 'invert' || selection[pc] == 1-all) {
			pcclick(pc);
		}
	}
}

function divclose (divId) {
	var div=document.getElementById(divId);
	var i;
	div.innerHTML='';
	div.style.border='0';
	div.style.height='';
	div.style.width='';
	enableclick=1;
	i=1;
	while(arguments[i]!=undefined) {
		divclose(arguments[i]);
		++i;
	}
}

function getpcinfo(pc,what) {
	var reply='<strong>'+((pcname[pc]=='')?pcmac[pc]:pcname[pc])+'</strong>';
	switch(what) {
 		case 'on':
			break;
 		case 'off':
			break;
		case 'save':
			if (pcdatesaved[pc]==undefined) break;
			var d=pcdatesaved[pc].split(' ');
			reply+='</td><td align="right">'+d[0]+((d[1]==undefined)?'':""+d[1]);
			break;
		case 'restore':
			if (pcdaterestored[pc]==undefined) break;
			var d=pcdaterestored[pc].split(' ');
			reply+='</td><td align="right">'+d[0]+((d[1]==undefined)?'':""+d[1]);
			reply+='</td><td>'+pcdaterestored[pc];
			break;

	}
	return reply;
}

function toggledetails(what) {
	if (showdetails[what]==undefined) showdetails[what]=0;
	showdetails[what]=1-showdetails[what];
	tab_draw(what);
}


function action(what,who) {
	var xhr = null;
	var querystring = "" ;
	var descr;

	if (arguments.length==1 && !selected_something()) {
		alert("Vous devez d'abord sélectionner une ou plusieurs machines.");
		return;
	}

	switch(what) {
		case 'mute':
			descr="couper le son sur"
			what="/cgi-bin/pxe/movie.mute.cgi?";
			break;
		case 'unmute':
			descr="remettre le son sur"
			what="/cgi-bin/pxe/movie.unmute.cgi?";
			break;
		case 'unpause':
			descr="d'enlever la pause sur";
			what="/cgi-bin/pxe/movie.unpause.cgi?";
			break;
		case 'pause':
			descr="mettre en pause";
			what="/cgi-bin/pxe/movie.pause.cgi?";
			break;
		case 'reboot':
			descr="redemarrer";
			what="/cgi-bin/pxe/lanreboot.cgi?";
			break;
		case 'off':
			descr="redemarrer";
			what="/cgi-bin/pxe/lanreboot.cgi?";
			break;
		case 'on':
			descr="allumer";
			what="/cgi-bin/pxe/lanwake.cgi?";
			break;
		case 'save':
			descr="sauvegarder";
			what="/cgi-bin/pxe/bootandrun.cgi?partimage-save&";
			break;
		case 'restore':
			descr="restaurer";
			what="/cgi-bin/pxe/bootandrun.cgi?partimage-restore&";
			break;
		case 'bootdsl':
			descr="booter DSL sur";
			what="/cgi-bin/pxe/bootandrun.cgi?bootdsl&";
			break;
		case 'register':
			descr="repertorier";
			what="/cgi-bin/pxe/bootandrun.cgi?register&";
			break;
		case 'selectimage':
			return;
			break;
	}

	var count = 0 ;
	var first = 0 ;
	var msg = "";

	if (who!=undefined) {
		querystring="machine="+who;
		count=1;
		first=who;
	} else {
		for (var i=1; i < pcname.length; i++) {
			if (selection[i]==1) {
				if (count==0) {
					querystring="machine="+i;
					first=i;
				} else
					querystring+="&machine="+i;

			 	msg+=pcname[i]+'\n';
				switch(what) {
					case 'restore':
						break;
					case 'save':
						break;
				}
				count++;
			}
		}
	}

	if (count>0) {
		busy();
		if (actionConfirm) {
			if ((who!=undefined) || (count==1)) {
				if ((who==undefined) && (count==1)) {
					msg="";
				}
				msg=pcname[first]+" ?" + msg;
			} else {
				msg='ces '+count+" machines ?\n" + msg;
			}
			msg='Etes vous sur de bien vouloir '+descr+' ' + msg;
			if (!confirm(msg)) {
				ready();
				return;
			}
		}

		xmlhttpget(what+querystring,'divlog',undefined,'ready(); pcclickall(0);');
	}
}

function busy() {
/////////////////////	++busylevel;
	busylevel=1;
	document.body.style.cursor="progress";
	enableclick=false;
	setTimeout('ready()',10000);
}

function ready() {
	--busylevel;
	if (busylevel>0) return;
	busylevel=0;
	enableclick=true;
	document.body.style.cursor="";
}


function disablelinks(){
	var objLink = document.links;
	for(var i=0;i < objLink.length;i++) {
		linkArray[i] = objLink[i].href.toString();
		objLink[i].disabled=true;
		objLink[i].onclick = new Function("return false;");
		objLink[i].style.color ="#7f7f7f";
		objLink[i].style.background ="#eeeeee";
	}
}

function enablelinks() {
	var objLink = document.links;
	for(var i=0;i < objLink.length;i++) {
		objLink[i].disabled=false;
		objLink[i].href=linkArray[i];
		objLink[i].onclick=linkArray[i];
		objLink[i].style.color ="#000000";
		objLink[i].style.background = "";
	}
}

function setMenuItemState(menuid,index,enable)  {
	var objList = document.getElementById(menuid).getElementsByTagName("li");
	if (objList.length==0)
		objList = document.getElementById(menuid).getElementsByTagName("TR");

	var link=objList[index].getElementsByTagName("a")[0];

	if (enable==undefined)
		enable=0;

	setLinkState(link,enable);
}

function setMenuItemsState(menuid,name,enable)  {
	var objList = document.getElementsByName(name);
	if (objList.length>0) {
		if (enable==undefined)
			enable=0;
		for (var i=0; i<objList.length ; ++i) {
			var link=objList[i].getElementsByTagName("a")[0];
			setLinkState(link,enable);
		}
	}
}

function setLinkState(link,enable) {
	switch (enable) {
		case 0:
			if (link.disabled==true) break;
			linkArray[link]=link.href.toString();
			link.disabled=true;
			link.onclick=new Function("return false;");
			link.style.color ="#7f7f7f";
			link.style.background ="#eeeeee";
			break;
		default:
			if (link.disabled==false) break;
			link.disabled=false;
			if (linkArray[link]!=undefined) {
				link.href=linkArray[link];
				link.onclick=linkArray[link];
			}
			link.style.color ="#000000";
			link.style.background = "";
			break;
	}
}

function loadicons(page) {
  var div='divicons';
  if ((page=="") || (page==undefined)) return;
  xmlhttpget("/cgi-bin/pxe/getpcicons.cgi?" + page,'eval',document.getElementById(div).innerHTML);
}

function reloadicons(page) {
  if ((page=="") || (page==undefined)) return;
  xmlhttpget("/cgi-bin/pxe/getpcicons.cgi?" + page + "&reload",'eval');
}

function storepcstyle(pclist) {

  nodrag=1;

  var xhr_object = null;
  var querystring = "" ;

  if(window.XMLHttpRequest) // Firefox
          xhr_object = new XMLHttpRequest();
  else if(window.ActiveXObject) // Internet Explorer
         xhr_object = new ActiveXObject("Microsoft.XMLHTTP");
  else {
         alert("Votre navigateur ne supporte pas les objets XMLHTTPRequest...");
         return;
  }

  if (pclist!=undefined) {
  	pc=pclist[0];
	querystring='pc' + pc + '=' + escape(pcStyle[pc]);
  	for (var i=1; i<pclist.length; ++i) {
	  	pc=pclist[i];
		querystring+='&pc' + pc + '=' + escape(pcStyle[pc]);
	}
  } else {

	  var first=1;
	  var i=1;
	  while (i<pcStyle.length) {

	    if (pcStyle[i]!=undefined) {

	      if (first) {
		querystring='pc' + i + '=' + escape(pcStyle[i]);
		first=0;
	      } else {
		querystring+='&pc' + i + '=' + escape(pcStyle[i]);
	      }

	    }

	    i++;
	}
  }

  xhr_object.open("POST", "/cgi-bin/pxe/storepcstyle.cgi", true);

//  document.getElementById('divlog').innerHTML='';
  xhr_object.onreadystatechange = function() {
        if(xhr_object.readyState == 4) {
		document.getElementById('divlog').innerHTML+=xhr_object.responseText;
  		nodrag=0;
	}
  }
  xhr_object.setRequestHeader=('Content-Type', 'application/x-www-form-urlencoded');
  xhr_object.send(querystring);

}

function previewmap() {
//  netscape.security.PrivilegeManager.enablePrivilege('UniversalFileRead');
  document.getElementById('divmappreview').innerHTML='<img src="file://' + document.forms['mapupload'].newmap.value + '">';
}

function innerHTML_save(id) {
        var element=document.getElementById(id);
        innerHTML_backup[id]=element.innerHTML;
	return element;
}

function innerHTML_restore(id) {
	var element=document.getElementById(id);
	if (innerHTML_backup[id]!=undefined) {
		element.innerHTML=innerHTML_backup[id];
	} else {
		element.innerHTML='';
	}
	return element;
}

function divedit(id,filename) {
	var div=innerHTML_save(id);
	xmlhttpget('/cgi-bin/pxe/editfile.cgi?file=' + filename + '&div=' + id,id);
}

function divedit_init(subdir) {
	xmlhttpget('/cgi-bin/pxe/editfile.cgi?list=' + subdir,'eval');
}

function divedit_menu_build(subdir) {
	var i;
	var select;

	select=document.getElementById('diveditmenu');

	i=select.length;
	while (i-- > 0) select.remove(0);

	i=0;
	while (i<divedit_menu.length) {
		var opt=document.createElement('option');
		opt.text=divedit_menu[i];
		select.add(opt,null);
		++i;
	}
	showfile(select,divedit_file[select.selectedIndex],'editor_window');
}

function showfile(select,editor_filename,editor_window) {
	if (table_edit_td!=undefined) {
		table_edit_td.innerHTML=table_edit_backup;
		table_edit_td=undefined;
	}
	var id=innerHTML_save(editor_window);
	xmlhttpget('/cgi-bin/pxe/loadfile.cgi?file=' + divedit_file[select.selectedIndex] + '&div=' + editor_window,editor_window);

}

function editfile(select,editor_filename,editor_window) {
	if (table_edit_td!=undefined) {
		table_edit_td.innerHTML=table_edit_backup;
		table_edit_td=undefined;
	}
	var id=innerHTML_save(editor_window);
//	var div=document.getElementById(editor_filename);
//	div.innerHTML=divedit_menu[select.selectedIndex];
	divedit(editor_window,divedit_menu[select.selectedIndex]);
}

function table_edit(td,width,validate) {
	var content=td.innerHTML;
	if (table_edit_td!=undefined) {
		if (table_edit_td==td) {
			return;
		}
//		table_edit_td.innerHTML=table_edit_td.childNodes[0].value;
		table_edit_td.innerHTML=table_edit_backup;
	}
	table_edit_backup=content;
	table_edit_td=td;
	table_edit_validate=validate;
	td.innerHTML='<input class="editable" type="text" style="width: '+width+';" onkeypress="return table_edit_keypress(this,event)" />'
	td.childNodes[0].value=content;
	td.childNodes[0].focus();
}

function table_edit_keypress(_this,event) {

	var unicode=event.charCode? event.charCode : event.keyCode ;
	if (unicode==13 || unicode==9) {
		if (eval(table_edit_validate)) {
			table_edit_td.innerHTML=table_edit_td.childNodes[0].value;
			table_edit_td=undefined;
		}
		return false;
	}
	if (unicode==27) {
		table_edit_td.innerHTML=table_edit_backup;
		table_edit_td=undefined;
		return false;
	}

	return true;
}

function pcadd(_this,hostsmacIndex) {
	_this.value=trim(_this.value);
	if (_this.value.match(/^[0-9]+/)) {
		addmachine_table_edit_td=table_edit_td;
		addmachine_hostsmacIndex=hostsmacIndex;
		xmlhttpget('/cgi-bin/pxe/addmachine.cgi?pc=' + _this.value  + '&name=' + escape(hostsmac[hostsmacIndex][0]),'eval',undefined,'addmachine_callback('+_this.value+');');
		return true;
	} else {
		return false;
	}
}

function addmachine_callback(pc) {

	if (addmachine_ok==false) {
		table_edit(addmachine_table_edit_td,24,'pcadd(table_edit_td.childNodes[0],addmachine_hostsmacIndex)');
		table_edit_backup='';
		return;
	}

	pcmac[pc]=hostsmac[addmachine_hostsmacIndex][0];
	pcname[pc]=hostsmac[addmachine_hostsmacIndex][1];
	pcip[pc]=hostsmac[addmachine_hostsmacIndex][2];
	pcStyle[pc]='left: ' + (mousex-24)  + 'px; top: ' + (mousey-24) + 'px;';
	selection[pc]=0;
	hostsmac_remove(hostsmac[addmachine_hostsmacIndex][0]);

	document.getElementById('divicons').innerHTML+='<img src="/pxe/thumbs/pc'+pc+'.png" name="machine'+pc+'" border="0" style="position: absolute; '+pcStyle[pc]+'cursor : move;">';
	var TRANSPARENT_SELECTION='/pxe/pics/transparent.png';
	document.getElementById('divicons').innerHTML+='<img class="pcIcon" name="selection'+pc+'" src="/pxe/pics/transparent.png" onmousedown="if (event.ctrlKey) {SimpleContextMenu._show(event); return false;} else {dragStart(event,'+pc+',selectionGroup(this));}" onmouseover="AffBulle(getpcbull('+pc+'));" onmouseout="HideBulle();" border="0" style="position: absolute; '+pcStyle[pc]+' cursor: move;">';
	addmachine_table_edit_td.innerHTML='<img class="pcIcon" src="/pxe/thumbs/pc'+pc+'_24x24.png" name="thumb'+pc+'" border="0">';
	addmachine_table_edit_td.ondblclick="";
	dragStart(null,pc,new Array(document.getElementsByName('selection'+pc)[0]));
	showpclist();
}

function getElementAttribute(el,attrName) {

	var value=eval("el."+attrName);

	if (value!=undefined) {
		return value;
 	}

	for (var i=0; i<el.attributes.length ; ++i) {
		if (el.attributes[i].nodeName!=attrName) continue;
		return el.attributes[i].value;
	}
	return '';
}

function nameOf(el) {
	if (el.name==undefined) {
		for (var i=0; i<el.attributes.length ; ++i) {
			if (el.attributes[i].nodeName!="name") continue;
			return el.attributes[i].value;
		}
		return '';
	}
	return el.name;
}

function numSuffix(el) {
	return parseInt(nameOf(el).replace(/[a-zA-Z]+/,''),10);
}

function strSuffix(el) {
	return nameOf(el).replace(/[a-zA-Z]+/,'');
}

function switchIconMode() {
	if (iconMode=='default') {
		iconMode='register';
		HideBulle();
		IB.enable=false;
	} else {
		if (table_edit_td!=undefined) {
			table_edit_td.innerHTML=table_edit_backup;
			table_edit_td=undefined;
		}
		iconMode='default';
		IB.enable=_IBenable;
	}
	setIconMode(iconMode);

}

function menuItemsEnable(name) {
	var itemlist=document.getElementsByName(name);
	for (var i=0; i<itemlist.length ; ++i) {
		setLinkState(itemlist[i].childNodes[0],1);
	}
}

function menuItemsDisable(name) {
	var itemlist=document.getElementsByName(name);
	for (var i=0; i<itemlist.length ; ++i) {
		setLinkState(itemlist[i].childNodes[0],0);
	}
}

function enableInfobulles() {
	var item=document.getElementsByName('switchInfobulles');
 	for (var i=0; i<item.length ; ++i) {
		item[i].innerHTML='<a href="javascript:disableInfobulles()">D&eacute;sactiver les Infobulles</a>';
	}
        _IBenable=true;
	IB.enable=true;
}

function disableInfobulles() {
	var item=document.getElementsByName('switchInfobulles');
 	for (var i=0; i<item.length ; ++i) {
		item[i].innerHTML='<a href="javascript:enableInfobulles()">Activer les Infobulles</a>';
	}
	HideBulle();
        _IBenable=false;
	IB.enable=false;
}

function setIconMode(mode) {
	switch(mode) {
		case 'default':
			busy();
			loadicons('default');
			SimpleContextMenu.attach('pcIcon', 'menu1',menuUpdate);
			SimpleContextMenu.attach('map', 'menu1b',menuUpdate);
			xmlhttpget('/cgi-bin/pxe/loadglobals.cgi','eval',undefined,'ready();');
			reloadIconsInterval=setInterval("reloadicons('default')",10000);
			loadGlobalsInterval=setInterval("xmlhttpget('/cgi-bin/pxe/loadglobals.cgi?','eval');",10000);
			break;
		case 'register':
			busy();
			clearInterval(reloadIconsInterval);
			clearInterval(loadGlobalsInterval);
			loadicons('register');
			xmlhttpget('/cgi-bin/pxe/loadglobals.cgi','eval',undefined,'ready();');
			SimpleContextMenu.attach('pcIcon', 'menu2',menuUpdate);
			SimpleContextMenu.attach('map', 'menu2b',menuUpdate);
			break;

	}
}

var t;
function showpclist() {
	if (iconMode=='default' && pcname.length==0) {
		switchIconMode();
		return;
	}
	pclist('pctable',(iconMode=='default')?false:true);
//	if (t==undefined) {
		var height=document.body.clientHeight-document.getElementById('roomName').clientHeight-4;
		t=new SortableTable(document.getElementById("pclist"),height);
		t.skipTrailingTR=1;
		t=new ScrollableTable(document.getElementById("pclist"),height);
//	}
}

function mapclick(event) {
	if (!enableclick) return;
	if (event.ctrlKey) {
		SimpleContextMenu._show(event);
		event.preventDefault();
		return false;
	} else {
		SimpleContextMenu._hide(event);
		mapselrect.init(event,mapselrect);
	}
}

function pcremove(pc) {
	var msg="";
	var count=0;
	var cgiparms="";
	var last;
	var pclist=new Array();

	last=pc;

	if (pc==undefined) {
		for (pc=1; pc<selection.length; ++pc) {
			if (selection[pc]==1) {
				msg+=pcname[pc]+"\n";
				if (count) {
					cgiparms+="&pc="+pc;
				} else {
					cgiparms+="pc="+pc;
				}
				++count;
				last=pc;
				pclist.push(pc);
			}
		}
	} else {
		pclist.push(pc);
		cgiparms="pc="+pc;
	}

	if (count>1) {
		msg="Etes-vous certain de bien vouloir enlever du plan ces " + count + " machines ?\n"+msg;
	} else {
		pc=last;
		msg="Etes-vous certain de bien vouloir enlever du plan " +pcname[pc]+" ("+pc+") ?";
	}

	if (!confirm(msg)) {
		return;
	}
	busy();
	xmlhttppost('/cgi-bin/pxe/pcremove.cgi?',cgiparms,'eval','','pcremove_callback('+pclist+')');

}


function pcremove_callback() {
	for (var i=0; i<arguments.length; ++i) {
		_pcremove_callback(arguments[i]);
	}
	loadicons(iconMode);
	for (var i=0; i<arguments.length; ++i) {
		document.getElementById('divicons').removeChild(document.getElementsByName('selection'+arguments[i])[0]);
//		document.getElementById('divicons').removeChild(document.getElementsByName('status'+arguments[i])[0]);
		document.getElementById('divicons').removeChild(document.getElementsByName('machine'+arguments[i])[0]);
	}
	showpclist();
	ready();
}

function _pcremove_callback(pc) {

	hostsmac.push(new Array(pcmac[pc],pcname[pc],pcip[pc]));
	selection[pc]=undefined;
	pcname[pc]=undefined;
	pcmac[pc]=undefined;
	pcip[pc]=undefined;
	pcpartitionssaved[pc]=undefined;
	pcdatesaved[pc]=undefined;
	pcdaterestored[pc]=undefined;
	pcdatebackuped[pc]=undefined;
	pcimagetorestore[pc]=undefined;
	pcdiskspaceleft[pc]=undefined;
	pcuptime[pc]=undefined;
}

function hostsmac_remove(mac) {
	for (var i=0; i<hostsmac.length ; ++i) {
		if (hostsmac[i][0]==mac) {
			hostsmac.splice(i,1);
			return;
		}
	}
}

function toggleColumns(what) {
	var menu=document.getElementById('menu3');
	var links=menu.getElementsByTagName('A');
	var col;

	for (col=0; col<pclistColumn.length;++col) {
		if (pclistColumn[col]==what)
			break;
	}

	toggleIcon('checkmark.png',new RegExp(/checkmark.png/),links[col].getElementsByTagName('img')[0]);
	showColumn[col]=1-showColumn[col];
	showpclist();

}

function setMenuIcon(menuId,index,src) {
	var img=document.getElementById(menuId).getElementsByTagName('li')[index].getElementsByTagName('img')[0];

	img.src=src;
	img.style.display="block";
}

function setMenuItemLink(menuId,index,href) {
	var link=document.getElementById(menuId).getElementsByTagName('li')[index].getElementsByTagName('a')[0];

	link.href=href;
}

function toggleMenuIcon(menuId,index,src,re) {
	var menu=document.getElementById(menuId);
	var img=menu.getElementsByTagName('a')[index].getElementsByTagName('img')[0];
//	var img=links[index].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0];
	toggleIcon(src,re,img);

}

function toggleIcon(_src,re,img) {
	var src=getElementAttribute(img,'src');
	if (src.match(re)!=null) {
		img.src="/pxe/pics/nomark.png";
	} else {
		img.src="/pxe/pics/"+_src;
	}
}

function setItalic(e,italic) {
	e.style.fontStyle=(italic==true || italic==1)?'italic':'normal';
}
function toggleItalic(e) {
	e.style.fontStyle=(e.style.fontStyle=="italic")?'normal':'italic';
}
function toggleDisplay(e) {
	e.style.display=(e.style.display=="none")?'block':'none';
}

function toggleClass(e) {
	nodeList[i].class=class+'|hidden';
}

function menuUpdate(showMenu) {

	if (showMenu==false) {
		IB.enable=_IBenable;
	} else {
		var count=0;
		var len=selection.length;
		for (var i=1; i<selection.length ; ++i) {
			if (selection[i]==undefined) {
				--len;
				continue;
			}
			if (selection[i]==1)
				++count;
		}
		if (count<1) {
			menuItemsDisable('contextSel');
			menuItemsEnable('contextToSel');
		} else {
			menuItemsEnable('contextSel');
			if (count<len-1) {
				menuItemsEnable('contextToSel');
			} else {
				menuItemsDisable('contextToSel');
			}
		}
	        HideBulle();
	        var link;
	        IB.enable=false;
	        var pc=numSuffix(SimpleContextMenu._attachedElement);
		var menu=SimpleContextMenu._menuElement.id;
		setMenuItemsState(menu,"invertSel",pcname.length);
		switch(menu) {
			case 'menu1':
				document.getElementsByName('contextPC')[0].innerHTML=pcname[pc]+' ('+pc+')';
				document.getElementsByName('contextOn')[0].innerHTML='Allumer '+pcname[pc]+' ('+pc+')';
				document.getElementsByName('contextOff')[0].innerHTML='Eteindre '+pcname[pc]+' ('+pc+')';
				document.getElementsByName('contextSave')[0].innerHTML='Sauvegarder '+pcname[pc]+' ('+pc+')';
				document.getElementsByName('contextRestore')[0].innerHTML='Restaurer '+pcname[pc]+' ('+pc+')';
				document.getElementsByName('contextMap')[0].innerHTML=(mapdisplay?"Cacher":"Afficher")+" le Plan";
				document.getElementsByName('contextPClist')[0].innerHTML=(pclistdisplay?"Cacher":"Afficher")+" la Liste";
				break;

			case 'menu1b':
				document.getElementsByName('contextMap2')[0].innerHTML=(mapdisplay?"Cacher":"Afficher")+" le Plan";
				document.getElementsByName('contextPClist2')[0].innerHTML=(pclistdisplay?"Cacher":"Afficher")+" la Liste";
				break;

			case 'menu2':
				document.getElementsByName('contextRemove')[0].innerHTML='Enlever '+pcname[pc]+' ('+pc+')';
				break;

			case 'menu2b':
				break;

			case 'menu3':
				link=SimpleContextMenu._menuElement.getElementsByTagName('a');
				for(i=0; i<showColumn.length; ++i)
					setItalic(link[i],1-showColumn[i]);
				break;

			case 'menu4':
				document.getElementsByName('contextPcIcon')[0].innerHTML='<img border="0" class="pcIcon" src="/pxe/thumbs/pc'+pc+'_24x24.png">';
				document.getElementsByName('contextPcName')[0].innerHTML=pcname[pc]+' ('+pc+')';
				setMenuItemState(menu,0,0);
				setMenuItemState(menu,1,0);
				setMenuItemState(menu,3,0);
				if (savlist.length==0) {
					xmlhttpget('/cgi-bin/pxe/savlist.cgi','eval','','buildSavList('+pc+')');
				} else {
					buildSavList(pc);
				}
				document.getElementById('srcList').innerHTML='';
				if (partitionrestore[pc]==undefined) {
					if (partitionsave[pc]==undefined) {
						xmlhttpget('/cgi-bin/pxe/partlist.cgi?what=save&pc='+pc,'eval');
					}
					xmlhttpget('/cgi-bin/pxe/partlist.cgi?what=restore&pc='+pc,'eval','','buildPartList('+pc+',"restore")');
				} else {
					buildPartList(pc,"restore");
				}

				setMenuItemState(menu,5,pcrestorembr[pc]);
				setMenuItemState(menu,6,pcrestoresf[pc]);
				break;

			case 'menu5':
				document.getElementsByName('contextPcIcon')[1].innerHTML='<img border="0" class="pcIcon" src="/pxe/thumbs/pc'+pc+'_24x24.png">';
				document.getElementsByName('contextPcName')[1].innerHTML=pcname[pc]+' ('+pc+')';
				setMenuItemState(menu,0,0);
				setMenuItemState(menu,1,0);
				setMenuItemState(menu,3,0);
				setMenuItemLink(menu,4,"javascript:td_click('destlist',"+pc+",-1)");
				if (pcsavepath[pc]==undefined) {
					setMenuIcon(menu,4,'/pxe/pics/checkmark.png');
				} else {
					setMenuIcon(menu,4,'/pxe/pics/nomark.png');
				}
				document.getElementById('partList').innerHTML='';
				document.getElementById('destList').innerHTML='';
				if (partitionsave[pc]==undefined) {
					xmlhttpget('/cgi-bin/pxe/partlist.cgi?what=save&pc='+pc,'eval','','buildPartList('+pc+',"save")');
				} else {
					buildPartList(pc,"save");
				}
				break;

			case 'menu6':
				setMenuItemState(menu,0,0);
				var t=document.getElementById('pxeconfig');
				var html='';
				var checkmark;
				var ismac=false;
				var selpc=new Array;

				for (var j=1; j<selection.length ; ++j) {
					if (selection[j]==1) selpc.push(new Array(j,false));
				}
			 	if (selpc.length>0) {
			 		if (selpc.length==1) {
			 			pc=selpc[0][0];
			 		} else {
				 		pc='selection';
				 	}

			 	} else {
					pc=strSuffix(SimpleContextMenu._attachedElement);
					for (var k=0 ; k<hostsmac.length ; ++k) {
						if (hostsmac[k][0]==pc) {
							ismac=true;
							break;
						}
					}
				}
				if (ismac==true) {
					for (var i=0; i<pxeconfig.length ; ++i) {
							checkmark=(pxeconfig[i]==hostsmac[k][3])||(hostsmac[k][3]==undefined && pxeconfig[i]=='default');
							html+='<tr><td><a href="javascript:td_click('+"'pxeconfig','"+pc+"',"+i+')"><table cellpadding="0" cellspacing="0"><tr><td><img border="0" src="/pxe/pics/'+((checkmark)?'check':'no')+'mark.png"></td><td>'+pxeconfig[i]+'</td></tr></table></a></td></tr>';
					}
				} else {
					if (selpc.length==0) {
						pc=parseInt(pc,10);
					}
					for (var i=0; i<pxeconfig.length ; ++i) {
							checkmark=(selpc.length<=1)&&((pxeconfig[i]==pcpxeconfig[pc])||(pcpxeconfig[pc]==undefined && pxeconfig[i]=='default'));
							html+='<tr><td><a href="javascript:td_click('+"'pxeconfig','"+pc+"',"+i+')"><table cellpadding="0" cellspacing="0"><tr><td><img border="0" src="/pxe/pics/'+((checkmark)?'check':'no')+'mark.png"></td><td>'+pxeconfig[i]+'</td></tr></table></a></td></tr>';
					}
				}

				t.innerHTML=html;
				break;
		}
	}
}

function buildSavList(pc) {
	var checkmark0=0;
	var html='<tr><td><a name="savelist00" class="savlist" href="javascript:td_click('+"'savlist',"+pc+","+i+')"><table cellspacing="0" cellpadding="0" style="border-style: none; border-width: 0px;"><tr><td><img border="0" src="/pxe/pics/'+((checkmark0)?'check':'no')+'mark.png"></td><td>Disque &agrave; Disque</td></tr></table></a></td></tr>';
	html="";
	for (var i=0; i<savlist.length ; ++i) {
		var checkmark=(savlist[i]==pcimagetorestore[pc]);
		var name=savlist[i].replace(/ .*/,'');
		var date=savlist[i].replace(/^[^\s]+\s/,'');
		html+='<tr><td><a name="savlist'+i+'" class="savlist" href="javascript:td_click('+"'savlist',"+pc+","+i+')"><table cellspacing="0" cellpadding="0" style="border-style: none; border-width: 0px;"><tr><td><img border="0" src="/pxe/pics/'+((checkmark)?'check':'no')+'mark.png"></td><td>'+savlist[i]+'</td></tr></table></a></td></tr>';
	}
	document.getElementById('restorePath').innerHTML=html;
}

function buildPartList(pc,what) {

	var html="";
	var html2="";

	switch (what) {
		case 'save':
			for (var i=0; i<partitionsave[pc].length ; ++i) {
				var checkmark=partitionsave[pc][i][1];
				var checkmark2=(pcsavepath[pc]==partitionsave[pc][i][0]);
				html+='<tr><td align="left">'+ '<a name="partlist'+i+'" class="partlist" href="javascript:td_click('+"'partlist',"+pc+","+i+",'"+what+"'"+')"><table cellspacing="0" cellpadding="0"><tr><td><img style="border-style: none;" src="/pxe/pics/'+ ((checkmark==1)?'check':'no')+'mark.png"></td><td>'+partitionsave[pc][i][0]+'</td></tr></table></a></td></tr>';
				html2+='<tr><td align="left"><a name="destlist'+i+'" class="destlist" href="javascript:td_click('+"'destlist',"+pc+","+i+')"><table cellspacing="0" cellpadding="0"><tr><td><img style="border-style: none;" src="/pxe/pics/'+ (checkmark2?'check':'no')+'mark.png"></td><td>'+partitionsave[pc][i][0]+'</td></tr></table></a></td></tr>';
			}
			document.getElementById('partList').innerHTML=html;
			document.getElementById('destList').innerHTML=html2;
			for (var i=0; i<partitionsave[pc].length ; ++i) {
				if (pcsavepath[pc]==partitionsave[pc][i][0]) {
					setLinkState(document.getElementsByName('partlist'+i)[0],0);
//				} else {
//					setLinkState(document.getElementsByName('partlist'+i)[0],1);
				}
				if (partitionsave[pc][i][1]==1) {
					setLinkState(document.getElementsByName('destlist'+i)[0],0);
				}
			}
			break;

		case 'restore':
		// TODO
			// must be the partitions from pcimagetorestore/partitions.restore
			for (var i=0; i<partitionrestore[pc].length ; ++i) {
				var checkmark=partitionrestore[pc][i][1];
				html+='<tr><td align="left"><a name="partlist'+i+'" class="partlist2" href="javascript:td_click('+"'partlist',"+pc+","+i+",'"+what+"'"+')"><table cellspacing="0" cellpadding="0"><tr><td><img style="border-style: none;" src="/pxe/pics/'+((checkmark==1)?'check':'no')+'mark.png"></td><td>'+partitionrestore[pc][i][0]+'</td></tr></table></a></td></tr>';
			}
			// must be the partitions from /pxe/image/mac/partitions.save
			for (var i=0; i<partitionrestore[pc].length ; ++i) {
				var checkmark2=(partitionrestore[pc][i][0]==pcimagetorestore[pc]);
				html2+='<tr><td align="left"><a name="srclist'+i+'" class="srclist" href="javascript:td_click('+"'srclist',"+pc+","+i+')"><table cellspacing="0" cellpadding="0"><tr><td><img style="border-style: none;" src="/pxe/pics/'+ (checkmark2?'check':'no')+'mark.png"></td><td>'+partitionrestore[pc][i][0]+'</td></tr></table></a></td></tr>';
			}
//			document.getElementById('partList2').innerHTML=html;
			document.getElementById('srcList').innerHTML=html2;
			for (var i=0; i<partitionrestore[pc].length ; ++i) {
//				if (pcimagetorestore[pc]==partitionrestore[pc][i][0]) {
//					setLinkState(document.getElementsByName('partlist'+i)[0],0);
//				} else {
//					setLinkState(document.getElementsByName('partlist'+i)[0],1);
//				}
				if (partitionsave[pc][i][1]==1) {
					setLinkState(document.getElementsByName('srclist'+i)[0],0);
				}
			}
			break;
	}

}

function td_click(classname) {

	busy();

	switch(classname) {
		case "savlist":
			var pc=arguments[1];
			var i=arguments[2];
			xmlhttpget("/cgi-bin/pxe/set_restorepath.cgi?pc="+pc+"&sav="+savlist[i].replace(/\ /g,'_'),"eval",'','set_restorepath_callback("savlist",'+pc+','+i+')');
			break;

		case "srclist":
			var pc=arguments[1];
			var i=arguments[2];
			// must be the partitions from /pxe/image/mac/partitions.save
			xmlhttpget("/cgi-bin/pxe/set_restorepath.cgi?pc="+pc+"&path="+(partitionrestore[pc][i][0]), "eval",'','set_restorepath_callback("srclist",'+pc+','+i+')');
			break;

		case "destlist":
			var pc=arguments[1];
			var i=arguments[2];
			if (i>=0 && partitionsave[pc][i][1]==1)
				break;
			xmlhttpget("/cgi-bin/pxe/set_savepath.cgi?pc="+pc+"&path="+((i==-1)?"":partitionsave[pc][i][0]), "eval",'','set_savepath_callback('+pc+','+i+')');
			break;

		case "partlist":
			var pc=arguments[1];
			var i=arguments[2];
			var what=arguments[3];
			switch (what) {
				case 'save':
					if (pcsavepath[pc]==partitionsave[pc][i][0])
						break;
					xmlhttpget("/cgi-bin/pxe/toggle_partition.cgi?what=save&pc="+pc+"&partition="+partitionsave[pc][i][0]+"&enable="+(1-partitionsave[pc][i][1]), "eval",'','toggle_partition_callback("save",'+pc+','+i+')');
					break;
				case 'restore':
					if (pcimagetorestore[pc]==partitionrestore[pc][i][0])
						break;
					xmlhttpget("/cgi-bin/pxe/toggle_partition.cgi?what=restore&pc="+pc+"&partition="+partitionrestore[pc][i][0]+"&enable="+(1-partitionrestore[pc][i][1]), "eval",'','toggle_partition_callback("restore",'+pc+','+i+')');
					break;
			}
			break;

		case "pxeconfig":
			var pc=arguments[1];
			var i=arguments[2];
			var selpc=new Array;
			var data='';

			for (var j=1; j<selection.length ; ++j) {
				if (selection[j]==1) selpc.push(new Array(j,false));
			}
			if (!selpc.length) {
			  	var ismac=false;
				for (var k=0 ; k<hostsmac.length ; ++k) {
					if (hostsmac[k][0]==pc) {
						ismac=true;
						pc=k;
						break;
					}
				}
				if (!ismac) {
					pc=parseInt(pc,10);
				}
				selpc.push(new Array(pc,ismac));
			}

			for (var j=0; j<selpc.length; ++j) {

				pc=selpc[j][0];
				if (!selpc[j][1]) {
					if (pcpxeconfig[pc]==pxeconfig[i]) {
						continue;
					}
					mac=pcmac[pc];

				} else {
					if (hostsmac[pc][3]==pxeconfig[i]) {
						continue;
					}
					mac=hostsmac[pc][0];
				}

				data+=(j>0?'&':'')+mac+'=on&cfg.'+mac+'='+pxeconfig[i];
			}

			if (data!='') {
				xmlhttppost("/cgi-bin/pxe/set_pxeconfig.cgi",data,'eval','','setpxeconfig_callback('+selpc+','+i+')');
			}
			break;
	}

}

function setpxeconfig_callback() {
	i=arguments[arguments.length-1];
	var k=0;
	var pc;
	var ismac;
	for (var j=0; j<arguments.length-1 ; j+=2) {
		pc=arguments[j];
		ismac=arguments[j+1]
		if (ismac) {
			hostsmac[pc][3]=pxeconfig[i];
		} else {
			pcpxeconfig[pc]=pxeconfig[i];
		}
	}
	showpclist();
	ready();
}

function bpxe(action,what) {

	var el;

	switch(what) {
		case 'map':
			el=document.getElementById('mapdiv').parentNode;
			break;
		case 'list':
			el=document.getElementById('cartouche').parentNode;
			break;
	}

	switch(action) {
		case 'show':
			el.style.display='block';
			break;

		case 'hide':
			el.style.display='none';
			break;
	}
}

function onlymap() {
	bpxe('hide','list');
	bpxe('show','map');
	pclistdisplay=false;
	mapdisplay=true;

}

function onlylist() {
	bpxe('hide','map');
	bpxe('show','list');
	var ltd=document.getElementById('cartouche').parentNode;
	ltd.style.position='relative';
	ltd.style.top='';
	ltd.style.left='';
	pclistdisplay=true;
	mapdisplay=false;
}

function mapandlist() {
	bpxe('show','map');
	var img=document.getElementById('map');
	var ltd=document.getElementById('cartouche').parentNode;
	ltd.style.position='relative';
	ltd.style.top='-'+(img.clientHeight)+'px';
	ltd.style.left=img.clientWidth+'px';
 	bpxe('show','list');
	pclistdisplay=true;
	mapdisplay=true;
}

function set_restorepath_callback(what,pc,i) {
	switch(what) {
		case 'savlist':
			if (savlist[i]!=null && savlist[i]!=undefined)
				pcimagetorestore[pc]=savlist[i];
			break;
		case 'srclist':
			// must be the partitions from /pxe/image/mac/partitions.save
			if (partitionrestore[pc][i][0]!=null && partitionrestore[pc][i][0]!=undefined)
				pcimagetorestore[pc]=partitionrestore[pc][i][0];
			break;
	}
	showpclist();
	ready();
}

function set_savepath_callback(pc,i) {
	if (i==-1) {
		pcsavepath[pc]=undefined;
	} else {
		pcsavepath[pc]=partitionsave[pc][i][0];
	}
	showpclist();
	ready();
}

function toggle_partition_callback(what,pc,i) {
	switch (what) {
		case 'save':
			partitionsave[pc][i][1]=1-partitionsave[pc][i][1];
			break;
		case 'restore':
			partitionrestore[pc][i][1]=1-partitionrestore[pc][i][1];
			break;
	}
	showpclist();
	ready();
}

function movie_setvol(vol,pc) {

	var query="";
	var pcl=new Array;

	if (pc==undefined) {
		var one=0;
		for (var pc=1; pc<selection.length; ++pc) {
			if (selection[pc]==1) {
				query+=(one==1?'&':'')+'pc='+pc;
				one=1;
				pcl.push(pc);
			}

		}

	} else {
		query='pc='+pc;
		pcl.push(pc);
	}
		xmlhttpget('/cgi-bin/pxe/movie_setvol.cgi?'+query+'&vol='+vol,'eval','','movie_setvol_callback('+vol+','+pcl.toString()+')');

}

function movie_setvol_callback(vol) {
	for (i=1; i<arguments.length; ++i) {
		pcsoundvol[arguments[i]]=vol;
	}
	showpclist();
}

function guixbox_pause() {
		if (!selected_something()) {
			pcclickall(1);
		}
                action('pause');
}

function guixbox_unpause() {
		if (!selected_something()) {
			pcclickall(1);
		}
                action('unpause');
}
function guixbox_mute() {
		if (!selected_something()) {
			pcclickall(1);
		}
                action('mute');
}

function guixbox_unmute() {
		if (!selected_something()) {
			pcclickall(1);
		}
                action('unmute');
}

function selected_something() {
        for( var pc=1 ; pc<pcname.length ; pc++) {
                if (selection[pc]==undefined) {
                        continue;
                }
		if (selection[pc]==1) {
			return true;
		}
	}
	return false;
}

var mapdisplay=true;
function togglemap() {
	if (mapdisplay) {
		onlylist();
	} else {
		if (pclistdisplay) {
			mapandlist();
		} else {
			onlymap();
			return;
		}
	}
	showpclist();
}

var pclistdisplay=true;
function togglepclist() {
        if (pclistdisplay) {
                onlymap();
		return;
        } else {
                if (mapdisplay) {
                        mapandlist();
                } else {
                        onlylist();
                }
        }
	showpclist();
}
