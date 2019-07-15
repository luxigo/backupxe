#!/bin/sh
. /pxe/etc/config
set -e
PCSTYLE=/pxe/etc/pcstyle

echo Content-type: text/html
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

  pc=`echo $param | cut -f 1 -d = | sed -r -n -e 's/^pc//p'`
  style=`echo $param | cut -f 2 -d =  | urldecode`

#  echo "pc$pc='$style'<br>"
  [ -z "$style" ] && continue
  [ -z "$pc" ] && continue
  [ "$style" = "undefined" ] && continue
  [ "$pc" = "undefined" ] && continue
  echo $style | grep -q \- && continue
  
  setrec $PCSTYLE $pc $style
  
done

killall getpcicons.sh > /dev/null 2>&1 || true
( /pxe/bin/getpcicons.sh "register" 
/pxe/bin/getpcicons.sh "default" ) 1>&- &

