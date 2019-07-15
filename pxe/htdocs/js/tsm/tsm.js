/************************************************************	
 *										*
 * TSM: TabStrip Menu version 0.1					* 
 * Auteur: Wonesek (wonesek@aol.com)				*
 * Liscence: GNU/GPL							* 
 *										*
 * Respectez le travail de l'auteur en laissant cette		*
 * entête dans le fichier source.					*
 * Pour une utilisation commercial, veuillez prevenir		*
 * l'auteur.								*
 * 										*
 ************************************************************/

var atsm;

//path vers tsm_spacer.png
//si le .js est utilisé dans plusieurs fichiers de different repertoire,
//il suffit de redefinir la variable qui suit dans chacun des fichiers HTML avec un chemin relatif
//ou donner un chemin absolu dans ce fichier
var	tsmPath	= (tsmPath) ? tsmPath : "./",
	tsmImg	= "tsm_spacer.png",
	tsmS		= tsmPath + tsmImg;

//directions
var	menuTop	= 1,
	menuLeft	= 2,
	menuBottom	= 3,
	menuRight	= 4;

//evenements
var	onClick	= "onClick",
	onMouseOver	= "onMouseOver";

//type style (CSS)
//le style s'applique à l'entete de l'onglet, mais à l'onglet lui meme aussi.
var style_t	=	{ $font_family		: 0,		/* police de caractere */ 
			  $font_color		: 1,		/* couleur de la police */
			  $font_size		: 2,		/* taille en pixel */
			  $font_style		: 3,		/* underline ou normal */
			  $background_color	: 4,		/* couleur de fond */
			  $border_size		: 5,		/* taille de la bordure */
			  $border_style		: 6,		/* dashed, solid, outset, etc... style de la bordure */
			  $border_color		: 7,		/* couleur de la bordure */
			  $padding			: 8}		/* marge interieur en pixel */
function style()
{
	var i;
	for(i in style_t) this[i] = null;
}


//style par defaut:
var standardStyleOn;
var standardStyleOff;

with(standardStyleOn = new style)
{
	$font_family	= "arial";
	$font_color		= "#000000";
	$font_size		= "12px";
	$font_style		= "normal";
	$background_color	= "#ffffff";
	$border_size	= "1px";
	$border_style	= "solid";
	$border_color	= "#000000";
	$padding		= "4px";			
}

with(standardStyleOff = new style)
{
	$font_family	= "arial";
	$font_color		= "#c0c0c0";
	$font_size		= "12px";
	$font_style		= "normal";
	$background_color	= "#efefef";
	$border_size	= "1px";
	$border_style	= "dashed";
	$border_color	= "#c0c0c0";
	$padding		= "4px";
}
	
var name_tsm = "tsm";

//contiendra la liste des menus
var tsm = new Array();

//definit le type menu
var tsm_t =	{ menuId		: 0,		/* identifiant du menu */
		  id_cpt		: 1,		/* id du tableau html qui contiendra la "tête" des onglets */
		  id_cnt		: 2,		/* id du tableau html qui contiendra le "corps" des onglets */
		  parentDivId	: 3,		/* id de la division ou se situe le menu */
		  tabs		: 4,		/* tableau contenant tous les onglets du menu
		  html		: 5,		/* code html du menu */
		  menuWidth		: 6,		/* largeur du menu (px) */
		  menuHeight	: 7,		/* hauteur du menu (px) */
		  menuSelectTab	: 8,		/* onglet selectionné par defaut */
		  menuChangeEvt	: 9,		/* evenement qui permet de changer d'onglet */
		  menuDirection	: 10,		/* direction du menu */
		  menuAlign		: 11,		/* alignement des entetes */
		  menuMargin	: 12,		/* espacement entre deux entetes d'onglets (px) */
		  styleOn		: 13,		/* style des onglets qui n'ont pas le focus */
		  styleOff		: 14};	/* style des onglets qui ont le focus */ 

//creation de la classe tabStripMenu
function tabStripMenu(parentId, width, height)
{
	var i;
	for(i in tsm_t)
		this[i] = null;
		
	this.menuId		= tsm.length;
	this.parentDivId	= parentId;
	this.tabs		= new Array();
	this.id_cpt		= name_tsm + this.menuId + "cpt";
	this.id_cnt		= name_tsm + this.menuId + "cnt";
	this.menuWidth	= width;
	this.menuHeight	= height;

	//setup par defaut
	this.menuSelectTab	= 0;				//tab par defaut: la premiere
	this.styleOn		= standardStyleOn;	//styleOn standard
	this.styleOff		= standardStyleOff;	//styleOff standard
	this.menuChangeEvt	= onClick;			//changement d'onglet par click
	this.menuDirection	= menuTop;			//menu a entete horizontal
	this.menuAlign		= menuLeft;			//entete à gauche
	this.menuMargin		= 0;				//pas d'espacement entre les entetes
		
	//methodes detruites apres build()
	this.addTab			= tab;				//ajout d'un onglet
	this.updateTab		= updateTab;			//modifie le contenu d'un onglet
	this.build			= build;			//ajout du menu dans tsm + creation du code html
	this.setDefaultTab	= setDefaultTab;	//definir l'onglet par defaut
	this.setEvent		= setEvent;			//definir l'evenement declencheur
	this.setStyles		= setStyles;		//definir les styles on/off du tabstripmenu
	this.setDirection		= setDirection;	//definir la position de l'entete
	this.setAlign		= setAlign;			//definir l'alignement des items
	this.setMargin		= setMargin;		//definir la marge entre les entetes
		
	//methode utilisable apres build() et tsmLoadAll()
	/*setFocus()*/	//donner le focus à un onglet
}

function setDefaultTab(aTab)
	{this.menuSelectTab = (aTab) ? aTab : 0;}
	
function setMargin(pxVal)
	{this.menuMargin = Math.max(pxVal, 0);}

function setEvent(evt)
	{this.menuChangeEvt = (!evt) ? onClick : evt;}

function setDirection(dir)
{
	switch(dir)
	{
		case menuTop: case menuLeft: case menuBottom: case menuRight:
			this.menuDirection = dir;
		break;
		default:
			this.menuDirection = menuTop;
		break;
	}

	//on recharge l'alignement
	this.setAlign(this.menuDirection);
}

function setAlign(dir)
{
	switch(this.menuDirection)
	{
		case menuLeft : case menuRight :
			if ((dir == menuTop) || (dir == menuBottom))
				this.menuAlign = dir;
			else
				this.menuAlign = menuTop;
		break;

		case menuTop : case menuBottom :
			if ((dir == menuRight) || (dir == menuLeft))
				this.menuAlign = dir;
			else
				this.menuAlign = menuLeft;
		break;
	}
}


function setStyles(sOn, sOff)
{
	this.styleOn	= (!sOn) ? standardStyleOn : sOn;
	this.styleOff	= (!sOff) ? standardStyleOff : sOff;
}

//cette methode permet de construire le code html du menu
function build()
{
	var i;
	switch(this.menuDirection)
	{
		case menuLeft:
			this.html	= 	  "<table border='0' cellpadding='0' cellspacing='0' width='" + this.menuWidth + "px' height='" + this.menuHeight + "px'>"
						+ "<tr>"
						+ "<td valign='top'>"
						+ "<table id='" + this.id_cpt + "' border='0' cellpadding='0' cellspacing='0' width='100%' height='100%'>";

			if (this.menuAlign == menuBottom)
				this.html += "<tr><td height='100%'><img src='" + tsmS + "'></td></tr>";	
			for(i = 0; i < this.tabs.length; i++)
			{
				this.html += "<tr><td nowrap style='cursor:pointer' " + this.menuChangeEvt + "='javascript:tsm[" + this.menuId + "].setFocus(" + i + ")'>" + this.tabs[i].tabCaption + "</td></tr>";
				if 	((this.menuMargin > 0) && 
					 (i+1 != this.tabs.length)) this.html += "<tr><td><img height='" + this.menuMargin + "px' src='" + tsmS + "'></td></tr>";
			}
			if (this.menuAlign == menuTop)
				this.html += "<tr><td height='100%'><img src='" + tsmS + "'></td></tr>";	

			this.html	+= 	  "</table>"
						+ "</td>"
						+ "<td valign='top' width='100%'>"
						+ "<table id='" + this.id_cnt + "' border='0' width='100%' height='100%' cellpadding='0' cellspacing='0'>"
						+ "<tr>"
						+ "<td valign='top'>";
												
			for(i = 0; i < this.tabs.length; i++)
				this.html += "<div id='" + this.tabs[i].id_tab + "'>" + this.tabs[i].tabContent + "</div>";
														
			this.html	+=	  "</td>"
						+ "</tr>"
						+ "</table>"			
						+ "</td>"
						+ "</tr>"
						+ "</table>";
		break;
		
		case menuRight:
			this.html	= 	  "<table border='0' cellpadding='0' cellspacing='0' width='" + this.menuWidth + "px' height='" + this.menuHeight + "px'>"
						+ "<tr>"
						+ "<td valign='top' width='100%'>"
						+ "<table id='" + this.id_cnt + "' border='0' width='100%' height='100%' cellpadding='0' cellspacing='0'>"
						+ "<tr>"
						+ "<td valign='top'>";
												
			for(i = 0; i < this.tabs.length; i++)
				this.html += "<div id='" + this.tabs[i].id_tab + "'>" + this.tabs[i].tabContent + "</div>";
														
			this.html	+=	  "</td>"
						+ "</tr>"
						+ "</table>"
						+ "</td>"
						+ "<td valign='top'>"
						+ "<table id='" + this.id_cpt + "' border='0' cellpadding='0' cellspacing='0' height='100%'>";

			if (this.menuAlign == menuBottom)
				this.html += "<tr><td height='100%'><img src='" + tsmS + "'></td></tr>";	
			for(i = 0; i < this.tabs.length; i++)
			{
				this.html += "<tr><td nowrap style='cursor:pointer' " + this.menuChangeEvt + "='javascript:tsm[" + this.menuId + "].setFocus(" + i + ")'>" + this.tabs[i].tabCaption + "</td></tr>";
				if 	((this.menuMargin > 0) && 
					 (i+1 != this.tabs.length)) this.html += "<tr><td><img height='" + this.menuMargin + "px' src='" + tsmS + "'></td></tr>";
			}
			if (this.menuAlign == menuTop)
				this.html += "<tr><td height='100%'><img src='" + tsmS + "'></td></tr>";	

			this.html	+= 	  "</table>"			
						+ "</td>"
						+ "</tr>"
						+ "</table>";
		break;

		case menuBottom:
			this.html	= 	  "<table border='0' cellpadding='0' cellspacing='0' width='" + this.menuWidth + "px' height='" + this.menuHeight + "px'>"
						+ "<tr>"
						+ "<td height='100%' valign='top'>"
						+ "<table id='" + this.id_cnt + "' border='0' width='100%' height='100%' cellpadding='0' cellspacing='0'>"
						+ "<tr>"
						+ "<td valign='top'>";
												
			for(i = 0; i < this.tabs.length; i++)
				this.html += "<div id='" + this.tabs[i].id_tab + "'>" + this.tabs[i].tabContent + "</div>";
														
			this.html	+=	  "</td>"
						+ "</tr>"
						+ "</table>"
						+ "</td>"
						+ "</tr>"
						+ "<tr>"
						+ "<td>"
						+ "<table id='" + this.id_cpt + "' border='0' cellpadding='0' cellspacing='0' width='100%'>"
						+ "<tr>";

			if (this.menuAlign == menuRight)
				this.html += "<td width='100%'><img src='" + tsmS + "'></td>";				
			for(i = 0; i < this.tabs.length; i++)
			{
				this.html += "<td nowrap style='cursor:pointer' " + this.menuChangeEvt + "='javascript:tsm[" + this.menuId + "].setFocus(" + i + ")'>" + this.tabs[i].tabCaption + "</td>";
				if 	((this.menuMargin > 0) && 
					 (i+1 != this.tabs.length)) this.html += "<td><img width='" + this.menuMargin + "px' src='" + tsmS + "'></td>";
			}
			if (this.menuAlign == menuLeft)
				this.html += "<td width='100%'><img src='" + tsmS + "'></td>";

			this.html	+=	  "</tr>"
						+ "</table>"
						+ "</td>"
						+ "</tr>"
						+ "</table>";
		break;

		case menuTop:
			this.html	= 	  "<table border='0' cellpadding='0' cellspacing='0' width='" + this.menuWidth + "px' height='" + this.menuHeight + "px'>"
						+ "<tr>"
						+ "<td>"
						+ "<table id='" + this.id_cpt + "' border='0' cellpadding='0' cellspacing='0' width='100%'>"
						+ "<tr>";

			if (this.menuAlign == menuRight)
				this.html += "<td width='100%'><img src='" + tsmS + "'></td>";				
			for(i = 0; i < this.tabs.length; i++)
			{
				this.html += "<td nowrap style='cursor:pointer' " + this.menuChangeEvt + "='javascript:tsm[" + this.menuId + "].setFocus(" + i + ")'>" + this.tabs[i].tabCaption + "</td>";
				if 	((this.menuMargin > 0) && 
					 (i+1 != this.tabs.length)) this.html += "<td><img width='" + this.menuMargin + "px' src='" + tsmS + "'></td>";
			}
			if (this.menuAlign == menuLeft)
				this.html += "<td width='100%'><img src='" + tsmS + "'></td>";

			this.html	+=	  "</tr>"
						+ "</table>"
						+ "</td>"
						+ "</tr>"
						+ "<tr>"
						+ "<td height='100%' valign='top'>"
						+ "<table id='" + this.id_cnt + "' border='0' width='100%' height='100%' cellpadding='0' cellspacing='0'>"
						+ "<tr>"
						+ "<td valign='top'>";
												
			for(i = 0; i < this.tabs.length; i++)
				this.html += "<div id='" + this.tabs[i].id_tab + "'>" + this.tabs[i].tabContent + "</div>";
														
			this.html	+=	  "</td>"
						+ "</tr>"
						+ "</table>"
						+ "</td>"
						+ "</tr>"
						+ "</table>";
		break;
	}
					
	tsm[this.menuId]			= this;
	tsm[this.menuId].setFocus	= setFocus; 
}

//donner le focus à un onglet
function setFocus(tab)
{
	var cell, row;

	for(var i = 0; i < this.tabs.length; i++)
	{
		if (tab == i)
		{
			switch(this.menuDirection)
			{
				case menuLeft: case menuRight:
					//si il y a une marge entre les entetes on double
					row = (this.menuMargin != 0) ? 2*i : i;
					//si l'alignement est en bas, on decale d'un
					row = (this.menuAlign == menuBottom) ? (row+1) : row;
					with(_getObj(this.id_cpt).rows[row].cells[0].style)
					{
						with(this.styleOn)
						{
							backgroundColor	= $background_color;
							fontFamily		= $font_family;
							fontStyle		= $font_style;
							fontSize		= $font_size;
							color			= $font_color;
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderTopWidth	= $border_size;
							borderLeftWidth	= (this.menuDirection == menuLeft) ? $border_size : '0px';
							borderRightWidth	= (this.menuDirection == menuLeft) ? '0px' : $border_size;
							borderBottomWidth	= $border_size;
							padding		= $padding;
						}
					}
				break;

				case menuTop: case menuBottom:
					//si il y a une marge entre les entetes on double
					cell = (this.menuMargin != 0) ? 2*i : i;
					//si l'alignement est à droite, on decale d'un
					cell = (this.menuAlign == menuRight) ? (cell+1) : cell;
					with(_getObj(this.id_cpt).rows[0].cells[cell].style)
					{
						with(this.styleOn)
						{
							backgroundColor	= $background_color;
							fontFamily		= $font_family;
							fontStyle		= $font_style;
							fontSize		= $font_size;
							color			= $font_color;
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderTopWidth	= (this.menuDirection == menuBottom) ? '0px' : $border_size;
							borderLeftWidth	= $border_size;
							borderRightWidth	= $border_size;
							borderBottomWidth	= (this.menuDirection == menuBottom) ? $border_size : '0px';
							padding		= $padding;
						}
					}
				break;
			}
			_getObj(this.tabs[i].id_tab).style.display = "block";
		}
		else
		{
			switch(this.menuDirection)
			{
				case menuLeft: case menuRight:
					//si il y a une marge entre les entetes on double
					row = (this.menuMargin != 0) ? 2*i : i;
					//si l'alignement est en bas, on decale d'un
					row = (this.menuAlign == menuBottom) ? (row+1) : row;
					with(_getObj(this.id_cpt).rows[row].cells[0].style)
					{
						with(this.styleOff)
						{
							backgroundColor	= $background_color;
							fontFamily		= $font_family;
							fontStyle		= $font_style;
							fontSize		= $font_size;
							color			= $font_color;
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderTopWidth	= ((i > tab) && (this.menuMargin == 0))  ? "0px" : $border_size;
							borderBottomWidth	= ((i < tab) && (this.menuMargin == 0))  ? "0px" : $border_size;
							padding		= $padding;
						}
						if (this.menuDirection == menuLeft)
						{ 
							borderLeftWidth	= this.styleOff.$border_size;
							borderRightStyle	= this.styleOn.$border_style;
							borderRightWidth	= this.styleOn.$border_size;
							borderRightColor	= this.styleOn.$border_color;
						}
						else
						{
							borderRightWidth	= this.styleOff.$border_size;
							borderLeftStyle	= this.styleOn.$border_style;
							borderLeftWidth	= this.styleOn.$border_size;
							borderLeftColor	= this.styleOn.$border_color;
						}
					}
				break;

				case menuBottom: case menuTop:
					//si il y a une marge entre les entetes on double
					cell = (this.menuMargin != 0) ? 2*i : i;
					//si l'alignement est à droite, on decale d'un
					cell = (this.menuAlign == menuRight) ? (cell+1) : cell;
					with(_getObj(this.id_cpt).rows[0].cells[cell].style)
					{
						with(this.styleOff)
						{
							backgroundColor	= $background_color;
							fontFamily		= $font_family;
							fontStyle		= $font_style;
							fontSize		= $font_size;
							color			= $font_color;
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderLeftWidth	= ((i > tab) && (this.menuMargin == 0)) ? "0px" : $border_size;
							borderRightWidth	= ((i < tab) && (this.menuMargin == 0)) ? "0px" : $border_size;
							padding		= $padding;
						}
				
						if (this.menuDirection == menuBottom)
						{ 
							borderBottomWidth	= this.styleOff.$border_size;
							borderTopStyle	= this.styleOn.$border_style;
							borderTopWidth	= this.styleOn.$border_size;
							borderTopColor	= this.styleOn.$border_color;
						}
						else
						{
							borderTopWidth	= this.styleOff.$border_size;
							borderBottomStyle	= this.styleOn.$border_style;
							borderBottomWidth	= this.styleOn.$border_size;
							borderBottomColor	= this.styleOn.$border_color;
						}
					}
				break;
			}
			_getObj(this.tabs[i].id_tab).style.display = "none";
		}
	}
}
//definit le type onglet (un menu est constitué d'onglet)
var tab_t = { tabId		: 0,		/* identifiant de l'onglet */
		  id_tab		: 1,		/* id de la division qui contient le corps de l'onglet */
		  tabCaption	: 2,		/* caption de la "tête" de l'onglet */
		  tabContent	: 3,		/* contenu de l'onglet */
		  parentMenu	: 4,		/* menu dans lequel est l'onglet */
		  parentMenuId	: 5};		/* id du menu dans lequel est l'onglet */

function tab(caption, content)
{
	this.tabId			= this.tabs.length;	
	this.id_tab			= this.id_cnt + this.tabId;
	this.tabCaption		= caption;
	this.tabContent		= content;
	this.parentMenuId		= this.menuId;
	this.parentMenu		= this;
	
	this.tabs[this.tabId]	= new Array();
	var i;
	for(i in tab_t)
		this.tabs[this.tabId][i] = this[i];
	return this.id_tab;			   	/*retourne l'id pour un éventuelle mise à jours de onglet*/
} 

// mise à jour d'un onglet existant : by thenox (thenox@orange.fr)
// au passage, grand merci à Wonesek pour ce source magnifique :).			
function updateTab(id, content)
{
	for(var i=0; i < this.tabs.length; i++)
	{
	  if(this.tabs[i].id_tab == id)
	  {
	    var num=i;
		break;
	  }
	}
	_getObj(this.tabs[num].id_tab).innerHTML = content;
}

//charge tous les menus sur la page et ajuste leur apparence graphique
function tsmLoadAll()
{
	var	i = 0,
		l = 0,
		j,k,m;
	
	var	alreadyOutList = new Array(),
		alreadyOut;
	
	var elt;
	
	//on tourne dans une boucle tant que tous les menus ne sont pas affichés
	//avec une limite pour eviter les boucles infinies en cas de probleme
	while ((i != tsm.length) && (l <= Math.pow(tsm.length,2)))
	{
		for(j = 0; j < tsm.length; j++)
		{
			if (_getObj(tsm[j].parentDivId))
			{
				alreadyOut = false;
				for(k = 0; k < alreadyOutList.length ; k++)
				{
					if (alreadyOutList[k] == tsm[j].menuId)
					{
						alreadyOut = true;
						break;
					}
				}
				if (!alreadyOut)
				{
					_getObj(tsm[j].parentDivId).innerHTML = tsm[j].html;
					alreadyOutList[k+1] = tsm[j].menuId;
				}
			}
		l++;
		}
	}

	for(i = 0; i < tsm.length; i++)
	{
		//on charge styleOn
		with(tsm[i].styleOn)
		{
			switch(tsm[i].menuDirection)
			{
				case menuLeft: case menuRight:
					//la cellule qui contient le contenu de l'onglet
					with(_getObj(tsm[i].id_cnt).rows[0].cells[0].style)
					{
						backgroundColor	= $background_color;
						fontFamily		= $font_family;
						fontStyle		= $font_style;
						fontSize		= $font_size;
						color			= $font_color;
						borderStyle		= $border_style;
						borderColor		= $border_color;
						borderTopWidth	= $border_size;
						borderLeftWidth	= (tsm[i].menuDirection == menuLeft) ? '0px' : $border_size;
						borderRightWidth	= (tsm[i].menuDirection == menuLeft) ? $border_size : '0px';
						borderBottomWidth	= $border_size;
						padding		= $padding;
					}

					//on crée le bord gauche/droite
					elt = _getObj(tsm[i].id_cpt);
					for(j = 0; j < elt.rows.length; j++)
					{
						with(elt.rows[j].cells[0].style)
						{
							backgroundColor	= "transparent";
							padding		= "0px";
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderTopWidth	= '0px';
							borderLeftWidth	= (tsm[i].menuDirection == menuLeft) ? '0px' : $border_size;
							borderRightWidth	= (tsm[i].menuDirection == menuLeft) ? $border_size : '0px';
							borderBottomWidth	= '0px';
						}
					}			
				break;

				case menuTop: case menuBottom:
					//la cellule qui contient le contenu de l'onglet
					with(_getObj(tsm[i].id_cnt).rows[0].cells[0].style)
					{
						backgroundColor	= $background_color;
						fontFamily		= $font_family;
						fontStyle		= $font_style;
						fontSize		= $font_size;
						color			= $font_color;
						borderStyle		= $border_style;
						borderColor		= $border_color;
						borderTopWidth	= (tsm[i].menuDirection == menuBottom) ? $border_size : '0px';
						borderBottomWidth	= (tsm[i].menuDirection == menuBottom) ? '0px' : $border_size;
						borderLeftWidth	= $border_size;
						borderRightWidth	= $border_size;
						padding		= $padding;
					}

					//on crée le bord haut/bas
					elt = _getObj(tsm[i].id_cpt).rows[0];
					for(j = 0; j < elt.cells.length; j++)
					{
						with(elt.cells[j].style)
						{
							backgroundColor	= "transparent";
							padding		= "0px";
							borderStyle		= $border_style;
							borderColor		= $border_color;
							borderTopWidth	= (tsm[i].menuDirection == menuBottom) ? $border_size : '0px';
							borderBottomWidth	= (tsm[i].menuDirection == menuBottom) ? '0px' : $border_size;
							borderLeftWidth	= '0px';
							borderRightWidth	= '0px';
						}
					}
				break;
			}
		}
	}
	
	//focus sur les onglets par defaut
	for(i = 0; i < tsm.length; i++)
		tsm[i].setFocus(tsm[i].menuSelectTab);
}

//retourne l'objet associé à l'id passé en argument
function _getObj(id)
	{return document.getElementById(id);}

//retourne le contenu HTML d'un element tout en le supprimant de la page
function _extractSrcObj(id)
{
	var	obj		= document.getElementById(id),
		content	= obj.innerHTML;

	obj.innerHTML = "";

	return content;
}