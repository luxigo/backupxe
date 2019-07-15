#!/bin/sh
. /pxe/etc/config

WORKDIR=/pxe

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
  case "$pname" in
    mac) mac=$pval ; continue ;;
    what) what=$pval ; continue ;;
    sav) sav=$pval ; continue ;;
  esac

done

echo '<html>'
echo $POSTDATA
current=$WORKDIR/image/$sav
if  ! cd $current ; then
  current=$WORKDIR/image/global/$sav
  if ! cd $current ; then
    echo cannot change to directory $current
    exit 1
  fi
fi

echo '<head>'
echo '<META HTTP-EQUIV="Refresh"'
echo " CONTENT=\"1; URL=/pxe/backuplan2.html\">"
echo 
echo '</head>'

echo '<body>'

if [ -z "$sav" ] ; then

  echo vous devez s&eacute;lectionner une sauvegarde 

else

  echo $current > $WORKDIR/image/$mac/current
  if [ $? -ne 0 ] ; then
    echo cant open $WORKDIR/image/$mac/current for writing  
    exit 1
  fi

  echo "<H3 align=center><a href=choosesav.cgi?$what&$mac>Votre s&eacute;lection a &eacute;t&eacute; enregistr&eacute;e</a></H3>"

fi

echo '</body>'
echo '</html>'
