
<!-- THREE STEPS TO INSTALL AJAX LOADER:

  1.  Copy the coding into the HEAD of your HTML document
  2.  Add the onLoad event handler into the BODY tag
  3.  Put the last coding into the BODY of your HTML document  -->

<!-- STEP ONE: Paste this code into the HEAD of your HTML document  -->

<HEAD>

<style type="text/css">
<!--
#contentLYR {
  position:absolute;
  width:200px;
  height:115px;
  z-index:1;
  left: 200px;
  top: 200px;
}
-->
</style>

<script type="text/javascript">
<!-- Begin
/* This script and many more are available free online at
The JavaScript Source!! http://javascript.internet.com
Created by: Eddie Traversa (2005) :: http://dhtmlnirvana.com/ */

function ajaxLoader(url,id) {
  if (document.getElementById) {
    var x = (window.ActiveXObject) ? new ActiveXObject("Microsoft.XMLHTTP") : new XMLHttpRequest();
  }
  if (x) {
    x.onreadystatechange = function() {
      if (x.readyState == 4 && x.status == 200) {
        el = document.getElementById(id);
        el.innerHTML = x.responseText;
      }
    }
    x.open("GET", url, true);
    x.send(null);
  }
}
//-->
</script>
</HEAD>

<!-- STEP TWO: Insert the onLoad event handler into your BODY tag  -->

<BODY onload="ajaxLoader('demo.xml','contentLYR')">

<!-- STEP THREE: Copy this code into the BODY of your HTML document  -->

<div id="contentLYR">
</div>

<p><center>
<font face="arial, helvetica" size"-2">Free JavaScripts provided<br>
by <a href="http://javascriptsource.com">The JavaScript Source</a></font>
</center><p>

<!-- Script Size:  1.49 KB -->
