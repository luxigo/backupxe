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

what=`echo $1 | cut -f 1 -d \\\\`
name=`echo $1 | cut -f 2 -d \& | cut -f 1 -d \\\\`
SAVNAME=`echo $1 | cut -f 3 -d \& | cut -f 1 -d \\\\`
disk=`echo $1 | cut -f 4 -d \& | cut -f 1 -d \\\\`

ACTION=/cgi-bin/pxe/choosepart_apply.cgi
WORKDIR=/pxe

echo Content-type: text/html
echo
echo '<html>'
echo '<body>'

case "$what" in
  save)
    echo "<H3>S&eacute;lectionnez les partitions &agrave; sauvegarder</H3>"
    ;;

  restore)
    echo "<H3>S&eacute;lectionnez les partitions &agrave; restaurer</H3>"
    echo
    ;;

  default)
    echo invalid parameter
    exit 1 ;;
esac

if egrep -q \ $name\$ $WORKDIR/etc/hosts.mac ; then
  mac=`grep $name $WORKDIR/etc/hosts.mac | cut -f 1 -d \ `
else
  mac=$name
fi

if [ -d $WORKDIR/image/$mac/$disk ] ; then
  dir=$mac/$disk
else
  if [ ! -d $WORKDIR/image/global/$SAVNAME/$disk ] ; then
    echo $WORKDIR/image/$mac/$disk not found
    echo $WORKDIR/image/global/$SAVNAME/disk not found
    exit 1
  fi
  dir=global/$SAVNAME/$disk
fi

cd $WORKDIR/image/$dir || exit 1

echo " $what / <a href=\"choosesav.cgi?$what&$mac\">$name</a> / $SAVNAME / $disk<br><br>"

echo "<form action=\"$ACTION\" method=\"POST\">"
echo "<input type=hidden name=what value=\"$what\">"
echo "<input type=hidden name=name value=\"$name\">"
echo "<input type=hidden name=mac value=\"$mac\">"
echo "<input type=hidden name=dir value=\"`pwd`\">"
echo "<input type=hidden name=sav value=\"$SAVNAME\">"
echo "<input type=hidden name=disk value=\"$disk\">"

checked=
if [ -f mbr$what ] ; then
  checked=" checked=on"
fi
echo "<input type=checkbox name=MBR$checked>Master Boot Record<br>"

checked=
if [ -f sf$what ] ; then
  checked=" checked=on"
fi
echo "<input type=checkbox name=PTBL$checked>Table de Partition<br><br>"
echo '<table>'

if [ ! -f partitions.$what ] ; then
  if [ "$what" = "restore" ] ; then
     cp -a partitions.save partitions.restore
  fi
fi

if [ ! -f partitions.$what ] ; then
   echo file not found: `pwd`/partitions.$what
   echo "<br>"
   exit 1
fi

for part in `cat partitions.$what` ; do

  echo '<tr>'
  echo '<td>'

  if echo $part | egrep -q '^#'  ; then
    partoff=`echo $part | cut -f 2 -d \#`
    echo "<INPUT TYPE=checkbox NAME=$partoff>$partoff"
  else
    echo "<INPUT TYPE=checkbox NAME=$part checked=on>$part"
  fi

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
