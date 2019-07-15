#!/bin/sh
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
