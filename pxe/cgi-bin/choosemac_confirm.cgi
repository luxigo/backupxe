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

# usage: choosemac_confirm.cgi <var>=<url_encoded_value> ...
# VARIABLES:
# what=<save|restore|job>             what are we gonna do today
# save.<mac>=on                       write jobq for <mac> (format: 00-ab-12-34-56-78) [ jobq.<mac> must be the next parameter ]
# jobq.<mac>=<url_encoded_script>     jobq for <mac> [ warning: must be specified right after save.<mac> ]
# <mac>=on                            specify the target machines
# commands=<url_encoded_script>       commands to add to target machines jobqs

set -x
set -e

WORKDIR=/pxe

if [ -z "$HTTP_HOST" ] ; then

  POSTDATA="$1"
  shift
  while [ -n "$1" ] ; do
    POSTDATA="$POSTDATA&$1"
    shift
  done
  nohtml=1

else

  echo Content-type: text/html
  echo
  echo '<html>'

  POSTDATA=`cat`

fi

n=1
while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break

  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  case $pname in
    what) what=$pval ; continue ;;
    commands) commands=$pval ; continue ;;
  esac

  if echo $pname | egrep -q ^save\. ; then
      mac=`echo $pname | sed -r -n -e 's/^save\.//p'`
    if [ -n "$tosave" ] ; then
      tosave=$tosave\ $mac
    else
      tosave=$mac
    fi
    continue
  fi

  if echo $pname | egrep -q ^jobq\. ; then
    mac2=`echo $pname | sed -r -n -e 's/^jobq\.//p'`
    if [ "$mac" = "$mac2" ] ; then
      echo -n $pval | urldecode > $WORKDIR/jobq/$mac
    fi
    continue
  fi

  if [ "$pval" = "on" ] ; then
    if [ -n "$maclist2" ] ; then
      maclist2=$maclist2\ $pname
    else
      maclist2=$pname
    fi
    continue
  fi

done

for mac in $maclist2 ; do

  case $what in
  save|restore)

    current=`cat $WORKDIR/image/$mac/current`

    partlist=
    for part in `cat $current/partitions.$what` ; do
      if echo part | grep -q '^#' ; then
        continue
      fi
      partlist="$partlist$part "
    done

    if [ -z "$partlist" ] ; then
       echo $mac skipped: nothing to $what
       [ -z "nohtml" ] && echo '<br>'
       continue
    fi

    disk=`basename $part | sed -r -e 's/[0-9]+//'`

    if [ -f $current/sf$what ] ; then
      case $what in
      save)
           cmd="sfdisk $disk -d > $current/$disk.sf" ;;

      restore)
        if [ ! -f "$current/$disk.sf" ] ; then
            echo "$disk: partition table backup not found in directory $current<br>"
            error=1
            continue
        fi
 #         sed -r -e 's/\/sd./\/hd'$drive'/' -e t -e 's/\/hd./\/sd'$drive'/' $current/$disk2.sf > $current/$disk.sf
        cmd="sfdisk /dev/$disk < $current/$disk.sf"
        ;;
      esac

      echo $cmd >>  $WORKDIR/jobq/$mac
      if [ $? -ne 0 ] ; then
        echo "could not write to $WORKDIR/jobq/$mac<br>"
      fi
    fi

    if [ -f $current/mbr$what ] ; then
      case $what in
      save)
        cmd="dd if=/dev/$disk of=$current/$disk.mbr bs=512 count=1" ;;

      restore)
        if [ ! -f $current/$disk.mbr ] ; then
           echo "file not found: $current/$disk.mbr<br>"
           error=1
           cmd=
        else
          cmd="dd of=/dev/$disk if=$current/$disk.mbr bs=512 count=1"
        fi
        ;;
      esac
      [ -n "$cmd" ] && echo $cmd >> $WORKDIR/jobq/$mac
    fi

    for part in $partlist ; do
      if [ -f "$current/`basename $part`" ] || [ "$what" = "save" ] ; then
        backupfile="$current/`basename $part`"
      else
        backupfile="$current/`basename $part | tr sh hs`"
        if [ ! -f "$backupfile" ] ; then
          echo "$part: backup file not found in directory \"$current\"<br>"
          exit 1
        fi
      fi
      cmd="partimage-$what.sh $part $backupfile"
      if ! grep -q "$cmd" $WORKDIR/jobq/$mac ; then
        echo $cmd >> $WORKDIR/jobq/$mac
        if [ $? -ne 0 ] ; then
          echo "could not write to $WORKDIR/jobq/$mac<br>"
        fi
      fi
    done ;;

  esac

  if [ -n "$commands" ] ; then
    echo -n $commands | urldecode >> $WORKDIR/jobq/$mac
    if [ $? -ne 0 ] ; then
      echo "could not write to $WORKDIR/jobq/$mac<br>"
    fi
  fi

done

[ -n "$nohtml" ] && exit

[ -n "$error" ] && exit 1

echo '<head>'
echo '<META HTTP-EQUIV="Refresh"'
echo " CONTENT=\"3; URL=/pxe/empty.html\">"
echo

echo '</head>'
echo '<body>'
echo "<H3 align=center><a href=/pxe/empty.html>Votre demande a &eacute;t&eacute; enregistr&eacute;e</a></H3>"

echo '</body>'
echo '</html>'
