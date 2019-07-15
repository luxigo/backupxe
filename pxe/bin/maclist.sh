#!/bin/sh

. /pxe/etc/config

mysql() {
 return
}

WORKDIR=/pxe

cd $WORKDIR/image || exit 1

if [ -z "$1" ] ; then

  for mac in `ls -1 -d 00-*` ; do
#   if grep -q $mac $WORKDIR/etc/hosts.mac ; then
#     grep $mac $WORKDIR/etc/hosts.mac
#   else
#     echo $mac $mac
#   fi
     echo $mac
  done

else
   for i in `nbtscan.sh | sed -r -n -e 's/.* ([0-9a-f\-]+.*)/\1/p'` ; do
      if echo $i | grep -q ^0 ; then
        mac=$i
      else
        [ "$mac" = "00-00-00-00-00-00" ] && continue
        name=$i
	if [ "$name" = "<unknown>" ] ; then
		name=""
	fi
        touch /pxe/etc/hosts.mac || exit 1
        if grep -q $mac /pxe/etc/hosts.mac ; then
          [ -z "$name" ] && continue
          setrec /pxe/etc/hosts.mac $mac $name
#          sed -r -e "s/$mac.*/$mac $name/" /pxe/etc/hosts.mac > /tmp/hosts.mac.$$.tmp
#          cat /tmp/hosts.mac.$$.tmp > /pxe/etc/hosts.mac
#          rm /tmp/hosts.mac.$$.tmp
#          echo "DELETE FROM \`hosts\` WHERE \`mac\` = '$mac' LIMIT 1;" | mysql -u root -pprout pxe 
#          echo "INSERT INTO \`hosts\` VALUES ('$mac', '$name');" | mysql -u root -pprout pxe
        else
          echo $mac $name >> /pxe/etc/hosts.mac
	  sort --key=2 /pxe/etc/hosts.mac > /pxe/etc/hosts.mac.new || exit
	  cat /pxe/etc/hosts.mac.new > /pxe/etc/hosts.mac
	  rm /pxe/etc/hosts.mac.new
#          echo "INSERT INTO \`hosts\` VALUES ('$mac', '$name');" | mysql -u root -pprout pxe
        fi
      fi
   done
   sed -r -n -e 's/([0-9a-f\-]+).*/\1/p' /pxe/etc/hosts.mac
fi
