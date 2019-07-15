#!/bin/sh
. /pxe/etc/config

WORKDIR=/pxe
PXEUSER=Administrateur

wakeupmachine () {
  while true ; do
    wakeonlan -i $destip -p 9 $mac
    if [ $? -ne 0 ] ; then
      echo `logprefix` error: cannot start the pc
      return 1
    fi
    [ -f $WORKDIR/$mac/ready ] && break
    sleep 10
  done
  return 0

}

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

  POSTDATA=`cat`

fi

n=1
while true ; do

  p=`echo $POSTDATA | cut -f $n -d \&`
  [ -z "$p" ] && break
  n=`expr $n + 1`

  pname=`echo $p | cut -f 1 -d =`
  pval=`echo $p | cut -f 2 -d =`

  case $pname in
   maclist) maclist=`echo $pval | urldecode` ;;
  esac

  if [ "$pval" = "on" ] ; then
    if [ -z "$onlist" ] ; then
      onlist=$pname
    else
      onlist="$onlist $pname"
    fi
    continue
  fi

done

[ -z "$nohtml" ] && echo '<html><body>'

for mac in $maclist ; do 

  if grep -q $mac $WORKDIR/etc/hosts.mac ; then
    name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
  else
    name=$mac
  fi

  for mac2 in $onlist ; do
    if [ "$mac" = "$mac2" ] ; then
       break
    fi
  done

  if [ "$mac" = "$mac2" ] ; then
    echo "starting  $mac<br>"
    wakeonlan -i $destip -p 9 $mac

  else
    ip=`dhcplease $mac`
    if [ -n "$ip" ] ; then
      echo "shuting down $mac<br>"
      ssh -o PasswordAuthentication=no $PXEUSER@$ip halt &
    fi
  fi

done

[ -z "$nohtml" ] && echo '</body></html>'
