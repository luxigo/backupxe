#!/bin/sh
. /pxe/etc/config

echo Content-type: text/html
echo 
echo '<html><body>'

for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
  machine=`echo $param | cut -f 2 -d =`
  name=`egrep "^$machine " /pxe/etc/machines | cut -f 2 -d ' '`
  if [ -z "$name" ] ; then
    name=$machine
 fi
  namelist="$namelist$name "
done

if [ -n "$namelist" ] ; then
  echo "/pxe/bin/lansleep.sh $namelist"  
  eval "/pxe/bin/lansleep.sh $namelist"  
else
  echo nothing to do
fi

echo '</body></html>'

