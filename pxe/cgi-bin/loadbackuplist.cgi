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

. /pxe/etc/debug
. /pxe/bin/auth

set -e
echo Content-Type: text/html
echo

HOSTSMAC=/pxe/etc/hosts.mac
IMAGE_DIR=/pxe/image

count=`cat $HOSTSMAC | wc -l`

i=0
for dirname in `ls -1d $IMAGE_DIR/00* $IMAGE_DIR/global/* | sort -u` ; do
	echo -n "backupdir[$i]='$dirname';"
 	i=`expr $i + 1`
done
