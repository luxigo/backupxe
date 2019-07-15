
/**
*
*  Simple Context Menu
*  http://www.webtoolkit.info/
*
**/

var SimpleContextMenu = {

	// private attributes
	_menus : new Array,
	_attachedElement : null,
	_rootElement : null,
	_menuElement : null,
	_preventDefault : true,
	_preventForms : true,
	_menuUpdate : new Array,
	_stack: new Array,
	_cascadeHideId: new Array,
	_cascadeHideTimeout: new Array,
	cascadeTimeout: 400,
	cascadeColor: "#CCCCFF",


	// public method. Sets up whole context menu stuff..
	setup : function (conf) {

		if ( document.all && document.getElementById && !window.opera ) {
			SimpleContextMenu.IE = true;
		}

		if ( !document.all && document.getElementById && !window.opera ) {
			SimpleContextMenu.FF = true;
		}

		if ( document.all && document.getElementById && window.opera ) {
			SimpleContextMenu.OP = true;
		}

		if ( SimpleContextMenu.IE || SimpleContextMenu.FF ) {

			document.oncontextmenu = SimpleContextMenu._show;
			document.onclick = SimpleContextMenu._hide;

			if (conf && typeof(conf.preventDefault) != "undefined") {
				SimpleContextMenu._preventDefault = conf.preventDefault;
			}

			if (conf && typeof(conf.preventForms) != "undefined") {
				SimpleContextMenu._preventForms = conf.preventForms;
			}

		}

	},


	// public method. Attaches context menus to specific class names
	attach : function (classNames, menuId, menuUpdate) {

		if (typeof(classNames) == "string") {
			SimpleContextMenu._menus[classNames] = menuId;
		}

		if (typeof(classNames) == "object") {
			for (x = 0; x < classNames.length; x++) {
				SimpleContextMenu._menus[classNames[x]] = menuId;
			}
		}

                if (typeof(menuUpdate) == "function") {
                        SimpleContextMenu._menuUpdate[menuId]=menuUpdate;
                }

	},


	// private method. Get which context menu to show
	_getMenuElementId : function (e) {

		if (SimpleContextMenu.IE) {
			SimpleContextMenu._attachedElement = event.srcElement;
		} else {
			SimpleContextMenu._attachedElement = e.target;
		}

		while(SimpleContextMenu._attachedElement != null) {
			var className = SimpleContextMenu._attachedElement.className;

			if (typeof(className) != "undefined") {
				className = className.replace(/^\s+/g, "").replace(/\s+$/g, "")
				var classArray = className.split(/[ ]+/g);

				for (i = 0; i < classArray.length; i++) {
					if (SimpleContextMenu._menus[classArray[i]]) {
						return SimpleContextMenu._menus[classArray[i]];
					}
				}
			}

			if (SimpleContextMenu.IE) {
				SimpleContextMenu._attachedElement = SimpleContextMenu._attachedElement.parentElement;
			} else {
				SimpleContextMenu._attachedElement = SimpleContextMenu._attachedElement.parentNode;
			}
		}

		return null;

	},


	// private method. Shows context menu
	_getReturnValue : function (e) {

		var returnValue = true;
		var evt = SimpleContextMenu.IE ? window.event : e;

		if (evt.button != 1) {
			if (evt.target) {
				var el = evt.target;
			} else if (evt.srcElement) {
				var el = evt.srcElement;
			}

			var tname = el.tagName.toLowerCase();

			if ((tname == "input" || tname == "textarea")) {
				if (!SimpleContextMenu._preventForms) {
					returnValue = true;
				} else {
					returnValue = false;
				}
			} else {
				if (!SimpleContextMenu._preventDefault) {
					returnValue = true;
				} else {
					returnValue = false;
				}
			}
		}

		return returnValue;
	},

	// private method. Shows context menu
	_show : function (e,parentMenuId) {

		var menuElementId = SimpleContextMenu._getMenuElementId(e);
	
		if (menuElementId) {

			for (var i=0; i<SimpleContextMenu._stack.length;++i) {
				if (SimpleContextMenu._stack[i].id==menuElementId) {
					return SimpleContextMenu._getReturnValue(e);
				}
			}

			if (parentMenuId==undefined) {
				var cascade=false;
				SimpleContextMenu._hide();
				SimpleContextMenu._rootElement=SimpleContextMenu._attachedElement;
			} else {
				var cascade=true;
				var parentMenu=document.getElementById(parentMenuId);
				for (var i=SimpleContextMenu._stack.length-1;i>=0;--i) {
					if (SimpleContextMenu._stack[i].id==parentMenuId) {
						break;
					}
				}
				if (i+1<SimpleContextMenu._stack.length) {
					SimpleContextMenu._dohide(SimpleContextMenu._stack[i+1].id);
				}

				var parentElement=SimpleContextMenu._attachedElement;
				parentElement.style.background=SimpleContextMenu.cascadeColor;
				SimpleContextMenu._clearTimeout(menuElementId);
			}

			var m = SimpleContextMenu._getMousePosition(e);
			var s = SimpleContextMenu._getScrollPosition(e);

			SimpleContextMenu._menuElement = document.getElementById(menuElementId);
			SimpleContextMenu._stack.push(SimpleContextMenu._menuElement);
			if (cascade) {
				SimpleContextMenu._menuElement.parentMenuId=parentMenuId;
				SimpleContextMenu._menuElement.parentElement=parentElement;
				SimpleContextMenu._menuElement.style.left=parseInt(parentMenu.style.left,10)+parentMenu.clientWidth;
				//SimpleContextMenu._menuElement.style.top=parentElement.offsetTop;
				var y = m.y + s.y ;
				var y=y-((y-parseInt(parentMenu.style.top,10)-2)%parentElement.clientHeight);
				SimpleContextMenu._menuElement.style.top = y + 'px';
				SimpleContextMenu._menuElement.style.zIndex=parentMenu.style.zIndex+1;
			} else {
				SimpleContextMenu._menuElement.style.top = m.y + s.y + 'px';
				SimpleContextMenu._menuElement.style.left = m.x + s.x + 'px';
				SimpleContextMenu._menuElement.style.zIndex=9000;
			}
                        if (typeof(SimpleContextMenu._menuUpdate[menuElementId])=="function") {
                                SimpleContextMenu._menuUpdate[menuElementId](true);
                        }

			SimpleContextMenu._menuElement.style.display = 'block';

			return false;
		}

		return SimpleContextMenu._getReturnValue(e);

	},


	// private method. Hides context menu
	_hide : function (menuId) {

		if (typeof(menuId)!="string") {
			if (SimpleContextMenu._menuElement) {
				SimpleContextMenu._menuElement.style.display = 'none';
			}
			while(SimpleContextMenu._stack.length>0) {
				var menuElement=SimpleContextMenu._stack.pop();
				if (menuElement) {
					if (typeof(menuElement.parentElement)!="undefined") {
						menuElement.parentElement.style.background="";
					}
					menuElement.style.display = 'none';
				}
			}
			SimpleContextMenu._clearTimeout();

		} else {
			SimpleContextMenu._clearTimeout(menuId);
			SimpleContextMenu._cascadeHideId.push(menuId);
			SimpleContextMenu._cascadeHideTimeout.push(setTimeout('SimpleContextMenu._dohide("'+menuId+'")',SimpleContextMenu.cascadeTimeout));
		}

	},


	_dohide: function (menuId) {

		for (var i=SimpleContextMenu._stack.length-1; i>=0; --i) {
			var id=SimpleContextMenu._stack[i].id;
			if (id==menuId) {
				break
			}
		}
		if (i>=0) {
			for (var j=SimpleContextMenu._stack.length-1; j>=i; --j) {
				var menu=SimpleContextMenu._stack.pop();
				menu.style.display="none";
				menu.parentElement.style.background="";
			}
		}
		
	},


	_hidechilds: function(menuId) {

		for (var i=0; i<SimpleContextMenu._stack.length;++i) {
			if (SimpleContextMenu._stack[i].id==menuId) {
				break;
			}
		}
		if (i+1<SimpleContextMenu._stack.length) {
			menuId=SimpleContextMenu._stack[i+1].id;
		} else {
			return;
		}

		SimpleContextMenu._clearTimeout(menuId);
		SimpleContextMenu._cascadeHideId.push(menuId);
		SimpleContextMenu._cascadeHideTimeout.push(setTimeout('SimpleContextMenu._dohide("'+menuId+'")',SimpleContextMenu.cascadeTimeout));
		
	},


	_clearTimeout: function (e) {

		switch (typeof(e)) {
			case "string":
				var menuElementId=e;
				break;

			case "object":
				var menuElementId = SimpleContextMenu._getMenuElementId(e);
				break;
		
			default:
				var menuELementId=false;
		}

		for (var i=SimpleContextMenu._cascadeHideId.length-1;i>=0;--i) {
			if ((!menuElementId) || SimpleContextMenu._cascadeHideId[i]==menuElementId) {
				var timeout=SimpleContextMenu._cascadeHideTimeout[i];
				SimpleContextMenu._cascadeHideTimeout.splice(i,1);
				SimpleContextMenu._cascadeHideId.splice(i,1);
				clearTimeout(timeout);
			}
		}

		
	},

	// private method. Returns mouse position
	_getMousePosition : function (e) {

		e = e ? e : window.event;
		var position = {
			'x' : e.clientX,
			'y' : e.clientY
		}

		return position;

	},


	// private method. Get document scroll position
	_getScrollPosition : function () {

		var x = 0;
		var y = 0;

		if( typeof( window.pageYOffset ) == 'number' ) {
			x = window.pageXOffset;
			y = window.pageYOffset;
		} else if( document.documentElement && ( document.documentElement.scrollLeft || document.documentElement.scrollTop ) ) {
			x = document.documentElement.scrollLeft;
			y = document.documentElement.scrollTop;
		} else if( document.body && ( document.body.scrollLeft || document.body.scrollTop ) ) {
			x = document.body.scrollLeft;
			y = document.body.scrollTop;
		}

		var position = {
			'x' : x,
			'y' : y
		}

		return position;

	}

}


