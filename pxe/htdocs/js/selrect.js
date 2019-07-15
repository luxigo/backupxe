
var selrect = new Object;

var SelRect = function (_this,id,callback) {

	this.xorig=0;
	this.yorig=0;
	this.div=id;
	this.callback=callback
	this._this=_this;
	this.zIndex=1;
	this.selrect='selrect';

	this.init=function(event,_this) {
		selrect._this=_this;

		if (event.button!=0) return;

		var x,y;
		if (!event) {
			x=mousex;
			y=mousey;
		} else {
			if (browser.isIE) {
				x = window.event.clientX + document.documentElement.scrollLeft + document.body.scrollLeft;
				y = window.event.clientY + document.documentElement.scrollTop + document.body.scrollTop;
			}
			if (browser.isNS) {
				x = event.clientX + window.scrollX;
				y = event.clientY + window.scrollY;
			}
		}

		var div=document.getElementById(_this.selrect);
		div.style.zIndex=++_this.zIndex;
		div.style.position="absolute";
		div.style.display="block";
		div.style.top=y;
		div.style.left=x;
		div.style.width=1;
		div.style.height=1;

		_this.xorig=parseInt(div.style.left,10);
		_this.yorig=parseInt(div.style.top,10);
		
		_this.callback("init");

		if (browser.isIE) {                                            
			document.attachEvent("onmousemove", _this.drag);
			document.attachEvent("onmouseup", _this.done);
			window.event.cancelBubble = true;                            
			window.event.returnValue = false;                            
		}                                                              
		if (browser.isNS) {                                            
			document.addEventListener("mousemove", _this.drag, true);      
			document.addEventListener("mouseup", _this.done, true);
		} 
		
	}

	this.drag=function (event) {
	
		var d;
		var x,y;
		
		_this=selrect._this;
		d=document.getElementById(_this.selrect);
		
		if (!event) {
			x=mousex;                                                        
			y=mousey;                                                        
		} else {                                                               
			if (browser.isIE) {                                              
				x = window.event.clientX + document.documentElement.scrollLeft + document.body.scrollLeft;                                  
				y = window.event.clientY + document.documentElement.scrollTop + document.body.scrollTop;                                  
			}                                                               
			if (browser.isNS) {                                             
				x = event.clientX + window.scrollX;                     
				y = event.clientY + window.scrollY;                     
			}                                                               
		}                          	

		var w=x-_this.xorig;
		if (w<0) {
			d.style.left=x+'px';
			d.style.width=(-w)+'px';
		} else {
			d.style.width=w+'px';
		}
		
		var h=y-_this.yorig;
		if (h<0) {
			d.style.top=y+'px';
			d.style.height=(-h)+'px';
		} else {
			d.style.height=h+'px';
		}

		_this.callback("drag");

		if (browser.isIE) {
			window.event.cancelBubble = true;
			window.event.returnValue = false;
		}

		if (browser.isNS) {
			event.preventDefault();
		}
	}

	this.done=function(event) {
		
		_this=selrect._this;
		
		_this.callback("done");

		if (browser.isIE) {
			document.detachEvent("onmousemove", _this.drag);
			document.detachEvent("onmouseup",   _this.done);
		}
		if (browser.isNS) {
			document.removeEventListener("mousemove", _this.drag,   true);
			document.removeEventListener("mouseup",   _this.done, true);
			event.preventDefault();
		}
		document.getElementById(_this.selrect).style.display="none";
	}

}
