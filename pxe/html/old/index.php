<?php
/*
*/
 

include ("_relpos.php");
include ($phproot . "/glpi/includes.php");

checkAuthentication("normal");

commonHeader("Graphviz", $_SERVER["PHP_SELF"]);

echo "<div align=\"center\">";
echo "</div>";


?>
<html>
<script src=mimg/select.js></script>


</body>

</html>

<html>
<head>


</STYLE>
<script src="/pxe/rainbow.js">
</script>

<script>

  macjs=new Array();
  comment='INDIQUER ICI dans macjs[] LES MAC ADRESSES DES POSTES';
  macjs[1]="M00_0c_29_b3_54_d2";
  macjs[2]="M00_0c_29_b3_59_d0";

</script>

</head>

<body>

<img src="plan_cliquable.png" width="644" height="476" border="0" usemap="#map" />
<map name="map">


<area shape="rect" coords="24,404,61,438" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[1]);" />
<area shape="rect" coords="24,369,59,400" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[2]);"  />
<area shape="rect" coords="71,321,108,355" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[3]);" />
<area shape="rect" coords="104,367,141,401" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[4]);" />
<area shape="rect" coords="105,401,142,435" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[5]);" />
<area shape="rect" coords="208,396,245,430" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[6]);" />
<area shape="rect" coords="253,136,290,170" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[7]);" />
<area shape="rect" coords="206,323,243,357" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[8]);" />
<area shape="rect" coords="320,125,357,159" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[9]);" />
<area shape="rect" coords="368,124,405,158" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[10]);" />
<area shape="rect" coords="413,125,450,159" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[11]);" />
<area shape="rect" coords="335,34,372,68" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[12]);" />
<area shape="rect" coords="374,33,411,67" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[13]);" />
<area shape="rect" coords="420,29,457,63" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[14]);" />
<area shape="rect" coords="461,28,498,62" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[15]);" />
<area shape="rect" coords="440,66,477,100" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[16]);" />
<area shape="rect" coords="512,37,549,71" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[17]);" />
<area shape="rect" coords="516,93,553,127" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[18]);" />
<area shape="rect" coords="559,93,596,127" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[19]);" />
<area shape="rect" coords="516,133,553,167" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[20]);" />
<area shape="rect" coords="560,133,597,167" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[21]);" />
<area shape="rect" coords="511,309,546,331" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[22]);" />
<area shape="rect" coords="510,333,547,359" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[23]);" />
<area shape="rect" coords="509,365,543,386" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[24]);" />
<area shape="rect" coords="511,389,544,415" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[25]);" />
<area shape="rect" coords="452,331,474,366" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[26]);" />
<area shape="rect" coords="426,332,450,366" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[27]);" />
<area shape="rect" coords="402,331,421,366" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[28]);" />
<area shape="rect" coords="373,331,399,366" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[29]);" />
<area shape="rect" coords="348,332,368,366" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[30]);" />
<area shape="rect" coords="322,330,345,367" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[31]);" />
<area shape="rect" coords="451,370,474,405" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[32]);" />
<area shape="rect" coords="429,370,449,405" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[33]);" />
<area shape="rect" coords="399,370,423,406" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[34]);" />
<area shape="rect" coords="375,371,396,405" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[35]);" />
<area shape="rect" coords="349,372,368,405" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[36]);" />
<area shape="rect" coords="321,373,345,406" onmouseover="" onmouseout="" onclick="parent.switchBox(macjs[37]);" />
</map>
<FRAMESET cols="40%, 60%">
      <FRAME src="/pxe/home.html" name=frame1>
      <FRAME src="/pxe/empty.html" name=frame2>
  <NOFRAMES>
     <P>This frameset document contains:
     <UL>
         <LI><A href="/pxe/home.html">home</A>
           </UL>
 </NOFRAMES>
 </FRAMESET>
</body>
</html>
<?php
commonFooter();
?>

