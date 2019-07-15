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

. /pxe/etc/config

set -e
. /etc/config

busy $$ "$0" "$@"

export IMAGE_DIR=`cat /pxe/etc/IMAGE_DIR`
PARTIMAGED=$REMOTESERVER
LOGFILE=/pxe/log/$HWADDR/partimage-restore.log

rm /pxe/log/$HWADDR/problem 2> /dev/null || true
rm /pxe/log/$HWADDR/done 2> /dev/null || true
rm /pxe/log/$HWADDR/busy 2> /dev/null || true
rm /pxe/log/$HWADDR/bye 2> /dev/null || true
rm /pxe/log/$HWADDR/ready 2> /dev/null || true

export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/usr/sbin:/bin:/usr/bin

touch $LOGFILE

err=0

if [ -z "$1" ] ; then

	for ARG in `cat /proc/cmdline` ; do
		name=`echo $ARG | cut -f 1 -d =`
		value=`echo $ARG | cut -f 2 -d =`
		case "$name" in
			IMAGE_DIR)
				IMAGE_DIR=$value
				PARTIMAGED=
				;;
		esac
	done

  partimage-restore $PARTIMAGED "$IMAGE_DIR" 2>> $LOGFILE || err=1

else
  partimage -o -b -f3 -s$PARTIMAGED restore "$1" "$2" 2>> $LOGFILE || err=1
fi

sleep 3

if [ $err -ne 0 ] ; then
   problem $$ $err
   if [ -n "$DEBUG" ] ; then
   	echo LOGFILE=$LOGFILE
	cat $LOGFILE
   fi
   exit 1
else
   /pxe/bin/setup.sh
   /usr/bin/done $$ $0 $@
   grep -q reboot /proc/cmdline && reboot
fi
