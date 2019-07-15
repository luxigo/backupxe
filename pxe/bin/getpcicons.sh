#!/bin/sh
. /pxe/etc/config
set +x
ASYNC=0
QUERY_STRING="$1"
for param in `echo $QUERY_STRING | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
	[ -z "$param" ] && continue
	varname=`echo $param | cut -f 1 -d = | urldecode`
	value=`echo $param | cut -f 2 -d =  | urldecode`
	case "$varname" in
		async) ASYNC=$value ;;
		register) page=register ;;
		default) page=default ;;
		reload) reload=1 ;;
	esac
done

set -e

if [ $ASYNC -eq 1 ] ; then
#	kill -0 `cat /var/run/pxe/pingall.pid` > /dev/null 2>&1 || nohup pingall &
	kill -0 `cat /var/run/pxe/getpcicons.pid` > /dev/null 2>&1 && exit 0
	echo $$ > /var/run/pxe/getpcicons.pid
fi

PCSTYLE=/pxe/etc/pcstyle

PC_OFF=/pxe/thumbs/pc_off.png
PC_LINUX=/pxe/thumbs/pc_linux.png
PC_WINDOWS=/pxe/thumbs/pc_windows.png
PC_BOOT=/pxe/thumbs/pc_boot.png
PC_GEEXBOX=/pxe/thumbs/pc_geexbox.png
PC_GEEXBOX_MPLAYER=/pxe/thumbs/pc_geexbox_mplayer.png
PC_GEEXBOX_ERROR=/pxe/thumbs/pc_geexbox_error.png
TRANSPARENT_SELECTION=/pxe/pics/transparent.png

printstatus() {
	case "$pcstatus" in
		W)
			printf "$pcstatus_img" "$PC_WINDOWS"
			;;
		1)
			printf "$pcstatus_img"  "$PC_BOOT"
			;;
		L)
			printf "$pcstatus_img" "$PC_LINUX"
			;;
		G|GL)
			printf "$pcstatus_img" "$PC_GEEXBOX"
			;;
		GM)
			printf "$pcstatus_img" "$PC_GEEXBOX_MPLAYER"
			;;
		GE)
			printf "$pcstatus_img" "$PC_GEEXBOX_ERROR"
			;;
		0|-1|*)
			printf "$pcstatus_img" "$PC_OFF"
			;;
	esac
}

main() {

(

echo Content-type: text/plain
echo Pragma: no-cache
echo Connection: close
echo

count=`cat $PCSTYLE | wc -l` 

if [ $count -eq 0 ] ; then
	echo -n "document.getElementById('divicons').innerHTML='';"
	exit 0
fi

i=1
while [ $i -le $count ] ; do

  line=`sed -r -n -e ${i}p $PCSTYLE`
  i=`expr $i + 1` 
  
  pc=`echo $line | cut -f 1 -d ' '`
  [ -z "$pc" ] && continue
  
  mac=`getrec /pxe/etc/machines $pc || true`
  [ -z "$mac" ] && continue
  name=`getrec /pxe/etc/hosts.mac $mac || true`
  [ -z "$name" ] && name=$mac
  
  style=`echo $line | sed -r -e s/^$pc\ //`
  [ -z "$style" ] && continue
  
  case "$page" in
	register)
		[ $i -eq 2 ] && echo -n "document.getElementById('divicons').innerHTML='"
		echo -n '<img src="/pxe/thumbs/pc'$pc'.png" name="machine'$pc'" border="0" style="position: absolute; '$style' cursor : move;">'
		selection_img="<img class=\"pcIcon\" name=\"selection$pc\" src=\"$TRANSPARENT_SELECTION\" onmousedown=\"if (event.ctrlKey) {SimpleContextMenu._show(event); return false;} else {dragStart(event,$pc,selectionGroup(this));}\" onmouseup=\"if(event.ctrlKey) return false; \" onmouseover=\"AffBulle(getpcbull($pc));\" onmouseout=\"HideBulle();\" border=\"0\" style=\"position: absolute; $style cursor: move;\" >"
		echo -n $selection_img
		;;
	default)
		if [ -z "$reload" ] ; then
			[ $i -eq 2 ] && echo -n "document.getElementById('divicons').innerHTML='"
			echo -n '<img name="pc'$pc'" src="/pxe/thumbs/pc'$pc'.png" style="position: absolute; '$style' cursor : pointer;">'
			pcstatus_img='<img name="status'$pc'" src="%s" onclick="if (event.ctrlKey) return false ; pcclick('$pc')" border="0" style="position: absolute; '$style' cursor : pointer;">'
			selection_img="<img class=\"pcIcon\" name=\"selection$pc\" src=\"$TRANSPARENT_SELECTION\" onclick=\"if (event.ctrlKey) return false ; pcclick($pc)\" onmousedown=\"if (event.ctrlKey) {SimpleContextMenu._show(event); return false;}\" onmouseup=\"if(event.ctrlKey) return false;\" onmouseover=\"AffBulle(getpcbull($pc));\" onmouseout=\"HideBulle();\" border=\"0\" style=\"position: absolute; $style cursor : pointer;\" >"

			pcstatus=`getrec /pxe/etc/pcstatus $pc 2> /dev/null 2> /dev/null 2> /dev/null 2> /dev/null 2> /dev/null 2> /dev/null 2> /dev/null 2> /dev/null || true` 
			printstatus
			echo -n $selection_img

		else

			pcstatus_img='document.images["status'$pc'"].src="%s";'	

			pcstatus=`getrec /pxe/etc/pcstatus $pc 2> /dev/null || true`  
			printstatus
			echo
		fi
	  esac
done

[ $i -gt $count ] && [ -z "$reload" ] && echo "';"
echo 'selection_init();'

) > /dev/shm/pcicons.$$.tmp

cat /dev/shm/pcicons.$$.tmp > /pxe/etc/pcicons.$page$reload
rm /dev/shm/pcicons.$$.tmp

}


page=`echo $QUERY_STRING | cut -f 1 -d \&`
if echo $QUERY_STRING | grep -q '&' ; then
  reload=1
fi

while true ; do

	if [ /pxe/etc/machines -nt /pxe/etc/pcicons.default ] || [ /pxe/etc/pcstyle -nt /pxe/etc/pcicons.default ] || [ /pxe/etc/pcstatus -nt /pxe/etc/pcicons.default ] ; then
		page=default
		reload=
		touch /pxe/etc/pcicons.default
		main
	fi

	if [ /pxe/etc/machines -nt /pxe/etc/pcicons.register ] || [ /pxe/etc/pcstyle -nt /pxe/etc/pcicons.register ] ; then
		page=register
		reload=
		touch /pxe/etc/pcicons.register
		main
	fi

	if [ /pxe/etc/machines -nt /pxe/etc/pcicons.default1 ] || [ /pxe/etc/pcstyle -nt /pxe/etc/pcicons.default1 ] || [ /pxe/etc/pcstatus -nt /pxe/etc/pcicons.default1 ] ; then
		page=default
		reload=1
		touch /pxe/etc/pcicons.default1
		main
	fi

	[ $ASYNC -eq 0 ] && break
	[ -f /var/run/pxe/getpcicons.pid ] || break
	
	sleep 1
done
