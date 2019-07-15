#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux, all rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
			mode) mode=$value ;;
                esac
        done
fi

case $mode in
        text)
                sed -r -e 's/.*/\0<br>/' /pxe/etc/$file
                ;;
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
                        	-e 's/ +/\<\/td\>\<td align="right" class="editor_table" ondblclick="table_edit(this)"\>/' \
                        	-e 's/.*/\<tr\>\<td align="right" class="editor_table_index" ondblclick="table_edit(this)"\>\0/' \
                        	/pxe/etc/$file
                else
                        echo '<td class="editor_text">Rien a afficher</td>'
                fi
                echo '</table>'
                echo '</td>'
                echo '</tr>'
                echo '</table>'
                ;;
esac
