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
  case "$pname" in
    mac) mac=$pval ; continue ;;
    what) what=$pval ; continue ;;
    sav) sav=$pval ; continue ;;
  esac

done

echo '<html>'
echo $POSTDATA
current=$WORKDIR/image/$sav
if  ! cd $current ; then
  current=$WORKDIR/image/global/$sav
  if ! cd $current ; then
    echo cannot change to directory $current
    exit 1
  fi
fi

echo '<head>'
echo '<META HTTP-EQUIV="Refresh"'
echo " CONTENT=\"1; URL=/pxe/backuplan2.html\">"
echo
echo '</head>'

echo '<body>'

if [ -z "$sav" ] ; then

  echo vous devez s&eacute;lectionner une sauvegarde

else

  echo $current > $WORKDIR/image/$mac/current
  if [ $? -ne 0 ] ; then
    echo cant open $WORKDIR/image/$mac/current for writing
    exit 1
  fi

  echo "<H3 align=center><a href=choosesav.cgi?$what&$mac>Votre s&eacute;lection a &eacute;t&eacute; enregistr&eacute;e</a></H3>"

fi

echo '</body>'
echo '</html>'
