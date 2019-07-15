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

echo Content-Type: text/html
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        pc) PC=$value ;;
                esac
        done
fi

cat << EOF
<form name="movieopen" method="get" action="/cgi-bin/pxe/movieopen.cgi">
	<table align="center">
		<tr>
			<td>
				url pour pc$PC:
			</td>
			<td>
				<input type="text" name="url" style="width: 320px;">
				<input type="hidden" name="pc" value="$PC">
			</td>
		</tr>
	</table>
</form>
EOF
