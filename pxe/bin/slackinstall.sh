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

PATH=/usr/lib/setup:$PATH

wgetit () {

  fn=`echo $@ | sed -r -n -e 's/.*:\/\/[^\/]+\/(.*)/\1/p'`
  derr=0
  while true ; do

    dialog --backtitle "Downloading..." --infobox  "$fn" 0 0
    wget $@ 1> $ROOT/tmp/wget.$$.tmp 2> $ROOT/tmp/wget.$$.tmp

    if [ $? -eq 0 ] ; then
       return 0
    else

      dialog --backtitle "Download Failed: $fn" --extra-button --ok-label Retry --extra-label Skip --yesno "`tail $ROOT/tmp/wget.$$.tmp`" 10 80
      derr=$?

      case $derr in
        3)
# skip
          rm $ROOT/tmp/wget.$$.tmp 2 > /dev/null
          return 1 ;;
        1)
          exit 1 ;;
        0)
          continue ;;
        default)
          doexit 1 ;;
      esac

    fi

  done

  rm $ROOT/tmp/wget.$$.tmp 2 > /dev/null

}

if [ ! -f $ROOT/etc/slackware-mirror ] ; then
   choosemirror || doexit 1
fi

MIRROR=`cat $ROOT/etc/slackware-mirror`

[ -z "$ROOT" ] && ROOT=/

export ROOT
verbose=0

WORKDIR=$ROOT/tmp/slackware/slackware

if killall -0 gpm ; then
#  echo killing gpm...
#  sleep 1
  gpm -k 2> /dev/null
fi

mkdir -p $WORKDIR || exit 1
cd $WORKDIR || exit 1

echo "--------------------------`date`" >> $ROOT/tmp/install.log
[ $verbose -ne 0 ] && tail -f --pid=$$ -n 1 $ROOT/tmp/install.log &

# downloading FILE_LIST

if [ ! -f FILE_LIST ] ; then
  echo Downloading slackware/FILE_LIST >> $ROOT/tmp/install.log
  wgetit $MIRROR/slackware/FILE_LIST || exit 1
fi
grep \.tgz\$ FILE_LIST > TGZ_LIST
TGZ_LIST=$WORKDIR/TGZ_LIST

clear

if [ ! -f $WORKDIR/a/tagfile ] ; then
  tagedit || exit 1
fi

for serie in a ap d e f k kde kdei l n t tcl x xap y ; do

  mkdir -p $WORKDIR/$serie || exit 1
  cd $WORKDIR/$serie || exit 1

  if [ ! -f tagfile ] ; then
    echo Downloading slackware/$serie/tagfile >> $ROOT/tmp/install.log
    wgetit $MIRROR/slackware/$serie/tagfile || exit 1
  fi

  for pkg in `egrep -E :\ *ADD\$ tagfile | cut -d : -f 1` ; do
    pkgpath=`grep /$serie/$pkg\-\[0-9\] $TGZ_LIST | sed -r -n -e 's/.* \.\/(.*)/\1/p' || grep /$serie/$pkg\-\[^0-9\ \-\]*\[0-9\] $TGZ_LIST | sed -r -n -e 's/.* \.\/(.*)/\1/p'`
    if [ -z "$pkgpath" ] ; then
       dialog --msgbox "error: cant find $pkg in $TGZ_LIST" 0 0
       echo error: cant find $pkg in $TGZ_LIST
       continue
    fi
    url=$MIRROR/slackware/$pkgpath

    [ -z "$url" ] &&  continue

    if echo $url | grep -q '.*\.tgz.*\.tgz$' ; then
       echo $url >>  $ROOT/tmp/install.log
       echo multiple matches >>  $ROOT/tmp/install.log
       exit 1
    fi

    base=`basename "$url" .tgz`
    if [ ! -f $ROOT/var/log/packages/$base ] ; then
      echo Downloading $pkg >> $ROOT/tmp/install.log
      wgetit -c $url || continue

      if [ ! -f $base.txt ] ; then
        wgetit -q $MIRROR/slackware/$serie/$base.txt || echo $base.tgz > $base.txt
      fi
      dialog --backtitle "Installing $base" --infobox "`sed -r -n -e 's/^[^ :]+: //p' $base.txt`" 11 -1

      installpkg -root $ROOT $base.tgz >> $ROOT/tmp/install.log || exit 1
    else
      dialog --infobox "Already installed: $pkg" 6 70
      echo  "Already installed: $pkg" >> $ROOT/tmp/install.log
    fi

  done

  cd ..

done

ldconfig -r $ROOT
