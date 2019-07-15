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
	if (showColumn[0]) html+='<th class="c1">Id</th>';
	if (showColumn[1]) html+='<th class="c2">Name</th>';
	if (showColumn[2]) html+='<th class="c3">IP</th>';
	if (showColumn[3]) html+='<th class="c4">Mac</th>';
	if (showColumn[4]) html+='<th class="c5">Network Boot</th>';
	if (showColumn[5]) html+='<th class="c6">Save To</th>';
	if (showColumn[6]) html+='<th class="c7">Restore From</th>';
		
	html+='</tr></thead><tbody class="pclist">';
		
	if (t!=undefined && t.tableEl!=undefined) {
		var scrollTop=t.tableEl.tBodies[0].scrollTop;
	}
	
	for (var pc=1; pc<pcname.length ; ++pc) {
		if (pcname[pc]==undefined)
			 continue;
		var selectionStyle='background: '+((selection[pc])?'#aaaadd':'#f0f0f0')+';';
		html+='<tr name="lpc'+pc+'" style="'+selectionStyle+'" onclick="pcclick('+pc+')">';
		if (showColumn[0]) html+='<td class="pcIcon" name="lpc'+pc+'"><img src="/pxe/thumbs/pc'+pc+'_24x24.png" align="center"></td>';
		if (showColumn[1]) html+='<td class="pcIcon" name="lpc'+pc+'">'+pcname[pc]+'</td>';
		if (showColumn[2]) html+='<td class="pcIcon" name="lpc'+pc+'">'+((pcip[pc]=='')?'?':pcip[pc])+'</td>';
		if (showColumn[3]) html+='<td class="pcIcon" name="lpc'+pc+'">'+pcmac[pc]+'</td>';
		if (showColumn[4]) html+='<td class="columnPXEconfig" name="lpc'+pc+'">'+((pcpxeconfig[pc]==undefined)?'default':pcpxeconfig[pc])+'</td>';
		if (showColumn[5]) html+='<td class="columnSave" name="lpc'+pc+'">'+((pcsavepath[pc]==undefined)?'/pxe/image/'+pcmac[pc]:pcsavepath[pc])+'</td>';
		if (showColumn[6]) html+='<td class="columnRestore" name="lpc'+pc+'">'+((pcimagetorestore[pc]==undefined)?'':pcimagetorestore[pc])+'</td>';
		html+='</tr>';
	}
	
	if (all==true) {
		for (var i=0; i<hostsmac.length ; ++i) {
			html+='<tr class="pclist" style="background: #f0f0f0">';
			if (showColumn[0]) html+='<td class="c1" ondblclick="table_edit(this,24,'+"'pcadd(table_edit_td.childNodes[0],"+i+")'"+')"> </td>';
			if (showColumn[1]) html+='<td class="c2">' + hostsmac[i][1] + '</td>';
			if (showColumn[2]) html+='<td class="c3">'+((hostsmac[i][2]=='')?"?":hostsmac[i][2])+'</td>';
			if (showColumn[3]) html+='<td class="c4">'+hostsmac[i][0]+'</td>';
			if (showColumn[4]) html+='<td class="columnPXEconfig" name="lpc'+hostsmac[i][0]+'">'+hostsmac[i][3]+'</td>';
			if (showColumn[5]) html+='<td class="c6"></td>';
			if (showColumn[6]) html+='<td class="c7"></td>';
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
