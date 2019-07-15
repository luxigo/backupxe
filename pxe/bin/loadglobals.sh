#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

. /pxe/etc/config

set -e

ASYNC=0
INIT=

QUERY_STRING="$1"
for param in `echo $QUERY_STRING | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
	[ -z "$param" ] && continue
	varname=`echo $param | cut -f 1 -d = | urldecode`
	value=`echo $param | cut -f 2 -d =  | urldecode`
	case $varname in
		async) ASYNC=$value ;;
		init) INIT=$value ;;
	esac
done

kill -0 `cat /var/run/pxe/loadglobals.pid` > /dev/null 2>&1 && exit 0
echo $$ > /var/run/pxe/loadglobals.pid

IMAGEDIR=/pxe/image
PCSTYLE=/pxe/etc/pcstyle
MACHINES=/pxe/etc/machines
HOSTSMAC=/pxe/etc/hosts.mac
LEASES=`cat /pxe/etc/leases` || true
MOVIES=/pxe/etc/movies
PXECFGDIR=/tftpboot/pxelinux/pxelinux.cfg

touch $HOSTSMAC
touch $MACHINES

while true ; do

[ $MACHINES -nt /pxe/etc/globals.pcname ] && pclist=`sed -r -n -e 's/([^\ ]+).*/\1/p' $MACHINES | tr "\n" ' '`


if [ $MOVIES -nt /pxe/etc/gobals.movies ] || [ $MACHINES -nt /pxe/etc/globals.movies ] ; then
	echo "pcmovie=new Array;" > /dev/shm/globals.movies.$$.tmp
	sed -r -n -e 's/^([0-9]+) +(.*)/pcmovie[\1]="\2";/p' /pxe/etc/movies >> /dev/shm/globals.movies.$$.tmp
	cat /dev/shm/globals.movies.$$.tmp > /pxe/etc/globals.movies
fi

if [ /tftpboot/pxelinux/pxelinux.cfg/movies.d -nt /pxe/etc/globals.soundvol ] ; then
	echo "pcsoundvol=new Array;" > /dev/shm/globals.pcsoundvol.$$.tmp
	for PC in $pclist ; do
		sed -r -n -e 's/.*getmovie.cgi\?([0-9]+) +volume=([0-9]+).*/pcsoundvol[\1]=\2;/p' -e T -e q $PXECFGDIR/movies.d/film$PC >> /dev/shm/globals.pcsoundvol.$$.tmp
	done
	cat /dev/shm/globals.pcsoundvol.$$.tmp > /pxe/etc/globals.pcsoundvol

fi

if [ $MACHINES -nt /pxe/etc/globals.pcname ] || [ $HOSTSMAC -nt /pxe/etc/globals.pcname ] ; then

	echo "pcname=new Array;" > /dev/shm/globals.pcname.$$.tmp
	for pc in $pclist ; do

	  [ -z "$pc" ] && continue

	  mac=`getrec  /pxe/etc/machines $pc 2> /dev/null || true`
	  [ -z "$mac" ] && continue

	  name=`getrec /pxe/etc/hosts.mac $mac 2> /dev/null || true`
	  if [ "$name" = "<unknown>" ] ; then
	  	name=
	  fi

	  echo "pcname[$pc]='$name';pcmac[$pc]='$mac';" >> /dev/shm/globals.pcname.$$.tmp
	done
	cat /dev/shm/globals.pcname.$$.tmp > /pxe/etc/globals.pcname
fi

if [ $HOSTSMAC -nt /pxe/etc/globals.hostsmac ] || [ "$LEASES" -nt /pxe/etc/globals.hostsmac ] || [ $MACHINES -nt /pxe/etc/globals.hostsmac ] ; then
  (
  	echo "hostsmac=new Array;"
	maclist=`sed -r -n -e 's/([^\ ]+).*/\1/p' $HOSTSMAC | tr "\n" ' '`
	for mac in $maclist ; do
	  grep -q "$mac" $MACHINES && continue
	  grep -q "$mac" $PCSTYLE && continue
	  name=`getrec $HOSTSMAC $mac`
	  ip=`dhcplease $mac` || true
	  pxeconfig=`ls -l /tftpboot/pxelinux/pxelinux.cfg/01-$mac 2> /dev/null | sed -r -n -e 's/.* -> (.*)/\1/p'`
	  [ -z "$pxeconfig" ] && pxeconfig="default"
	  echo "hostsmac.push(new Array('$mac','$name','$ip','$pxeconfig' ));"
	done
  ) >> /dev/shm/globals.hostsmac.$$.tmp
  cat /dev/shm/globals.hostsmac.$$.tmp > /pxe/etc/globals.hostsmac
  rm /dev/shm/globals.hostsmac.$$.tmp
fi

if [ /tftpboot/pxelinux/pxelinux.cfg -nt /pxe/etc/globals.all ] || [ /pxe/etc/restorepath -nt /pxe/etc/globals.all ] || [ /pxe/etc/savepath -nt /pxe/etc/globals.all ] || [ $MACHINES -nt /pxe/etc/globals.all ] || [ $HOSTSMAC -nt /pxe/etc/globals.all ] ; then
 (
	echo "pxeconfig=new Array;"
	wd=`pwd`
	cd /tftpboot/pxelinux/pxelinux.cfg
	for cfg in `ls -1` ; do
		if [ -d "$cfg" ] ; then
			for cfgg in `ls -1 $cfg/` ; do
				[ ! -f "$cfg/$cfgg" ] && continue
				echo "pxeconfig.push('$cfg/$cfgg');"
			done
			continue
		fi
		echo $cfg | grep -q ^01- && continue
		echo "pxeconfig.push('$cfg');"
	done
	cd $wd

	echo "pcpxeconfig=new Array;"
	echo "pcpxeconfig[0]='`ls -l "/tftpboot/pxelinux/pxelinux.cfg/default" | sed -r -n -e 's/.* -> (.*)/\1/p'`';"

	for pc in $pclist ; do

	  mac=`getrec $MACHINES $pc`
	  if [ -f /tftpboot/pxelinux/pxelinux.cfg/01-$mac ] ; then
	  	echo "pcpxeconfig[$pc]='`ls -l "/tftpboot/pxelinux/pxelinux.cfg/01-$mac" | sed -r -n -e 's/.* -> (.*)/\1/p'`';"
	  fi

	  imagetorestore=`getrec /pxe/etc/restorepath $mac 2>/dev/null || echo $IMAGEDIR/$mac`
	  if pcsavepath=`getrec /pxe/etc/savepath $mac 2>/dev/null` ; then
	 	 echo "pcsavepath[$pc]='$pcsavepath';"
	  else
	 	 echo "pcsavepath[$pc]=undefined;"
	  fi

	 if echo $imagetorestore | grep -q ^/dev/ ; then
	   echo "pcimagetorestore[$pc]='$imagetorestore';"
	 else
    	   savdate=`cat $imagetorestore/_ok 2> /dev/null` || true
	   mac=`basename $imagetorestore`
           name=`getrec $HOSTSMAC $mac || echo $mac`

	  if [ -n "$savdate" ] ; then
	  	echo "pcimagetorestore[$pc]='$name $savdate';"
	  else
	  	imagetorestore="$IMAGEDIR/ff-ff-ff-ff-ff-ff"
	  	name=`getrec $HOSTSMAC ff-ff-ff-ff-ff-ff`
		savdate=`cat $imagetorestore/_ok 2> /dev/null` || true

	  	if [ -n "$savdate" ] ; then
	  		echo "pcimagetorestore[$pc]='$name $savdate';"
	  	else
	  		echo "pcimagetorestore[$pc]=undefined;"
	  	fi
	  fi
	fi
	done
  ) > /dev/shm/globals.all.$$.tmp
  cat /dev/shm/globals.all.$$.tmp > /pxe/etc/globals.all
  rm /dev/shm/globals.all.$$.tmp
fi


if [ "$LEASES" -nt /pxe/etc/globals ] || [ $MACHINES -nt /pxe/etc/globals ] || [ /pxe/etc/boottime -nt /pxe/etc/globals ] || [ /pxe/etc/uptimelog -nt /pxe/etc/globals ] ; then
(

echo "pcip=new Array;"
for pc in $pclist ; do

  [ -z "$pc" ] && continue

  mac=`getrec  /pxe/etc/machines $pc 2> /dev/null || true`
  [ -z "$mac" ] && continue

  ip=`dhcplease $mac` || true
  echo "pcip[$pc]='$ip';"

#  partitionssaved="`ls -l /pxe/image/$mac/*/*.000 2>/dev/null | sed -r -n -e 's
#  echo -n  "pcpartitionssaved[$pc]='$partitionssaved';"

#  datesaved=`sed -r -n -e 's#$mac ([0-9\:\ \.\-]+) saved (/[^/]+){3}#\1#p'/pxe/log/journal | tail -n 1`
  echo "pcdatesaved[$pc]='$datesaved';"

  echo "pcdaterestored[$pc]='$pcdaterestored';"

  pcdiskspaceleft=`df -h $IMAGEDIR/$mac/ 2>/dev/null | tail -n 1 | sed -r -e 's/ +/ /g' | cut -f 4 -d ' '`
  echo "pcdiskspaceleft[$pc]='$pcdiskspaceleft';"

  boottime=`getrec /pxe/etc/boottime $pc 2>/dev/null || true`
  if [ -n "$boottime" ] ; then
        curtime=`date +%s`
        uptime=`expr $curtime - $boottime`
  else
    uptime=`( lastrec /pxe/etc/uptimelog $pc  2>/dev/null || true ) | cut -f 2 -d ' '`
  fi

  if [ -z "$uptime" ] ; then
    uptime=0
  fi

  echo "pcuptime[$pc]=$uptime;"

#  restorembr=`getrec /pxe/etc/restorembr $mac 2> /dev/null` || true
#  savembr=`getrec /pxe/etc/restorembr $mac 2> /dev/null` || true
done

[ -z "$INIT" ] && echo "setTimeout('showpclist();',1000);"

) >> /dev/shm/globals.$$.tmp && (
  cat /dev/shm/globals.$$.tmp > /pxe/etc/globals
  rm /dev/shm/*.$$.tmp
)

fi

[ $ASYNC -eq 0 ] && break
[ -f /var/run/pxe/loadglobals.pid ] ||  break

sleep 3

done
