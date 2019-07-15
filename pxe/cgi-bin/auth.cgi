#!/bin/sh

EMOTE_ADDR=$REMOTE_ADDR
export REMOTE_ADDR=
. /pxe/etc/config
export REMOTE_ADDR=$EMOTE_ADDR

set -e
echo Content-type: text/html
echo Pragma: no-cache
echo

for param in `sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
	[ -z "$param" ] && continue
        varname=`echo $param | cut -f 1 -d = | urldecode`
        value=`echo $param | cut -f 2 -d =  | urldecode`
        case "$varname" in 
                user) user="$value" ;;
                pass) pass="$value" ;;
        esac
done

page=`getrec /etc/auth.passwd $user:$pass 2> /dev/null` || true
if [ -n "$page" ] ; then
	setrec /pxe/etc/allow $REMOTE_ADDR 1
        setrec /pxe/etc/logintime $REMOTE_ADDR `date +%s` 2> /dev/null 
        setrec /pxe/etc/lasthit $REMOTE_ADDR `date +%s` 2> /dev/null 
# iptables -A FORWARD -s $REMOTE_ADDR -d ! 192.168.0.0/16 -j ACCEPT
	cat << EOF
<html>
<head>
	<meta http-equiv="refresh" content="0; URL=$page">
</head>
</body>
<body>
</html>
EOF

else
	setrec /pxe/etc/allow $REMOTE_ADDR 0
	cat /pxe/htdocs/denied.html
fi
