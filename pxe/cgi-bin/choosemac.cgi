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

ACTION=/cgi-bin/pxe/choosemac_next.cgi
MACLINK=/cgi-bin/pxe/choosesav.cgi
WORKDIR=/pxe
PXEUSER=int4
echo Content-type: text/html
echo
echo '<!doctype html public "-//w3c//dtd html 4.0 transitional//en">'
echo '<html>'
echo '<body>'

echo '<form name=myform action="/pxe/backuplan2.html" target=frame2>'
echo '</form>'
echo '<script>document.forms[0].submit()</script>'

what="$1"
case "$what" in
  save)
    echo "<H3>S&eacute;lectionnez les machines &agrave; sauvegarder</H3>"
    echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / $what<br><br>"
    echo "Cochez les machines &agrave; sauvegarder et clickez"
    echo "sur \"suivant\".<br><br>"
    echo "Ou bien clickez sur le nom de la machine pour modifier"
    echo "les param&egrave;tres de la sauvegarde.<br><br>"
    ;;

  restore)
    echo "<H3>S&eacute;lectionnez les machines &agrave; restaurer</H3>"
    echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / $what<br><br>"
    echo "Cochez les machines &agrave; restaurer et clickez"
    echo "sur \"suivant\".<br><br>"
    echo "Ou bien clickez sur le nom de la machine pour modifier"
    echo "les param&egrave;tres de la restauration.<br><br>"
    ;;

  job)
    echo "<H3>S&eacute;lectionnez les machines cibles</H3>"
    echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / $what<br><br>"
    echo
    ;;

  power)
    echo "<H3>Allumer / Eteindre les machines</H3>"
    echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / power<br><br>"
    echo
    echo "Cocher les machines &agrave; allumer.<br>"
    echo "D&eacute;cocher les machines &agrave; &eacute;teindre.<br>"
    echo "Cliquer sur appliquer.<br><br>"
    ;;

  default)
    echo invalid parameter
    exit 1 ;;
esac

echo '<input type="button" value="Tout" onclick="parent.checkAll();">'
echo '<input type="button" value="Rien" onclick="parent.uncheckAll();">'
echo '<input type="button" value="Inverser" onclick="parent.switchAll();">'
echo '<br>'
echo '<br>'
echo "<form name=choosemac action=\"$ACTION\" method=\"POST\" target=frame2>"
echo "<input type=hidden name=what value=$what>"
echo '<table>'

echo '<script>parent.maccount=0;</script>'

if [ "$what" = "power" ] ; then
  moremac=" 1"
fi

for mac in `maclist.sh$moremac` ; do

  macjs=`echo $mac | tr - _`

  echo '<script>parent.mac[parent.maccount]="'$macjs'"; parent.maccount=parent.maccount+1;</script>'

  if grep -q $mac $WORKDIR/etc/hosts.mac ; then
    name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
    if [ -z "$name" ] ; then
       name=$mac
    fi
  else
     name=$mac
  fi

  echo '<tr>'
  echo '<td>'

  checked=
  if [ "$what" = "power" ] ; then
    mac0=`echo $mac | tr '-' ':' | tr A-Z a-z`
    ip=`dhcplease $mac0`
    echo $mac0 $ip

    if [ -n "$ip" ] ; then
      online=0
      ssh -o PasswordAuthentication=no $PXEUSER@$ip pwd > /dev/null && online=1
      if [ $online -eq 0 ] ; then
        if false ; then
        #if ping -c 1 -w 1 $ip > /dev/null ; then
           online=1
        else
           if [ "$mac" = "`arp -n $ip | sed -r -n -e 's/:/-/g' -e 's/.* ([0-9A-F][0-9A-F]-[0-9A-F\-]+).*/\1/p' | tr A-Z a-z`" ] ; then
             online=1
           fi
        fi
      fi
      if [ $online -eq 1 ] ; then
        checked=" checked=on"
      fi
    fi
  fi

  echo "<INPUT TYPE=checkbox NAME=\"M$macjs\" href=\"#$mac\" $checked>"
  if [ "$what" = "save" ] || [ "$what" = "restore" ] ; then
       echo "<a href=\"$MACLINK?$what&$name\" target=frame2>$name</a>"
  else
       echo $name
       echo '<br>'
  fi
  echo '</td>'
  echo '</tr>'

done

echo '<tr>'
echo '<td>'
echo '</td>'
echo '</tr>'
echo '</table><br>'

echo "<input type=\"submit\" value=\"Suivant\" name=\"submit\">"
echo '</form>'
echo '</body>'
echo '</html>'
