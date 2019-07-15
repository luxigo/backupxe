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
// Global object to hold drag information.

var dragObj = new Object();
dragObj.id = 0;
dragObj.zIndex = 0;
var mousex;
var mousey;
var nodrag=0;

 function getmousepos(event) {
  if (browser.isIE) {
    mousex = window.event.clientX + document.documentElement.scrollLeft
      + document.body.scrollLeft;
    mousey = window.event.clientY + document.documentElement.scrollTop
      + document.body.scrollTop;
  }
  if (browser.isNS) {
    mousex = event.clientX + window.scrollX;
    mousey = event.clientY + window.scrollY;
  }
}

function dragStart(event, id, el_list) {

  if (nodrag) return;
  dragObj.el_list=el_list;

  if (browser.isIE) {
  	var event=window.event;
  }
  if (event!=null && event.button!=0) return;

  var el;
  var x, y;

  // If an element id was given, find it. Otherwise use the element being
  // clicked on.

  if (id) {
    dragObj.elNode = document.getElementsByName("machine" + id)[0];
    dragObj.id = id;
   }  else {
    if (browser.isIE)
      dragObj.elNode = window.event.srcElement;
    if (browser.isNS)
      dragObj.elNode = event.target;

    // If this is a text node, use its parent element.

    if (dragObj.elNode.nodeType == 3)
      dragObj.elNode = dragObj.elNode.parentNode;
  }

  // Get cursor position with respect to the page.

  if (!event) {
	x=mousex;
	y=mousey;
  } else {
	if (browser.isIE) {
	  x = window.event.clientX + document.documentElement.scrollLeft
	    + document.body.scrollLeft;
	  y = window.event.clientY + document.documentElement.scrollTop
	    + document.body.scrollTop;
	}
	if (browser.isNS) {
		x = event.clientX + window.scrollX;
		y = event.clientY + window.scrollY;
  	}
  }

  // Save starting positions of cursor and element.

  dragObj.cursorStartX = x;
  dragObj.cursorStartY = y;
  dragObj.elStartLeft  = parseInt(dragObj.elNode.style.left, 10);
  dragObj.elStartTop   = parseInt(dragObj.elNode.style.top,  10);

  if (isNaN(dragObj.elStartLeft)) dragObj.elStartLeft = 0;
  if (isNaN(dragObj.elStartTop))  dragObj.elStartTop  = 0;

  // Update element's z-index.

  dragObj.elNode.style.zIndex = ++dragObj.zIndex;
  if (el_list!=undefined) {
  	dragObj.elStartLeft_list=new Array();
  	dragObj.elStartTop_list=new Array();
  	for(var i=0; i<el_list.length; ++i) {
  		dragObj.elStartLeft_list[i]=parseInt(el_list[i].style.left,10);
  		dragObj.elStartTop_list[i]=parseInt(el_list[i].style.top,10);
  		el_list[i].style.zIndex=++dragObj.zIndex;
  	}
  }

  // Capture mousemove and mouseup events on the page.

  if (browser.isIE) {
    document.attachEvent("onmousemove", dragGo);
    document.attachEvent("onmouseup",   dragStop);
    window.event.cancelBubble = true;
    window.event.returnValue = false;
  }
  if (browser.isNS) {
    document.addEventListener("mousemove", dragGo,   true);
    document.addEventListener("mouseup",   dragStop, true);
    if (event) {
	event.preventDefault();
    }
  }
}

function dragGo(event) {

  var x, y;

  // Get cursor position with respect to the page.

  if (browser.isIE) {
    x = window.event.clientX + document.documentElement.scrollLeft
      + document.body.scrollLeft;
    y = window.event.clientY + document.documentElement.scrollTop
      + document.body.scrollTop;
  }
  if (browser.isNS) {
    x = event.clientX + window.scrollX;
    y = event.clientY + window.scrollY;
  }

  // Move drag element by the same amount the cursor has moved.

  dragObj.elNode.style.left = (dragObj.elStartLeft + x - dragObj.cursorStartX) + "px";
  dragObj.elNode.style.top  = (dragObj.elStartTop  + y - dragObj.cursorStartY) + "px";

  pcStyle[dragObj.id] = 'left: ' + dragObj.elNode.style.left + '; top: ' + dragObj.elNode.style.top + ';';

  if (dragObj.el_list!=undefined) {
	var done=new Array();
 	done[dragObj.id]=true;
  	for (var i=0; i< dragObj.el_list.length; ++i) {
  		dragObj.el_list[i].style.left= (dragObj.elStartLeft_list[i] + x - dragObj.cursorStartX) + "px";
  		dragObj.el_list[i].style.top= (dragObj.elStartTop_list[i] + y - dragObj.cursorStartY) + "px";
		var id=numSuffix(dragObj.el_list[i]);
	  	if (done[id]==undefined) {
			pcStyle[id] = 'left: ' + dragObj.el_list[i].style.left + '; top: ' + dragObj.el_list[i].style.top + ';';
			done[id]=true;
	  	}
	}
  }

  if (browser.isIE) {
    window.event.cancelBubble = true;
    window.event.returnValue = false;
  }
  if (browser.isNS)
    event.preventDefault();
}

function dragStop(event) {

  // Stop capturing mousemove and mouseup events.

  if (browser.isIE) {
    document.detachEvent("onmousemove", dragGo);
    document.detachEvent("onmouseup",   dragStop);
  }
  if (browser.isNS) {
    document.removeEventListener("mousemove", dragGo,   true);
    document.removeEventListener("mouseup",   dragStop, true);
  }
  var id_list=new Array();
  id_list.push(dragObj.id);

  var done=new Array();
  done[dragObj.id]=true;

  if (dragObj.el_list!=undefined) {
  	for (var i=0; i< dragObj.el_list.length; ++i) {
  		var id=numSuffix(dragObj.el_list[i]);
  		if (done[id]==undefined) {
  			id_list.push(id);
  			done[id]=true;
  		}
  	}
  }
  storepcstyle(id_list);
}
