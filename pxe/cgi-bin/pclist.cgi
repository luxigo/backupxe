#!/bin/sh

. /pxe/etc/config

set -e

if [ -n "$REMOTE_ADDR" ] ; then
	echo Content-Type: text/javascript
	echo Pragma: no-cache
	echo
else
	echo // DONT MODIFY !! this file has been generated
	echo //
	echo // Edit $0 instead !
	echo
fi

echo "pclistColumn=new Array();"
sed -r -n -e '/^#/b' -e 's/(.*)/pclistColumn.push("\1");/p' /pxe/etc/pclist/columns
echo

echo "showColumn=new Array();"
for col in `cat /pxe/etc/pclist/columns` ; do
	show=`cat /pxe/etc/pclist/$col/show`
	echo "showColumn.push($show);"
done
echo

cat << EOF
function pclist(tableId,all)  {
	if (table_edit_td!=undefined) {
		var tdbackup=table_edit_td.innerHTML;
	}
	
	var html="";
	var div=document.getElementById(tableId);
	var t=document.getElementById('pclist');
	var container;
	
	
	container=div;
	
	html='<table class="pclist" id="pclist" cellspacing="1" cellpadding="4"><thead class="pclisthead"><tr>';
EOF


c=0
for col in `cat /pxe/etc/pclist/columns` ; do
	header=`cat /pxe/etc/pclist/$col/header`
	cat << EOF
	if (showColumn[$c]) html+='<th class="c$c">$header</th>';
EOF
	c=`expr $c + 1`
done
columns=$c

cat << EOF
		
	html+='</tr></thead><tbody class="pclist">';
		
	if (t!=undefined && t.tableEl!=undefined) {
		var scrollTop=t.tableEl.tBodies[0].scrollTop;
	}
	
	for (var pc=1; pc<pcname.length ; ++pc) {
		if (pcname[pc]==undefined)
			 continue;
		var selectionStyle='background: '+((selection[pc])?'#aaaadd':'#f0f0f0')+';';
		html+='<tr name="lpc'+pc+'" style="'+selectionStyle+'" onclick="pcclick('+pc+')">';
EOF

c=0
for col in `cat /pxe/etc/pclist/columns` ; do
	td=`cat /pxe/etc/pclist/$col/td1`
	cat << EOF
		if (showColumn[$c]) html+='$td';
EOF
	c=`expr $c + 1`
done


#		if (showColumn[0]) html+='<td class="pcIcon" name="lpc'+pc+'"><img src="/pxe/thumbs/pc'+pc+'_24x24.png" align="center"></td>';
#		if (showColumn[1]) html+='<td class="pcIcon" name="lpc'+pc+'">'+pcname[pc]+'</td>';
#		if (showColumn[2]) html+='<td class="pcIcon" name="lpc'+pc+'">'+((pcip[pc]=='')?'?':pcip[pc])+'</td>';
#		if (showColumn[3]) html+='<td class="pcIcon" name="lpc'+pc+'">'+pcmac[pc]+'</td>';
#		if (showColumn[4]) html+='<td class="columnPXEconfig" name="lpc'+pc+'">'+((pcpxeconfig[pc]==undefined)?'default':pcpxeconfig[pc])+'</td>';
#		if (showColumn[5]) html+='<td class="columnSave" name="lpc'+pc+'">'+((pcsavepath[pc]==undefined)?'/pxe/image/'+pcmac[pc]:pcsavepath[pc])+'</td>';
#		if (showColumn[6]) html+='<td class="columnRestore" name="lpc'+pc+'">'+((pcimagetorestore[pc]==undefined)?'':pcimagetorestore[pc])+'</td>';

cat << EOF
		html+='</tr>';
	}
	
	if (all==true) {
		for (var i=0; i<hostsmac.length ; ++i) {
			html+='<tr class="pclist" style="background: #f0f0f0">';
EOF

c=0
for col in `cat /pxe/etc/pclist/columns` ; do
	td=`cat /pxe/etc/pclist/$col/td2`
	cat << EOF
			if (showColumn[$c]) html+='$td';
EOF
	c=`expr $c + 1`
done
#			if (showColumn[0]) html+='<td class="c1" ondblclick="table_edit(this,24,'+"'pcadd(table_edit_td.childNodes[0],"+i+")'"+')"> </td>';
#			if (showColumn[1]) html+='<td class="c2">' + hostsmac[i][1] + '</td>';
#			if (showColumn[2]) html+='<td class="c3">'+((hostsmac[i][2]=='')?"?":hostsmac[i][2])+'</td>';
#			if (showColumn[3]) html+='<td class="c4">'+hostsmac[i][0]+'</td>';
#			if (showColumn[4]) html+='<td class="columnPXEconfig" name="lpc'+hostsmac[i][0]+'">'+hostsmac[i][3]+'</td>';
#			if (showColumn[5]) html+='<td class="c6"></td>';
#			if (showColumn[6]) html+='<td class="c7"></td>';

cat << EOF
			html+='</tr>';
		}
	} 
	
	html+='</tbody></table>';
	container.innerHTML=html;
	
	if (t!=undefined && t.tableEl!=undefined) {
		t.tableEl.tBodies[0].scrollTop=scrollTop;
	}
	if (table_edit_td!=undefined) {
		
	}
}
EOF

