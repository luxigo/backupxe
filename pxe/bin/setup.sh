#!/bin/sh
# this script is run from rc.S 
. /pxe/etc/config
. /etc/config
	
export IMAGE_DIR=`cat /pxe/etc/IMAGE_DIR`
export PATH=/pxe/bin/`uname -m`:/pxe/bin:/usr/local/sbin:/usr/local/bin:/sbin:/usr/sbin:/bin:/usr/bin

#busy $$ "$0" "$@"

mkdir -p /pxe/log/$HWADDR || exit 1 # problem $$ "$0" $$
LOGFILE=/pxe/log/$HWADDR/partimage-save.log

rm /pxe/log/$HWADDR/done 2> /dev/null || true
rm /pxe/log/$HWADDR/bye 2> /dev/null || true
rm /pxe/log/$HWADDR/ready 2> /dev/null || true
rm /pxe/log/$HWADDR/problem 2> /dev/null || true

touch $LOGFILE || exit 1
 
name=`getrec /pxe/etc/hosts.mac $HWADDR`
if [ -z "$name" ] ; then
	addrec /pxe/etc/hosts.mac $HWADDR $HWADDR
fi
partimage-save -R $REMOTESERVER "$IMAGE_DIR" 2>> $LOGFILE
err=$? 

if [ $err -ne 0 ] ; then
   problem $$ $err
   exit 1
fi

lspci > /pxe/log/$HWADDR/lspci
cat /proc/cpuinfo > /pxe/log/$HWADDR/cpuinfo
cat /proc/meminfo > /pxe/log/$HWADDR/meminfo
cat /proc/bus/usb/devices > /pxe/log/$HWADDR/devices
cardctl info > /pxe/log/$HWADDR/pcmcia
dmesg > /pxe/log/$HWADDR/dmesg

if [ $? -ne 0 ] ; then
   problem $$ $err
   exit 1
else
  /usr/bin/done $$ done
  grep -q reboot /proc/cmdline && reboot
  echo Done !
fi
