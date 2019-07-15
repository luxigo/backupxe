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

echo Content: text/plain
echo
POSTDATA=`cat`
n=1
while true ; do
  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`
  if [ "$pname" == "submit" ] ; then
    action=$pval
  else
    if [ -n "$maclist" ] ; then
      maclist=$maclist\ $pname
    else
      maclist=$pname
    fi
  fi
  n=`expr $n + 1`
done

[ -z "$action" ] && exit 1

if [ -x "`which q$action`" ] ; then
  q$action html $maclist
else
  exit 1
fi
