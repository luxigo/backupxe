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

. /pxe/etc/config

sav=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 3`
NAME=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 2`
what=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 1`

ACTION=/cgi-bin/pxe/choosedisk_apply.cgi
SAVLINK=/cgi-bin/pxe/choosepart.cgi
WORKDIR=/pxe

echo Content-type: text/html
echo
echo '<html>'
echo '<body>'

if egrep -q \ $NAME\$ $WORKDIR/etc/hosts.mac ; then
  mac=`egrep \ $NAME\$ $WORKDIR/etc/hosts.mac | cut -f 1 -d \ `
else
  mac=$NAME
fi

case "$what" in
  save)
    echo "<H3>S&eacute;lectionnez les disques &agrave; sauvegarder</H3>"
    echo " $what / $NAME / $sav<br><br>"

    echo
    echo "Clicker sur le nom du disque pour indiquer<br>"
    echo "quelles partitions sauvegarder<br><br>"
    ;;

  restore)
    echo "<H3>S&eacute;lectionnez les disques &agrave; restaurer</H3>"

    echo "$what / $NAME / $sav<br><br>"

    echo
    echo "Clicker sur le nom du disque pour indiquer<br>"
    echo "quelles partitions restaurer.<br><br>"
    echo
    ;;

  default)
    echo invalid parameter
    exit 1 ;;
esac

echo "<form action=\"$ACTION\" method=\"POST\">"
echo "<input type=hidden name=mac value=\"$mac\">"
echo "<input type=hidden name=what value=\"$what\">"

echo '<table>'

for disk in `disklist.sh $sav` ; do
  echo '<tr>'
  echo '<td>'
     if [ "$WORKDIR/image/$mac/$sav" = "$current" ] ; then
       checked=" checked=on"
     else
       checked=
     fi
  echo "<INPUT TYPE=checkbox NAME=\"$mac/$sav/$disk\"$checked><a href=\"$SAVLINK?$what&$NAME&$sav&$disk\">$disk</a>"
  echo '</td>'
  echo '</tr>'

done

echo '<tr>'
echo '<td>'
echo '</td>'
echo '</tr>'
echo '</table><br>'

echo '<input type="submit" value="Appliquer" name="submit">'
echo '</form>'

echo '</body>'
echo '</html>'
