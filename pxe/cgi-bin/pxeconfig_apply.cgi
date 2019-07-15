#!/bin/sh
. /pxe/etc/config

WORKDIR=/pxe
PXEUSER=Administrateur

set -e

echo Content-type: text/html
echo

POSTDATA=`cat`
n=1
while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  if [ "$pval" = "on" ] ; then
    if [ -z "$maclist" ] ; then
      maclist=$pname
    else
      maclist="$maclist $pname"
    fi
    continue
  fi

done

echo '<html>'
echo '<head>'
echo '<META HTTP-EQUIV="Refresh"'
echo " CONTENT=\"3; URL=pxeconfig.cgi\">"
echo
echo '</head>'
echo '<body>'

cd /tftpboot/pxelinux/pxelinux.cfg || exit 1

for mac in $maclist ; do 

  bootfile=`echo $POSTDATA | sed -r -n -e 's/.*cfg\.'$mac'=([^&]+).*/\1/p'`
  [ -z "$bootfile" ] && exit 

  if [ "$mac" = "default" ] ; then  
     fn=default
  else
     fn=01-$mac
  fi

  if [ -L "$fn" ] ; then
    rm $fn
    if [ $? -ne 0 ] ; then
      echo "couldnt remove link: $fn "
      exit 1 
    fi
  else
    if [ -f "$fn" ] ; then
       echo not a symlink: `pwd`/$fn
       exit 1
    fi
  fi

  [ "$bootfile" = "default" ] && continue

  ln -sf $bootfile $fn

  if [ $? -ne 0 ] ; then
     echo couldnt create link: "ln -sf $bootfile $fn" 
     exit 1
  fi

done

echo "<H3 align=center><a href=/pxe/empty.html>Votre s&eacute;lection a &eacute;t&eacute; enregistr&eacute;e</a></H3>"

echo '</body>'
echo '</html>'
