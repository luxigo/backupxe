//D'autres scripts sur http://www.toutjavascript.com
//Si vous utilisez ce script, merci de m'avertir !  < <voir adresse mail sur site> >
//Auteur original :Olivier Hondermarck  <<voir adresse mail sur site>>
//Modifs compatibilité Netscape 6/Mozilla : Cédric Lamalle 09/2001 <cedric@cpac.embrapa.br>
//Correction Mac IE5 (Merci Fred)

var IB=new Object;
var posX=0;posY=0;
var xOffset=-40;yOffset=20;
IB.enable=false;

function AffBulle(texte) {
  if (IB.enable==false) return;
  contenu="<TABLE border=0 cellspacing=0 cellpadding="+IB.NbPixel+"><TR bgcolor='"+IB.ColContour+"'><TD><TABLE border=0 cellpadding=2 cellspacing=0 bgcolor='"+IB.ColFond+"'><TR><TD align=\"left\"><FONT size='-1' face='arial' color='"+IB.ColTexte+"'>"+texte+"</FONT></TD></TR></TABLE></TD></TR></TABLE>&nbsp;";
  var finalPosX=posX-xOffset;
  if (finalPosX<0) finalPosX=200;
  if (document.layers) {
    document.layers["bulle"].document.write(contenu);
    document.layers["bulle"].document.close();
    document.layers["bulle"].top=posY+yOffset;
    document.layers["bulle"].left=finalPosX;
    document.layers["bulle"].visibility="show";}
  if (document.all) {
    //var f=window.event;
    //doc=document.body.scrollTop;
    bulle.innerHTML=contenu;
    document.all["bulle"].style.top=posY+yOffset;
    document.all["bulle"].style.left=finalPosX;//f.x-xOffset;
    document.all["bulle"].style.visibility="visible";
  }
  //modif CL 09/2001 - NS6 : celui-ci ne supporte plus document.layers mais document.getElementById
  else if (document.getElementById) {
    var div=document.getElementById("bulle");
    div.innerHTML=contenu;
    div.style.position="absolute";
    if (posY+200>window.innerHeight+window.pageYOffset) {posY=window.innerHeight-200+window.pageYOffset}
    div.style.top=posY+yOffset + "px";
    div.style.left=finalPosX + "px";
    div.style.visibility="visible";

  }
}

function getMousePos(event) {

  var el;
  var x, y;

  // If an element id was given, find it. Otherwise use the element being
  // clicked on.

  // Get cursor position with respect to the page.

  if (browser.isIE) {
    posX = window.event.clientX + document.documentElement.scrollLeft
      + document.body.scrollLeft;
    posY = window.event.clientY + document.documentElement.scrollTop
      + document.body.scrollTop;
  }
  if (browser.isNS) {
//  if (browser.isNS) {
    posX=event.clientX + window.scrollX;
    posY=event.clientY + window.scrollY;
  }

}

function HideBulle() {
	if (IB.enable==false) return;
	if (document.layers) {document.layers["bulle"].visibility="hide";}
	if (document.all) {document.all["bulle"].style.visibility="hidden";}
	else if (document.getElementById){document.getElementById("bulle").style.visibility="hidden";}
}

function InitBulle(ColTexte,ColFond,ColContour,NbPixel) {
	IB.ColTexte=ColTexte;IB.ColFond=ColFond;IB.ColContour=ColContour;IB.NbPixel=NbPixel;
	if (document.layers) {
		window.captureEvents(Event.MOUSEMOVE);window.onMouseMove=getMousePos;
		document.write("<LAYER name='bulle' top='0px' left='0px' visibility='hide'></LAYER>");
	}
	if (document.all) {
		document.write("<DIV id='bulle' style='position:absolute;top:0px;left:0px;visibility:hidden'></DIV>");
		document.onmousemove=getMousePos;
	}
	//modif CL 09/2001 - NS6 : celui-ci ne supporte plus document.layers mais document.getElementById
	else if (document.getElementById) {
	        document.onmousemove=getMousePos;
	        document.write("<DIV id='bulle' style='position:absolute;top:0;left:0;visibility:hidden'></DIV>");
	}

}

//InitBulle('black','yellow','black',1);
