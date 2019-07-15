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

#-----------------------------6451759192554576801115574341
#Content-Disposition: form-data; name="fileforminput"; filename="filename.txt"
#Content-Type: text/plain
. /pxe/etc/config

MAPFILE="/pxe/htdocs/pics/map.png"
MAPSDIR="/pxe/htdocs/pics/maps"
OLDMAPFILE="/pxe/htdocs/pics/oldmap.png"

set -e

echo Content-Type: text/html
echo Pragma: no-cache
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        file) file=`basename $value` ;;
                        room) room=$value ;;
                esac
        done
fi

_exit() {
  echo "$1"
  rm $POSTDATA 2> /dev/null || true
  exit 1
}

POSTDATA=/tmp/postdata.$$.tmp
cat > $POSTDATA

chmod +r $POSTDATA

TMPFILE="/tmp/file.$$.tmp"
HEADERS="/tmp/headers.$$.tmp"
boundary=`echo $CONTENT_TYPE | sed -r -n -e 's/.* boundary=([^\ ]+).*/\1/p'`
form-data $HEADERS $boundary form-data $POSTDATA > $TMPFILE

chmod +r $TMPFILE
chmod +r $HEADERS

if ! NAME=`sed -r -n -e '/Content-[Dd]isposition: form-data; name="([^\"]*)"/!b' -e 's/Content-[Dd]isposition: form-data; name="([^\"]*).*/\1/p' -e q $HEADERS` ; then
  _exit 'Error : cant parse headers [1]'
fi

if ! FILENAME=`sed -r -n -e '/Content-[Dd]isposition: form-data; name="'$NAME'"/!b' -e 's/.* filename="([^\"]*).*/\1/p' -e q $HEADERS` ; then
  _exit 'Error : cant parse headers [2]'
fi

FILENAME=`basename $FILENAME`
if echo $FILENAME | grep -q '\.\.' ; then
  _exit 'Error: double dot in filename'
fi

DESTPNG=`echo $FILENAME | sed -r -e 's/\.[^\.]+$//'`.png
if [ "$FILENAME" != "$DESTPNG" ] ; then
	convert "$TMPFILE" "/tmp/tmp.$$.$DESTPNG" || _exit 'Error: cant convert image'
	TMPFILE="/tmp/tmp.$$.$DESTPNG"
fi

cp "$TMPFILE" "$MAPSDIR/$DESTPNG"
cat "$TMPFILE" > "$MAPFILE"
rm /tmp/*.$$.*

cat << EOF
<html>
<head>
<script>
top.img.src="/pxe/pics/maps/$DESTPNG";
top.setTimeout("showpclist();",100);
top.innerHTML_restore("divmapupload");

</script>
</head>
<body>
</body>


EOF
