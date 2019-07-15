#!/bin/sh
# rc.S:  Basic system initialization.
export BACKUPXE=1
clear
# uncomment for debugging:
#set -x

[ -x /etc/rc.d/usplash ] && /etc/rc.d/usplash

myexit() {
	[ -x /etc/rc.d/usplash ] && touch /tmp/killsplash
	exit $1
}

kernelcmdline () {
# If possible, figure out what kernel we just booted with:

. /etc/profile
  unset SLACK_KERNEL
  unset NFS_ROOT
  unset USR_LOCAL
  unset NIC
  unset EXEC
  unset TORAM
  unset REBOOT
  for ARG in `cat /proc/cmdline` ; do
    name=`echo $ARG | tr a-z A-Z | cut -f 1 -d =`   
    value=`echo $ARG | cut -f 2 -d =`   
    case "$name" in 
	SLACK_KERNEL) SLACK_KERNEL=$value ;;
    	NFS_ROOT) NFS_ROOT=$value ;;
    	USR_LOCAL) USR_LOCAL=$value ;;
    	NIC) NIC=$value ;;
    	EXEC) EXEC=$value ;;
    	TORAM) TORAM=$value ;;
    	REBOOT) REBOOT=$value ;;
    esac
  done
  export SLACK_KERNEL
  export NFS_ROOT
  export USR_LOCAL
  export NIC
  export EXEC
  export TORAM
  export REBOOT
}

network () {

  if [ -x /etc/rc.d/rc.inet1 ]; then
    /bin/sh /etc/rc.d/rc.inet1
  fi

  if [ -z "$IF" ] ; then
    export IF=eth0
  fi

  if ! ifconfig $IF 2> /dev/null 1>&2 ; then
    if [ -n "$NIC" ] ; then
      echo "--- loading network card module $NIC"
      /sbin/modprobe "$NIC" && echo $NIC > /cardfound
    fi
    if [ ! -f /cardfound ] ; then 
      echo "--- trying to autodetect network card"
      ( /bin/network.sh AUTO > /var/log/network.log ) 2> /dev/null
      if [ ! -f /cardfound ] ; then
        echo "--- please identify your network card manually and"
        echo "--- set NIC=<module_name> in dhcpd.conf or kernel boot options"
        echo
        cat /proc/pci | grep -i network
        cat /proc/pci | grep -i ethernet
        echo
      else
        echo "--- module `cat /cardfound` loaded"
        rm /var/log/network.log
      fi
    fi
  else
    touch /cardfound
  fi
  
  
  if [ -f /cardfound ]  ; then

    echo "--- configuring network interface using dhcp"
    while [ 0 ] ; do
      if [ -n "$NFS_ROOT" ] ; then
        /sbin/dhcpcd -n -p $IF  && break
      else
        /sbin/dhcpcd -n $IF  && break
      fi
      sleep 1
    done

    ifconfig $IF
    sleep 1

    . /etc/dhcpc/dhcpcd-$IF.info
    export REMOTESERVER=`echo $ROOTPATH | cut -f 1 -d :`
    export HWADDR=`echo $CLIENTID | tr : - | tr A-Z a-z`

    echo IF=$IF > /etc/config
    echo . /etc/dhcpc/dhcpcd-$IF.info >> /etc/config
    echo export REMOTESERVER=$REMOTESERVER >> /etc/config
    echo export HWADDR=`echo $CLIENTID | tr : - | tr A-Z a-z` >> /etc/config

  fi

}

modules () {

  echo "--- updating library dependencies"
  if [ -x /sbin/ldconfig ]; then
    /sbin/ldconfig
  fi

  echo "--- loading modules"

  /sbin/modprobe apm > /dev/null
  grep SCSI.*BusLogic /proc/pci && modprobe BusLogic

  cd /lib/modules/`uname -r`/kernel/drivers
  for m in md/*.o.gz ide/*.o.gz scsi/*.o.gz ; do modprobe `basename $m .o.gz` 2>> /var/log/modprobe.log ; done
  for m in md/*.o ide/*.o scsi/*.o ; do modprobe `basename $m .o` 2>> /var/log/modprobe.log ; done

}

nfsroot () {

  echo "--- starting portmap"
  /sbin/rpc.portmap   # for lockd (implicitly started by mount)
  sleep 5

# default ip is $REMOTESERVER 
  NFS_ROOT=`echo $NFS_ROOT | sed -r -e 's/^([^:]+)$/'$REMOTESERVER':\1/'`
  
  echo "--- mounting $NFS_ROOT on /mnt"
  /sbin/mount -n -o nolock,ro,rsize=8192,wsize=8192,async $NFS_ROOT /mnt || myexit 1
  
  echo "--- stopping portmap"
  killall rpc.portmap   # portmap keeps old root busy
  sleep 5
  echo "--- unmounting /proc"
  umount /proc
  cd /mnt

  echo "--- doing the pivot_root"
  /sbin/pivot_root . old_root
  exec chroot . /bin/sh <dev/console >dev/console 2>&1
  myexit 0
}

# remove /etc/mtab* so mount creates the /etc/mtab file
/bin/rm -f /etc/mtab* /etc/nologin

# Mounts /proc:
echo "--- mounting /proc"
/bin/mount proc /proc -t proc

echo "--- setting environment variables from kernel command line"
kernelcmdline

echo "--- updating modules dependencies"
/sbin/depmod -a -F /boot/System.map 2> /var/log/depmod.log

network

if [ -n "$NFS_ROOT" ] ; then
  nfsroot
fi

if ! grep -q nossh /proc/cmdline ; then
  if [ -x /etc/rc.d/rc.sshd ]; then
    /bin/sh /etc/rc.d/rc.sshd start
  fi
fi

/bin/mount -av -t nonfs

modules

echo "--- turning on swap"
/sbin/swapon -a 2> /dev/null

if [ -n "$TORAM" ] ; then

  echo "--- copying /etc /home /root /tmp /usr and /var in ramdisk"

  mkdir -p /ram
  mount -t tmpfs tmpfs /ram

  mkdir -p /home

  for dir in etc home root tmp usr var ; do
    cp -a /$dir /ram
    rm -r /$dir
    ln -s /ram/$dir /$dir
  done

fi

# Here's the situation.  Because of the practice of keeping the local
# time (rather than UTC) in the system's clock, at any given time half
# of the people doing an install will be creating files that upon
# reboot will appear to have been created in the future.
#
# There are a lot of things that aren't happy when that happens.  The
# one that screams the most loudly is e2fsck, and we don't want to
# anger that!  Sometimes it even proceeds to check the partitions just
# to be sure the user is fully punished.
#
# But, there's a simple solution.  If we set the (temporary) Linux clock
# to yesterday (-24h), then there's no way that could occur.  Everything
# on the system will be in the past (but not too far in the past).
# Since files will quickly be put into use and given the correct after
# reboot, this really shouldn't have a negative impact.  Plus, it affects
# only newly created files during installation -- any file shipped in a
# package will have an accurate time of creation.  (for its timezone ;-)
#
# Update:  We have to use 2 days ago, or chroot()+timezone offset might
# still be in the future...  <sigh>
#
touch /.today
/bin/sh /sbin/fakedate

## Detect serial console from kernel command line:
#if cat /proc/cmdline | grep console=ttyS 1> /dev/null 2> /dev/null ; then
#  SERIAL_CONSOLE="true"
#fi

# Try to mount sysfs:
#if cat /proc/filesystems | grep -w sysfs 1> /dev/null 2> /dev/null ; then
#  mount -t sysfs sysfs /sys 2> /dev/null
#fi

# System logger (mostly to eat annoying messages):
echo "--- starting syslogd"
/sbin/syslogd 2> /dev/null
sleep 1
echo "--- starting klogd"
/sbin/klogd -c 3 1> /dev/null

# Look for USB keyboard or storage:
echo "--- looking for usb devices"
/etc/rc.d/rc.usb start
#sleep 3

# Look for IEEE1394 devices:
echo "--- looking for firewire devices"
if cat /proc/pci | grep 1394 1> /dev/null 2> /dev/null ; then
  /etc/rc.d/rc.ieee1394 start
  sleep 3
fi

### PROBABLY USELESS WITHOUT SOME TIMED DELAY ABOVE
## Start USB again (in case we missed a USB keyboard)
#/etc/rc.d/rc.usb start

# Replace some startup binaries with better versions:
#( cd /bin
#  rm -f grep gzip tar gunzip zcat df
#  ln -sf df.bin df
#  ln -sf grep.bin grep
#  ln -sf gzip.bin gzip
#  ln -sf tar-1.13 tar
#  ln -sf gzip gunzip
#  ln -sf gzip zcat
#)

# Make detected partitions:
/dev/makedevs.sh

# Create LVM nodes:
/dev/devmap_mknod.sh

# Scan for existing LVM partitions:
# We will run 'vgscan -ay' in the setup to prevent a 10 second sleep;
vgscan --mknodes 2> /tmp/foo
cat /tmp/foo | uniq
rm -f /tmp/foo

unset SCAN
# Now we should rescan the "SCSI" bus to look for new USB or firewire devices
# that look like SCSI devices:
if [ -r /proc/bus/usb/devices ]; then
  if cat /proc/bus/usb/devices | grep -w usb-storage 1> /dev/null 2> /dev/null ; then
    SCAN="true"
  fi
fi
if [ -r /proc/bus/ieee1394/devices ]; then
  if cat /proc/bus/ieee1394/devices | grep -w SBP2 1> /dev/null 2> /dev/null ; then
    SCAN="true"
  fi
fi
if [ "$SCAN" = "true" ]; then
  if ! cat /proc/cmdline | grep -q noscanluns 2> /dev/null ; then
    echo "Detected new USB/IEEE1394 storage devices...  scanning all LUNs."
    echo "(to skip, give a 'noscanluns' kernel option at boot)"  
    sleep 5
    sh /etc/rc.d/rescan-scsi-bus -l
    sleep 1
  fi
fi
unset SCAN

# Check /proc/partitions again:
/dev/makedevs.sh

# Don't automatically blank the screen, or it will go black during the install
# process when stray keystrokes might be dangerous:
/bin/setterm -blank 0

clear

echo > /etc/motd


if [ -z "$EXEC" ] ; then
  echo
  echo
  echo "<OPTION TO LOAD SUPPORT FOR NON-US KEYBOARD>"
  echo
  echo "If you are not using a US keyboard, you may now load a different"
  echo "keyboard map.  To select a different keyboard map, please enter 1"
  echo "now.  To continue using the US map, just hit enter."
  echo
  echo -n "Enter 1 to select a keyboard map: "
  read ONE
  if [ "$ONE" = "1" ]; then
    /usr/lib/setup/SeTkeymap
  fi

  echo "If you're upgrading an existing Slackware system, you might want to" >> /etc/motd
  echo "remove old packages before you run 'setup' to install the new ones. If" >> /etc/motd
  echo "you don't, your system will still work but there might be some old files" >> /etc/motd
  echo "left laying around on your drive." >> /etc/motd
  echo >> /etc/motd
  echo "Just mount your Linux partitions under /mnt and type 'pkgtool'. If you" >> /etc/motd
  echo "don't know how to mount your partitions, type 'pkgtool' and it will tell" >> /etc/motd
  echo "you how it's done." >> /etc/motd
  echo >> /etc/motd
  echo "To partition your hard drive(s), use 'cfdisk' or 'fdisk'." >> /etc/motd
  echo "To activate PCMCIA/Cardbus devices needed for installation, type 'pcmcia'." >> /etc/motd
  echo "To activate network devices needed for installation, type 'network'." >> /etc/motd
  echo "To start the main installation, type 'setup'." >> /etc/motd
  echo >> /etc/motd
fi

echo "`/bin/uname -a | /bin/cut -d\  -f1,3`." >> /etc/motd
echo >> /etc/motd

if [ -f /cardfound ] ; then

  if [ -n "$USR_LOCAL" ]; then

    if [ "$USR_LOCAL" = "cdrom" ] ; then
	echo USR_LOCAL=cdrom: not implemented
    	myexit
    else
	    echo "--- starting portmap"
	    /sbin/rpc.portmap
	    sleep 5

	    echo "--- mounting $USR_LOCAL on /usr/local"
	    USR_LOCAL=`echo $USR_LOCAL | sed -r -e 's/^([^:]+)$/'$REMOTESERVER':\1/'`
	    mkdir -p /usr/local
	    /sbin/mount -o nolock,rsize=8192,wsize=8192,async $USR_LOCAL /usr/local || myexit 1
	    echo "--- done"
	    sleep 1
    fi

    if [ -x /usr/local/linuxrc ] ; then
        cd /usr/local
        echo "--- running /usr/local/linuxrc"
        . linuxrc
        echo
    fi

  fi

  if [ -s /pxe/etc/authorized_keys ] ; then
    cat /pxe/etc/authorized_keys >> /root/.ssh/authorized_keys
  fi

  if [ -x /pxe/etc/$HWADDR/rc.d/rc.S ] ; then
    . /pxe/etc/$HWADDR/rc.d/rc.S
  fi

  if [ -n "$EXEC" ] ; then

    echo $EXEC | egrep -q '^[a-z]+://' 
    if [ $? -eq 0 ] ; then

      echo "--- getting $EXEC"
      mkdir -p /root/EXEC

      echo $EXEC | egrep -q '^https?://' 
      if [ $? -eq 0 ] ; then
        cd /root/EXEC || myexit 1
        wget $EXEC || myexit 1
  
      else 

        echo $EXEC | egrep -q '^ssh://' 
        if [ $? -eq 0 ] ; then
          cd /root/EXEC || myexit 1
          scp $EXEC . || myexit 1
        fi

      fi

    else

      cd `dirname $EXEC`

    fi

    echo "--- running `pwd`/`basename $EXEC`"
    if ./`basename $EXEC` ; then
       [ -n "$REBOOT" ] && /sbin/reboot
    fi
  fi

else 


  if [ -n "$EXEC" ] ; then

    echo $EXEC | egrep -q -e '^[^ :]+://' 
    if [ $? -eq 0 ] ; then

      echo "*** network interface down, cant get $EXEC"
      myexit 1

    else 

      echo "--- running $EXEC"
      if $EXEC ; then
         [ -n "$REBOOT" ] && /sbin/reboot
      fi

    fi 
  fi

  echo "*** network interface is down"

fi

cat /etc/issue

myexit 0
