#!/bin/sh
. /pxe/etc/config

MOVIES="/pxe/etc/movies"

set -e

echo Content-Type: text/html
echo Pragma: no-cache
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        url) URL=$value ;;
			pc) PC=$value;;
                esac
        done
fi

setrec /pxe/etc/movies $PC $URL  

cat << EOF
<html>
<head>
<script>
top.pcmovie[$PC]="$URL";
top.showpclist();
top.innerHTML_restore("divmapupload");
</script>
</head>
<body>
</body>


EOF

