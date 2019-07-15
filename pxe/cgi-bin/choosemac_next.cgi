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

WORKDIR=/pxe

echo Content-type: text/html
echo

POSTDATA=`cat`
n=1

while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  case $pname in
   what) what=$pval ;;
  esac

  if [ "$pval" = "on" ] ; then
    maclist="$maclist`echo $pname | sed -r -e 's/^M//' -e 's/_/-/g'` "
    continue
  fi

done

echo '<html>'

if [ -z "$maclist" ] ; then
  echo '<head>'
  echo '<META HTTP-EQUIV="Refresh"'
  echo " CONTENT=\"1; URL=/pxe/empty.html\">"
  echo '</head>'
  echo '<body>'
  echo "<H3 align=center><a href=/pxe/empty.html>La s&eacute;lection est vide</a><H3>"
  echo '</body>'
  echo '</html>'
  exit
fi

echo '<body>'

case $what in
  save) echo '<H3>Confirmez votre demande de sauvegarde</H3>' ;;
  restore) echo '<H3>Confirmez votre demande de restauration</H3>' ;;
  job) echo '<H3>Modifier la liste des travaux en attente</H3>' ;;
esac
#echo " / <a href=\"/pxe\" target=frame0>home</a> / <a href=choosemac.cgi?$what target=frame1>$what</a> / confirmation <br><br>"

echo "<form action=\"choosemac_confirm.cgi\" method=\"POST\">"
echo "<input type=hidden name=what value=\"$what\">"

for mac in $maclist ; do

  echo '<table border=1>'

  if grep -q $mac $WORKDIR/etc/hosts.mac ; then
    name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
  else
    name=$mac
  fi

  echo "<tr><td align=center>"
  echo "<input type=checkbox name=\"$mac\" checked=on>"
#  echo "</td><td><a href=choosemac.cgi?$what>$name</a></td></tr>"
  echo "</td><td>$name</td></tr>"

  macdir=$WORKDIR/image/$mac
  if  ! cd $macdir ; then
    echo "cannot change to directory $macdir<br>"
    exit 1
  fi

  current=`cat current`
  if [ -z "$current" ] ; then
     echo "Vous devez d'abord s&eacute;lectionner une sauvegarde<br>"
     exit 1
  fi

  if [ "$what" != "job" ] ; then
    echo "<tr><td align=right>Directory</td><td><a href=\"choosesav.cgi?$what&$mac\">`basename $current`</a></td></tr>"

    if  ! cd $current ; then
      echo "cannot change to directory $current<br>"
      exit 1
    fi

    echo '<tr><td align=right>'
    echo "Partitions</td>"
    echo '<td>'
    if [ -f partitions.$what ] ; then
       echo "<a href=\"choosepart.cgi?$what&$mac&`basename $current`\">"
       cat partitions.$what
       echo '</a>'
    else
      if [ "$what" = "restore" ] ; then
        if [ -f partitions.save ] ; then
          echo "<a href=\"choosepart.cgi?$what&$mac&`basename $current`\">"
          cat partitions.save
          echo '</a>'
        else
          echo "cannot read `pwd`/partitions.save<br>"
          exit 1
        fi
      else
        echo "cannot read `pwd`/partitions.save<br>"
        exit 1
      fi
    fi
    echo '</td></tr>'

    echo '<tr><td align=center>'
    echo "MBR</td>"
    echo '<td>'
    echo "<a href=\"choosepart.cgi?$what&$mac&`basename $current`\">"
    if [ -f $current/mbr$what ] ; then
       echo Oui
     else
       echo Non
    fi
    echo '</a>'
    echo '</td></tr>'

    echo '<tr><td align=center>'
    echo "PTable</td>"
    echo '<td>'
    echo "<a href=\"choosepart.cgi?$what&$mac&`basename $current`\">"
    if [ -f $current/sf$what ] ; then
       echo Oui
     else
       echo Non
    fi
    echo '</a>'
    echo '</td></tr>'
fi

  echo '<tr><td align=center>'
#  echo '&nbsp;Jobs&nbsp;<br><br><br>'
#  echo '&nbsp;Modifier&nbsp;<br>'
  echo "<input type=checkbox name=\"save.$mac\"></td>"
  echo '<td>'
  echo "<textarea rows=6 wrap=virtual cols=80 name=\"jobq.$mac\">"
  cat /pxe/jobq/$mac
  echo '</textarea><br>'

#  sed -r -n -e 's/.*/\0<br>/p' /pxe/jobq/$mac
  echo '</td></tr>'
  echo '</table><br>'

done

if [ "$what" = "job" ] ; then
  echo '<H3>Ajouter des commandes</H3>'
  echo '<table border=1>'
  echo '<tr>'
# echo '<td>Commandes</td>'
  echo "<td><textarea rows=6 wrap=virtual cols=80 name=\"commands\">"
  echo '</textarea>'
  echo '</td></tr>'
  echo '</table><br>'
fi
echo '<input type=submit value="Confirmer" name="submit">'
echo '</form>'

echo '</body>'
echo '</html>'
