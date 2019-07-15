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

. /etc/config

set -x

logprefix () {
	echo `date +%Y%m%d-%H%M.%S` $0
}

rm /pxe/log/$HWADDR/problem 2> /dev/null || true
rm /pxe/log/$HWADDR/done 2> /dev/null || true
rm /pxe/log/$HWADDR/busy 2> /dev/null || true
rm /pxe/log/$HWADDR/bye 2> /dev/null || true
rm /pxe/log/$HWADDR/ready 2> /dev/null || true

busy $$ "$0" "$@"

LOGFILE=/pxe/jobq/$HWADDR.log

echo `logprefix` $@ >> $LOGFILE

if  [ ! -f /pxe/jobq/$HWADDR ] ; then
  problem $$ "cant read /pxe/jobq/$HWADDR"
  problem $$ waiting
  t=0;
  while true ; do
     sleep 10
     t=`expr $t + 10`
     if [ $t -gt 1200 ] ; then
       rm /pxe/log/$HWADDR/ready 2> /dev/null || true
       notice $$ timeout
       halt
     fi
     [ -f /pxe/jobq/$HWADDR ] && break
  done
  rm /pxe/log/$HWADDR/problem 2> /dev/null
fi


removejob () {

  if ! touch /pxe/jobq/$HWADDR.new ; then
    problem $$ cant write to /pxe/jobq/$HWADDR.new
    exit 1
  fi

  sed -r -e '1d' /pxe/jobq/$HWADDR > /pxe/jobq/$HWADDR.new

  if ! cat /pxe/jobq/$HWADDR.new > /pxe/jobq/$HWADDR ; then
    problem $$ cant write to /pxe/jobq/$HWADDR
    exit 1
  fi

  rm /pxe/jobq/$HWADDR.new

}

t=0
while true ; do

  SCRIPT=`sed -r -n -e '1p' /pxe/jobq/$HWADDR`

  if [ -z "$SCRIPT" ] ; then

     removejob
     remain=`wc -l /pxe/jobq/$HWADDR | cut -f 1 -d \ `
     [ $remain -gt 0 ] && continue

     [ ! -f /pxe/log/$HWADDR/ready ] && ready $$ jobq empty

     sleep 10
     t=`expr $t + 10`
     if [ $t -gt 1200 ] ; then
       rm /pxe/log/$HWADDR/ready 2> /dev/null
       notice $$ timeout
       halt
     fi

     continue

  else

    t=0

  fi

  echo `logprefix` $SCRIPT >> $LOGFILE

  case `echo $SCRIPT | cut -f 1 -d \ ` in
    halt|reboot|shutdown)
       removejob
       rm /pxe/log/$HWADDR/ready 2> /dev/null
       notice $$ $SCRIPT
       eval $SCRIPT
       exit 0 ;;
  esac

  rm /pxe/log/$HWADDR/ready 2> /dev/null
  busy $$ $SCRIPT

  err=0
  if ! eval "$SCRIPT 2>> $LOGFILE" ; then
     err=$?
     echo `logprefix` $err >> $LOGFILE
     problem $$ $err $SCRIPT
     exit 1
  fi

  echo `logprefix` done >> $LOGFILE
  rm /pxe/log/$HWADDR/busy 2> /dev/null
  /usr/bin/done $$ $SCRIPT

  removejob

done
