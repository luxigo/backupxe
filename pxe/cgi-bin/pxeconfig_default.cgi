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

ACTION=/cgi-bin/pxe/pxeconfig_default_apply.cgi

echo Content-type: text/html
echo Pragma: no-cache
echo
echo '<html>'
echo '<body>'

echo "<H3>PXE Configuration</H3>"
echo
echo "S&eacute;lectionnez le fichier de d&eacute;marrage r&eacute;seau par d&eacute;faut"
echo '<br><br>'
echo "<form action=\"$ACTION\" method=\"POST\">"

echo '<table>'
echo '<tr>'
echo '<td>'

echo '<select name=default>'

cd /tftpboot/pxelinux/pxelinux.cfg
if [ $? -eq 1 ] ; then
   echo cannot change to directory /tftpboot/pxelinux/pxelinux.cfg
   exit 1
fi

list=`ls -1`
default_one=`ls -l default | sed -r -n -e 's/.* -> (.*)/\1/p'`

for pxeconfig in $list ; do

  [ "$pxeconfig" = "default" ] && continue
  echo $pxeconfig | egrep -q ^01- && continue

  selected=
  if [ "$pxeconfig" = "$default_one" ] ; then
      selected=" selected"
  fi

  echo "<option value=\"$pxeconfig\"$selected>$pxeconfig</option>"

done

echo '</select>'
echo '</td>'
echo '</tr>'

echo '</table><br>'

echo "<input type=\"submit\" value=\"Appliquer\" name=\"submit\">"
echo '</form>'

echo '</body>'
echo '</html>'
