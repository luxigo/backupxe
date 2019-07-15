#!/bin/sh
. /pxe/etc/config

echo Content: text/plain
echo
POSTDATA=`cat`
n=1
while true ; do
  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`
  if [ "$pname" == "submit" ] ; then
    action=$pval
  else
    if [ -n "$maclist" ] ; then
      maclist=$maclist\ $pname
    else
      maclist=$pname
    fi
  fi
  n=`expr $n + 1`
done

[ -z "$action" ] && exit 1

if [ -x "`which q$action`" ] ; then
  q$action html $maclist
else
  exit 1
fi
