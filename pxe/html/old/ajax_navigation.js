
<!-- Paste this code into an external JavaScript file named: ajax_navagation.js  -->

/* This script and many more are available free online at
The JavaScript Source :: http://javascript.internet.com
Created by: Michael :: http://www.posters-bestellen.nl */

var please_wait = null;

function open_url(url, target) {
 	if ( ! document.getElementById) {
  		return false;
 	}

 	if (please_wait != null) {
  		document.getElementById(target).innerHTML = please_wait;
 	}

 	if (window.ActiveXObject) {
  		link = new ActiveXObject("Microsoft.XMLHTTP");
 	} else if (window.XMLHttpRequest) {
  		link = new XMLHttpRequest();
 	}

 	if (link == undefined) {
  		return false;
 	}
 	link.onreadystatechange = function() { response(url, target); }
 	link.open("GET", url, true);
 	link.send(null);
}

function response(url, target) {
 	if (link.readyState == 4) {
	 	document.getElementById(target).innerHTML = (link.status == 200) ? link.responseText : "Ooops!! A broken link! Please contact the webmaster of this website ASAP and give him the fallowing errorcode: " + link.status;
	}
}

function set_loading_message(msg) {
 	please_wait = msg;
}



<!-- Paste this code into the HEAD section of your HTML document.
     You may need to change the path of the file.  -->

<script type="text/javascript" src="ajax_navagation.js"></script>



<!-- Paste this code into the HEAD section of your HTML document  -->

<script type="text/javascript">
<!--
/* This script and many more are available free online at
The JavaScript Source :: http://javascript.internet.com
Created by: Michael :: http://www.posters-bestellen.nl */

  set_loading_message("Please wait while the page is opening....");
//-->
</script>



<!-- Paste this code into the BODY section of your HTML document  -->

<table>
<tr>
<td valign=top width=150>
<H5>My Navagation links</H5>
<a href="javascript:void(0)" onclick="open_url('page-1.html','my_site_content');">Go to page 1</a><br>
<a href="javascript:void(0)" onclick="open_url('page-2.html','my_site_content');">Go to page 2</a><br>
<a href="javascript:void(0)" onclick="open_url('page-3.html','my_site_content');">Go to page 3</a><br>
<a href="javascript:void(0)" onclick="open_url('page-4.html','my_site_content');">Go to page 4</a><br>
<a href="javascript:void(0)" onclick="open_url('xxxx.html','my_site_content');">Broken Link</a><br>
</td>
<td valign=top>
<div id="my_site_content">
</div>
</td>
</tr>
</table>



