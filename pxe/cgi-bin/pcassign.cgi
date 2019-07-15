#!/bin/sh
. /pxe/etc/config
set -e

HOSTSMAC=/pxe/etc/hosts.mac
ITEMHEIGHT=24

echo Content-type: text/html
echo

#echo '<html><head>'
echo '<script src="/pxe/js/pcclick.js"></script>'
#echo '</head><body>'

#/pxe/bin/maclist.sh -more > /dev/null

machinesList () {


#	echo '<table>'
#	echo '<tr><td>'
#
#
	echo '<strong>Machines</strong>'
#	echo '</td><td>'
#	echo '</td></tr>'
#
#	echo '<tr><td>'

	echo '<div id="machines" style="border: 1px solid black; width: 192; height: 128; overflow: auto;">'

	count=0
	for m in `cat /pxe/etc/machines | sort -n | sed -r -n -e 's/^([0-9]+)[\ \t]+(.*)/\1_\2/p'` ; do

		pc=`echo $m | cut -f 1 -d _`
		hwaddr=`echo $m | cut -f 2 -d _`
                [ -z "$hwaddr" ] && continue	

		name=`getrec $HOSTSMAC $hwaddr || true`
		if [ -z "$name" ] ; then
			name=$hwaddr
		fi
		echo -n "<div id=\"divlist0_$pc\" onclick=\"divlistselect(0,$pc,'$name',pcedit($pc,'$name'))\" style=\"cursor: pointer;"
		if [ "$1" = "$pc" ] ; then
			echo -n "backgroundColor: cyan;"
		fi
		echo "\"><img src=\"/pxe/thumbs/pc$pc\_24x24.png\">&nbsp;$name</div>"

		count=`expr $count + 1`

	done

	if [ $count -eq 0 ] ; then
		echo Nothing to display
	fi

	echo '</div>'
}

editmachine () {
#	echo '<div id="pcedit">'
	if [ -n "$1" ] ; then
		echo '<img src="/pxe/thumbs/pc'$1'.png">'
		echo '<input type="text" name="pcname" value="'$2'">'
		echo '<input type="button" value="Modifier" onclick="pcedit_save('$1')">'
	fi
#	echo '</div>'
#	echo '</tr>
#	echo '</table>'

}

unassignedList () {

	echo '<div id="available" style="border: 1px solid black; width: 192; height: 128; overflow: auto;">'
	count=0

	for hwaddr in `/pxe/bin/maclist.sh -more` ; do

		grep -q $hwaddr /pxe/etc/machines && continue

		count=`expr $count + 1`

		name=`getrec $HOSTSMAC $hwaddr || true`;
		if [ -z "$name" ] ; then
			name=$hwaddr
		fi

		echo "<div id=\"divlist1_$count\" onclick=\"divlistselect(1,$count,'$name')\" style=\"cursor: pointer;\">"
		echo '<img src="/pxe/thumbs/pc00_24x24.png" align="center">'$name
		echo '</div>'

	done
	echo '</div>'
	echo 'PC Num&eacute;ro:<input type=text name="addpcnum" value="'$1'" style="width: 32;">'
	echo "<input type=button name=\"addmachine\" value=\"Enregistrer\" onclick=\"addmachine(1,event);\">"
	echo "<input type=button name=\"cancel\" value=\"Annuler\" onclick=\"divclose('divassign');\">"
	echo '<div id="addmachine_errormsg"></div>'
}

if [ -n "$QUERY_STRING" ] ; then 

	for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
		[ -z "$param" ] && continue
		varname=`echo $param | cut -f 1 -d =`
		value=`echo $param | cut -f 2 -d =`
		case "$varname" in
			pc) pc=$value ;;
			name) name=$value ;;
		esac
	done
fi

if [ -n "$name" ] ; then
	editmachine $pc $name
else
	unassignedList $pc
fi
#echo '</body></html>'
