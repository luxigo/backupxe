#!/bin/sh
#-----------------------------6451759192554576801115574341
#Content-Disposition: form-data; name="fileforminput"; filename="filename.txt"
#Content-Type: text/plain
. /pxe/etc/config

MOVIESDIR="/var/www/movies"

set -e

echo Content-Type: text/html
echo Pragma: no-cache
echo

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

if ! PC=`sed -r -n -e '/Content-[Dd]isposition: form-data; name="([^\"]*)"/!b' -e 's/Content-[Dd]isposition: form-data; name="([^\"]*).*/\1/p' -e q $HEADERS` ; then
  _exit 'Error : cant parse headers [1]'
fi

if ! FILENAME=`sed -r -n -e '/Content-[Dd]isposition: form-data; name="'$PC'"/!b' -e 's/.* filename="([^\"]*).*/\1/p' -e q $HEADERS` ; then
  _exit 'Error : cant parse headers [2]'
fi

FILENAME=`basename $FILENAME`
if echo $FILENAME | grep -q '\.\.' ; then
  _exit 'Error: double dot in filename'
fi

cp "$TMPFILE" "$MOVIESDIR/$FILENAME"
setrec /pxe/etc/movies $PC http://movieserver.lan/movies/$FILENAME
rm /tmp/*.$$.*

cat << EOF
<html>
<head>
<script>
top.innerHTML_restore("divmapupload");
</script>
</head>
<body>
</body>


EOF

