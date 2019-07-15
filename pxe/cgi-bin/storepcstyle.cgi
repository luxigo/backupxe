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
PCSTYLE=/pxe/etc/pcstyle

echo Content-type: text/html
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

  pc=`echo $param | cut -f 1 -d = | sed -r -n -e 's/^pc//p'`
  style=`echo $param | cut -f 2 -d =  | urldecode`

#  echo "pc$pc='$style'<br>"
  [ -z "$style" ] && continue
  [ -z "$pc" ] && continue
  [ "$style" = "undefined" ] && continue
  [ "$pc" = "undefined" ] && continue
  echo $style | grep -q \- && continue

  setrec $PCSTYLE $pc $style

done

killall getpcicons.sh > /dev/null 2>&1 || true
( /pxe/bin/getpcicons.sh "register"
/pxe/bin/getpcicons.sh "default" ) 1>&- &
