#!/bin/bash
# this cgi is used to receive stats from the patched partimage binary running on the client machine
# AND to send those stats when backupxe.html ask for them (what=show)

. /pxe/etc/config

set -e

echo Content-Type: text/plain
echo

ADDR=$REMOTE_ADDR

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                
                [ -z "$param" ] && continue
                
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                
                case "$varname" in
                
                        what) what=$value ;;
                        who) 
                        	ADDR=`dhcplease $value`
                        	[ -z "$ADDR" ] && exit 1
                        	;;
                        	
#                        elapsed) elapsed=$value ;;
#                        remaining) remaining=$value ;;
#                        bytespermin) bytespermin=$value ;;
#                        bytescopied) bytescopied=$value ;;
#                        bytestotal) bytestotal=$value ;;
#                        percent) percent=$value ;;
                esac
        done
fi

LOGFILE=/pxe/log/partimage-showstats.$ADDR

# when the cgi is run from the patched partimage (what=save or restore):
# as long the log file exists, say 'continue' to partimage-showstats.sh
# which is run each 2nd second from the patched partimage
# when /tmp/showstats exists on the host running it.

if [  -f "$LOGFILE" ] ; then

	case "$what" in
		show)
			#  the cgi is run from backupxe.html with ?what=show&who=<mac address>
			tail -n 1 $LOGFILE
			exit 0
			;;
		stop)
			#  the cgi is run from backupxe.html with ?what=stop&who=<mac address>
			rm "$LOGFILE"
			exit 0
			;;
		
	esac
	
	echo `date +%Y%m%d-%T` $REMOTE_ADDR $QUERY_STRING >> $LOGFILE 
	echo continue
fi
