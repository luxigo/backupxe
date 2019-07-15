var tabsPanel;

var TabsPanel = function (_this,container,tabList,urlList,callbackList) {

	this.container=		container;
	this.tabList=		(tabList==undefined)?new Array():tabList;
	this.urlList=		(urlList==undefined)?new Array():urlList;
	this.callbackList=	(callbackList==undefined)?new Array():callbacklist;
	this.tabbar=		'tabbar';
	this.tabpanel=		'tabpanel';
	this._this=		_this;

	this.activeBackground=		"#f6f6f6"; 
	this.disabledBackground=	"#efefef"; 
	this.borderStyle=		"ridge";
	this.borderWidth=		"1px";
	this.paddingRight=		"4px";
	this.tabSuffix=			"Tab";
	this.panelSuffix=		"Panel";
	this.currentTabIndex=		0;
	
	this.tabIndex=function(what) {
		for (var i=0; i<this.tabList.length; ++i) {
			if (this.tabList[i]==what) return i;
		}
		return -1;
	}

	this.click=function (event,what) {                                                                                                       

		if (what==this.tabList[this.currentTabIndex])
			return;
			
		var i=this.tabIndex(what);
		if (i<0) {
			alert("TabsPanel.tabIndex('"+what+"'): no such tab !");
			return;
		}
		
		xmlhttpget(this.urlList[i],this.tabList[i]+this.panelSuffix,undefined,'if ('+this.callbackList[i].replace(/\)$/,',"click")')+') {'+this._this+'.showActiveTab('+i+');'+this._this+'.currentTabIndex='+i+';}');
		
	}
       
       this.showActiveTab=function(index) {
       		what=this.tabList[index];
       		
		document.getElementById(what+this.panelSuffix).style.display='block';
		document.getElementById(what+this.panelSuffix).style.background=this.activeBackground;
		
      		this.hideOtherTabs(index); 		
      		
		var t=document.getElementById(what+this.tabSuffix);
		t.style.backgroundColor=this.activeBackground;                                                              
		t.style.paddingRight=this.paddingRight;                                                                  
		t.style.borderBottomStyle="none";
	} 
	
	this.hideOtherTabs=function(index) {
		var what=this.tabList[index];
		for(tab in this.tabList) {                                                                                                                           
			if (this.tabList[tab]==what || this.tabList[tab]==undefined )
 				continue;  

			var t=document.getElementById(this.tabList[tab]+this.tabSuffix);
			if ( t==undefined )
 				continue;  
			t.style.backgroundColor=this.disabledBackground;
			t.style.paddingRight=this.paddingRight;                                                                         
			t.style.borderBottomStyle=this.borderStyle;                                                                  
			var panel=document.getElementById(this.tabList[tab]+this.panelSuffix);
			panel.style.display='none';                                                                       
		}           
	
	}
	
	this.add=function(what,url,callback) {
		var i=this.tabIndex(what);
		if (i<0) {
			this.tabList.push(what);
			this.urlList.push(url);
			this.callbackList.push(callback);
			i=this.tabList.length-1;
			
			var html='<td id="'+what+this.tabSuffix+'" align="center" class="tabtable" onclick="return '+this._this+'.click(event,'+"'"+what+"'"+');" style="background-color: '+this.disabledBackground+'; border-style: '+this.borderStyle+'; border-width: '+this.borderWidth+';" > <strong>'+what+'</strong> </td>'
			document.getElementById(this.tabbar).innerHTML+=html;
			
			html='<div id="'+what+this.panelSuffix+'" class="tabtable" style="display: block ; width: 100%;"></div>';
			document.getElementById(this.tabpanel).childNodes[0].innerHTML+=html;
			
			this.setAttr(document.getElementById(this.tabpanel).childNodes[0],'colspan',this.tabList.length);
			
			var panel=document.getElementById(this.tabList[i]+this.panelSuffix);
			var tab=document.getElementById(what+this.tabSuffix);
		
			panel.style.background=this.activeBackground;
			panel.style.borderStyle="none";
			panel.parentNode.style.borderStyle=this.borderStyle;
			panel.parentNode.style.borderWidth=this.borderWidth;
			
			tab.style.paddingRight=this.paddingRight;                                                                         
			tab.style.borderRightStyle="none";
			
			if (i==this.currentTabIndex) {
				this.currentTabIndex=-1;
				setTimeout(this._this+'.click(null,"'+what+'");',0);
				panel.style.display='block';
			
				tab.style.backgroundColor=this.activeBackground;                                                              
				tab.style.borderBottomStyle="none";
	
			} else {
				panel.style.display='none';
				
				tab.style.backgroundColor=this.disabledBackground;
				tab.style.borderBottomStyle=this.borderStyle;                                                                  
			}
//			document.getElementById(this.tabpanel).childNodes[0].style.borderTopStyle="none";
			panel.parentNode.style.borderTopStyle="none";
			panel.parentNode.style.borderRightStyle="none";
			panel.parentNode.style.backgroundColor=this.activeBackground;
//			document.getElementById(this.tabpanel).childNodes[0].style.backgroundColor=this.activeBackground;
			document.getElementById(this.tabpanel).parentNode.style.backgroundColor=this.activeBackground;
			var s=new String(callback);
			setTimeout(s.replace(/\)$/,',"init")'),0);
		}
		
	}
	
	this.containerInit=function() {
		var html;
		html='<table class="tabtable" cellpadding="4" cellspacing="0" width="100%">';
		html+='<tr id="'+this.tabbar+'"></tr>';
		html+='<tr id="'+this.tabpanel+'" style="padding-top: 0px; margin: none;"><td colspan="1"></td></tr>';
		html+='</table>';
	 	
		var c=document.getElementById(this.container);
		c.innerHTML=html;
		
	}
	this.setAttr=function(obj,attr,value) {
		for (var i=0; i<obj.attributes.length; ++i) {
			if (obj.attributes[i].name==attr) {
				obj.attributes[i].value=value;
				return;
			}
				
		}
		alert('TabsPanel.setAttr: no such attribute: '+attr);
	}
	
	this.containerInit();
	
}

