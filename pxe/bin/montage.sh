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

[ -z "$1" ] && exit 1
PATH=/pxe/bin/`uname -m`:/pxe/bin:$PATH
LD_LIBRARY_PATH=/pxe/lib/`uname -m`:/pxe/lib:$LD_LIBRARY_PATH

BASICON=/pxe/htdocs/thumbs/pc.png
[ `uname -m` = 'mips' ] && exit 0

if [ $1 -lt 10 ] ; then
	montage -border 0x0 -borderwidth 0 -font fixed -fill white -annotate +21+18 $1 $BASICON /pxe/htdocs/thumbs/pc$1.tmp.png
else
	if [ $1 -lt 100 ] ; then
		montage -border 0x0 -borderwidth 0 -font fixed -fill white -annotate +17+18 $1 $BASICON /pxe/htdocs/thumbs/pc$1.tmp.png
  	else
		montage -border 0x0 -borderwidth 0 -font fixed -fill white -annotate +14+18 $1 $BASICON /pxe/htdocs/thumbs/pc$1.tmp.png
	fi
fi

convert -transparent blue -crop 48x47+40+40 /pxe/htdocs/thumbs/pc$1.tmp.png /pxe/htdocs/thumbs/pc$1.png
convert -resize 24x24 /pxe/htdocs/thumbs/pc$1.png /pxe/htdocs/thumbs/pc$1_24x24.png
