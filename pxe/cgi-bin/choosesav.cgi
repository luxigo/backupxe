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

NAME=`echo $1 | cut -f 2 -d \&`
what=`echo $1 | cut -f 1 -d '\\'`

ACTION=/cgi-bin/pxe/choosesav_apply.cgi
SAVLINK=/cgi-bin/pxe/choosedisk.cgi
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
    echo "<H3>S&eacute;lectionnez un r&eacute;pertoire de destination</H3>"
    echo " $what / $NAME<br><br>"

    echo
    echo "Clicker sur le nom du repertoire pour indiquer<br>"
    echo "quels disques sauvegarder<br><br>"
    ;;

  restore)
    echo "<H3>S&eacute;lectionnez la sauvegarde &agrave; restaurer</H3>"

    echo "$what / $NAME<br><br>"

    echo
    echo "Clicker sur le nom de la sauvegarde pour indiquer<br>"
    echo "quels disques restaurer.<br><br>"
    echo
    ;;

  default)
    echo invalid parameter
    exit 1 ;;
esac

echo "<form action=\"$ACTION\" method=\"POST\">"
echo "<input type=hidden name=mac value=\"$mac\">"
echo "<input type=hidden name=what value=\"$what\">"

[ -f $WORKDIR/image/$mac/current ] && current=`cat $WORKDIR/image/$mac/current`

echo '<table>'

for sav in $mac `ls -1 $WORKDIR/image/global` ; do
  sav=`basename "$sav"`
  echo '<tr>'
  echo '<td>'
  if [ "$sav" = "`basename $current`" ] ; then
    checked="checked=on"
  else
    checked=
  fi
  echo "<INPUT TYPE=radio NAME=\"sav\" value=\"$sav\"$checked><a href=\"$SAVLINK?$what&$NAME&$sav\">$sav</a>"
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
