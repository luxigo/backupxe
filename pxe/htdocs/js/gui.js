
//document.body.onmousedown="getmousepos(event)";
//document.body.onload="backupxe_onload(event)";
var gui = document.createElement("table");
var t=gui;
t.className="backupxe";
t.setAttribute("cellpadding","0");
t.setAttribute("cellspacing","0");
t.style.width="100%";

var tr=document.createElement("tr");

// left column

var td=document.createElement("td");
td.setAttribute("valign","top");
td.setAttribute("align","left");

// map
var div=document.createElement("div");
div.id="mapdiv";

var img=document.createElement("img");
img.id="map";
img.name="map";
img.src="/pxe/pics/map.png";
img.setAttribute("onmousedown","mapclick(event)");
img.className="map";

// pc icons
var div1=document.createElement("div");
div1.id="divicons";

div.appendChild(img);
td.appendChild(div);
td.appendChild(div1);
tr.appendChild(td);

// right column

var td=document.createElement('td');
td.setAttribute("name","cartable");
td.className="pclist";
td.setAttribute("valign","top");
td.style.top="0px";
td.style.width="100%";

div=document.createElement('div');
div.id="cartouche";
div.style.width="100%";

t2=document.createElement('table');
t2.setAttribute("cellpadding","0");
t2.setAttribute("cellspacing","0");
t2.border="0";
t2.style.width="100%";

tr2=document.createElement('tr');
tr2.style.width="100%";

var td2=document.createElement('td');
td2.setAttribute("valign","top");
td2.setAttribute("colspan","3");
td2.className="page_header";
td2.style.width="100%";


// room name table

var t3=document.createElement('table');
t3.setAttribute("cellspacing","0");
t3.border="0";
t3.style.width="100%";

var tr3=document.createElement('tr');
tr3.id="roomName";
tr3.style.width="100%";

// room name
var td3=document.createElement('td');
td3.className="roomName";
td3.style.width="100%";
td3.innerHTML="<h2>BackuPXE</h2>";
td3.style.display="none";

// end of room name table
tr3.appendChild(td3);
t3.appendChild(tr3);

td2.appendChild(t3);
tr2.appendChild(td2);
t2.appendChild(tr2);

// div mapupload
tr2=document.createElement('tr');
td3=document.createElement('td');
div2=document.createElement('div');
div2.id="divmapupload";

td3.appendChild(div2);
tr2.appendChild(td3);
t2.appendChild(tr2);

// pclist

tr2=document.createElement('tr');
td3=document.createElement('td');
div2=document.createElement('div');
div2.id="pctable";

td3.appendChild(div2);
tr2.appendChild(td3);
t2.appendChild(tr2);

// end of row
div.appendChild(t2);
td.appendChild(div);
tr.appendChild(td);
t.appendChild(tr);


// main div
gui=document.createElement('div');
gui.id="backupxe";
gui.className="backupxe";
gui.appendChild(t);

div=document.createElement('div');
div.id="selrect";
div.className="selrect";
gui.appendChild(div);

div=document.createElement('div');
div.id="divlog";
gui.appendChild(div);



