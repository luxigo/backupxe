#!/bin/sh
. /pxe/etc/config

echo Content-type: text/html
echo 

echo '<html><body>'
#echo "$0 $@"

if [ -n "$QUERY_STRING" ] ; then

	count=0
        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do

                [ -z "$param" ] && continue

		if [ $count -eq 0 ] ; then
			action=$param
			count=1
			continue
		fi

                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        machine)
				machine=$value
				echo "bootandrun $machine $action $cmdline<br>"
				bootandrun $machine $action $cmdline 
				sleep 3
				cmdline=""
				;;
			*)
				cmdline=$cmdline+" $varname=$value"
				;;
                esac
        done
fi

echo '</body></html>'

