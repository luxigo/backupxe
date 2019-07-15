#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux
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

EMOTE_ADDR=$REMOTE_ADDR
export REMOTE_ADDR=
. /pxe/etc/config
export REMOTE_ADDR=$EMOTE_ADDR

set -e
echo Content-type: text/html
echo Pragma: no-cache
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
	[ -z "$param" ] && continue
        varname=`echo $param | cut -f 1 -d = | urldecode`
        value=`echo $param | cut -f 2 -d =  | urldecode`
        case "$varname" in
                user) user="$value" ;;
                pass) pass="$value" ;;
        esac
done

page=`getrec /etc/auth.passwd $user:$pass 2> /dev/null` || true
if [ -n "$page" ] ; then
	setrec /pxe/etc/allow $REMOTE_ADDR 1
        setrec /pxe/etc/logintime $REMOTE_ADDR `date +%s` 2> /dev/null
        setrec /pxe/etc/lasthit $REMOTE_ADDR `date +%s` 2> /dev/null
# iptables -A FORWARD -s $REMOTE_ADDR -d ! 192.168.0.0/16 -j ACCEPT
	cat << EOF
<html>
<head>
	<meta http-equiv="refresh" content="0; URL=$page">
</head>
</body>
<body>
</html>
EOF

else
	setrec /pxe/etc/allow $REMOTE_ADDR 0
	cat /pxe/htdocs/denied.html
fi
