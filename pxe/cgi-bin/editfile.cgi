#!/bin/bash
. /pxe/etc/config

set -e

echo Content-Type: text/html
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        file) file=`basename $value` ;;
                        div) divID=$value ;;
                        list) subdir=$value ;;
                        mode) mode=$value ;;
                        
                esac 
        done
fi

if [ -n "$subdir" ] ; then
	linenum=1
	echo "FileEditor.divedit_file.slice(0,FileEditor.divedit_file.length);"
	echo "FileEditor.divedit_menu.slice(0,FileEditor.divedit_menu.length);"
	while true; do
		line=`sed -n -e ${linenum}p /pxe/etc/$subdir/divedit.conf`
		[ -z "$line" ] && break
		filename=`echo $line | cut -f 0 -d ' '`
		echo "FileEditor.divedit_file.push('$filename');"
		descr=`echo $line | sed -r -n -e 's/^[^\ ]+ (.*)/\1/p'`
		[ -z "$descr" ] && descr=`basename $filename`
		
		echo "FileEditor.divedit_menu.push('$descr');"
		linenum=`expr $linenum + 1`
	done
	echo "FileEditor.menu_build('diveditmenu','editor_window','$mode');"
	exit 0
fi

case $mode in
	table)
		echo '<table class="editor_window" cellspacing="0" cellpadding="0">'
		echo '<tr>'
		echo '<td valign="top" class="editor_filename" width="100%">'
		echo $file
		echo '</td>'
		echo '</tr>'
		echo '<tr>'
		echo '<td class="editor_text" align="right">'
		#echo '<td class="editor_text" align="right" ondblclick="divedit('"'$divID','$file')"'">'
		echo '<table align="right" cellspacing="0" cellpadding="0">'
		if [ -s /pxe/etc/$file ] ; then
		        sed -r \
		        	-e 's/ +/\<\/td\>\<td align="right" class="editor_table" ondblclick="FileEditor.table_edit(this)"\>/' \
		        	-e 's/.*/\<tr\>\<td align="right" class="editor_table_index" ondblclick="FileEditor.table_edit(this)"\>\0/'
		else
		        echo '<td class="editor_text">Rien a afficher</td>'
		fi
		echo '</table>'
		#sed -r -e 's/.*/\0<br>/' /pxe/etc/$file
		echo '</td>'
		echo '</tr>'
		echo '</table>'
		;;
	text)
		echo '<textarea style="width: 100%">'
		cat /pxe/etc/$file
		echo '</textarea>'
		echo '<input type="button" class="button" value="Sauver" onclick="div_save('"'$divID','$file'"')"></input>'
		echo '<input type="button" class="button" value="Annuler" onclick="innerHTML_restore('"'$divID'"')"></input>'
		;;
esac

exit 0
