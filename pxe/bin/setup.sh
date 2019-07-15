#!/bin/sh
# this script is run from rc.S

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
. /etc/config

export IMAGE_DIR=`cat /pxe/etc/IMAGE_DIR`
export PATH=/pxe/bin/`uname -m`:/pxe/bin:/usr/local/sbin:/usr/local/bin:/sbin:/usr/sbin:/bin:/usr/bin

#busy $$ "$0" "$@"

mkdir -p /pxe/log/$HWADDR || exit 1 # problem $$ "$0" $$
LOGFILE=/pxe/log/$HWADDR/partimage-save.log

rm /pxe/log/$HWADDR/done 2> /dev/null || true
rm /pxe/log/$HWADDR/bye 2> /dev/null || true
rm /pxe/log/$HWADDR/ready 2> /dev/null || true
rm /pxe/log/$HWADDR/problem 2> /dev/null || true

touch $LOGFILE || exit 1

name=`getrec /pxe/etc/hosts.mac $HWADDR`
if [ -z "$name" ] ; then
	addrec /pxe/etc/hosts.mac $HWADDR $HWADDR
fi
partimage-save -R $REMOTESERVER "$IMAGE_DIR" 2>> $LOGFILE
err=$?

if [ $err -ne 0 ] ; then
   problem $$ $err
   exit 1
fi

lspci > /pxe/log/$HWADDR/lspci
cat /proc/cpuinfo > /pxe/log/$HWADDR/cpuinfo
cat /proc/meminfo > /pxe/log/$HWADDR/meminfo
cat /proc/bus/usb/devices > /pxe/log/$HWADDR/devices
cardctl info > /pxe/log/$HWADDR/pcmcia
dmesg > /pxe/log/$HWADDR/dmesg

if [ $? -ne 0 ] ; then
   problem $$ $err
   exit 1
else
  /usr/bin/done $$ done
  grep -q reboot /proc/cmdline && reboot
  echo Done !
fi
