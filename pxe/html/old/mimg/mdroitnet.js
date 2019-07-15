document.write("<style>h3{COLOR:'#000000'; font: 11px 'Trebuchet MS', Tahoma, Geneva, Arial, Helvetica, sans-serif;} #mleft{COLOR: #000000; text-align:center; float:left; width:132px; margin-bottom:2px;} .cbar h3{font-weight:bold; background-image:url(mimg/mh.gif); background-position: top left; margin:0px 3px;text-align:left; padding: 9px 8px 3px 8px; line-height:13px;} .cbar .box {background-image:url(mimg/mb.gif); background-position:bottom left; background-repeat:no-repeat; margin:0px 3px 3px 3px; text-align:left; width:126px; padding-bottom:5px; overflow:hidden;} ul.menu li{background-image:url(mimg/mp.gif); background-repeat: repeat-x; padding: 3px 3px;} ul.menu li div{background-image: url(mimg/mg.gif); background-position: 0px 5px; background-repeat: no-repeat; padding-left: 9px; margin-left:3px; line-height:14px;} UL {margin: 0 5px; list-style-type: none;}</style>")
var mavar='?mavar='; // est ajouté comme variable GET à toute page appelée le contenu est spécifié ligne 17 & 18 par défaut la valeur de l'url
var mavar2='?mavar2=monurl';// Sert si vous voulez ajouter une variable à l'adresse(voir dans div)
var n=new Boolean();if(navigator.appName=='Netscape'){n=true;}else{n=false;} // Netscape(Mozilla) ou IE par défaut
function afficher_menu(e){
 if(n){gauche=e.pageX;if(window.innerWidth-e.pageX<document.getElementById('m').offsetWidth){gauche-=document.getElementById('m').offsetWidth;}
	haut=e.pageY;if(window.innerHeight-e.pageY<document.getElementById('m').offsetHeight){haut-=document.getElementById('m').offsetHeight;if(haut<0){haut=5}}
	with(document.getElementById('m').style){left=gauche; top=haut; visibility='visible';}}
 else{gauche=document.body.scrollLeft+event.clientX;if(document.body.clientWidth-event.clientX<m.offsetWidth){gauche-=m.offsetWidth;}
	haut=document.body.scrollTop+event.clientY;if(document.body.clientHeight-event.clientY<m.offsetHeight){haut-=m.offsetHeight;if(haut<0){haut=5}}
	with(m.style){left=gauche; top=haut; visibility='visible';}}return false;}
function cacher_menu(){if(n){document.getElementById('m').style.visibility='hidden';}else{m.style.visibility='hidden';}}
function menu_over(e){if(n){if(e.target.className=='rub'){with (e.target.style){color='#0FBFFF';}window.status=e.target.getAttribute('url'); }}
 else{if(event.srcElement.className=='rub'){with (event.srcElement.style){color='#0FBFFF';}status=event.srcElement.url; }}}
function menu_out(e){if(n){if(e.target.className=='rub'){with (e.target.style){color='#0FB000';}window.status='';}}
 else{if(event.srcElement.className=='rub'){with(event.srcElement.style){color='#0FB000';}status='';}}}
function menu_click(e){if(n){if(e.target.className=='rub'){location=e.target.getAttribute('url')+mavar+e.target.getAttribute('url');}}
 else{if(event.srcElement.className=='rub'){location=event.srcElement.url+mavar+event.srcElement.url;}}}
document.oncontextmenu=afficher_menu;document.onmouseover=menu_over;document.onclick=menu_click;document.onmouseout=menu_out;
document.write("<div id='m' style='position: absolute; visibility: hidden; width:126px; cursor: default; font: menu;'><div id='mleft' class='cbar'> <h3> :: Menu  ::</h3><div class='box'><ul class='menu'><li><div class='rub' url='javascript:history.go(-1)'> ON </div><div class='rub' url='javascript:history.go(1)'> OFF </div><div class='rub' url='javascript:history.go(0)'></div></li><li><div class='rub' url='accueil.php'> Restore </div><div class='rub' url='lienvariable.htm"+mavar2+"'> Backup </div></li><li><div class='rub' url='galerie.htm'>DamnSmallinux</div><div class='rub' url='salle.htm'> Cluster </div><div class='rub' url='video.htm'> Vnc </div> <div class='rub' url='intro.htm'> Camera </div></div></li></ul></div></div></div><body onClick='cacher_menu()'>")