#!/bin/sh
. /pxe/etc/config

WORKDIR=/pxe
set -e
set -x

if [ -z "$HTTP_HOST" ] ; then

  POSTDATA="$1"
  shift
  while [ -n "$1" ] ; do
    POSTDATA="$POSTDATA&$1"
    shift
  done
  nohtml=1

else

  echo Content-type: text/html
  echo
  echo '<html>'

  POSTDATA=`cat`

fi


n=1
while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  case "$pname" in
   mac) mac=$pval ; continue ;;
   dir) dir=`echo $pval | urldecode` ; continue ;;
   disk) disk=$pval ; continue ;;
   sav) sav=$pval ; continue ;;
   name) name=$pval ; continue ;;
   what) what=$pval ; continue ;;
   MBR) MBR=$pval ; continue ;;
   PTBL) PTBL=$pval ; continue ;;
  esac

  if [ "$pval" = "on" ] ; then
    devname=`echo $pname | sed -r -n -e 's/\%2F/\//pg'`
    if [ -z "$devlist" ] ; then
      devlist=$devname
    else
      devlist="$devlist $devname"
    fi
  fi 
done

current=$dir
if  ! cd $current ; then

  [ -z "$nohtml" ] &&  echo '<body>'
  echo cannot change to directory $current
  [ -z "$nohtml" ] &&  echo '</body>'
  [ -z "$nohtml" ] &&  echo '</html>'
  exit 1

fi

if [ -z "$nohtml" ] ; then

  echo '<head>'
  echo '<META HTTP-EQUIV="Refresh"'
  echo " CONTENT=\"1; URL=choosepart.cgi?$what&$name&$sav&$disk\">"
  echo 
  echo '</head>'

  echo '<body>'

fi

if [ -n "$MBR" ] ; then
  [ ! -f "mbr$what" ] && touch "mbr$what"
else
  [ -f "mbr$what" ] && rm "mbr$what"
fi 

if [ -n "$PTBL" ] ; then
  [ ! -f "sf$what" ] && touch "sf$what"
else
  [ -f "sf$what" ] && rm "sf$what"
fi

touch partitions.$what.$$.new
if [ $? -ne 0 ] ; then
  echo "cant write to `pwd`/partitions.$what.$$.new<br>"
  echo "check file permissions<br>"
  echo 
  exit 1
fi

if [ "$what" = "restore" ] ; then
  if [ ! -f partitions.restore ] ; then
    cp -a partitions.save partitions.restore || exit 1
  fi
fi
  
if [ ! -f partitions.$what ] ; then
   echo "file not found: `pwd`/partitions.$what<br>"
   exit 1
fi

for part in "`cat ./partitions.$what`" ; do
   found=0
   for dev in $devlist ; do
      if [ "$dev" = "$part" ] ; then
        echo $part >> partitions.$what.$$.new
        found=1
        break
      fi
      if [ "#$dev" = "$part" ] ; then
        echo $dev >> partitions.$what.$$.new
        found=1
        break
      fi
    done
    if [ $found -eq 0 ] ; then
      part=`echo $part | cut -f 2 -d \\#` 
      prefix="#"
      echo $prefix$part >> partitions.$what.$$.new
    fi
done

cat partitions.$what.$$.new > partitions.$what
if [ $? -ne 0 ] ; then
  echo "cant write to `pwd`/partitions.$what<br>"
  echo "check file permissions<br>"
  echo 
  exit 1
fi

rm partitions.$what.$$.new
 
[ -n "$nohtml" ] && exit

echo "<H3 align=center><a href=\"choosepart.cgi?$what&$name&$sav&$disk\">Votre s&eacute;lection a &eacute;t&eacute; enregistr&eacute;e</a></H3>"

echo '</body>'
echo '</html>'
