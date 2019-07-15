#!/bin/sh

. /pxe/etc/config

echo Content-Type: text/html
echo

if [ -n "$QUERY_STRING" ] ; then

        for param in `echo $QUERY_STRING | urldecode | sed -r -e 's/\\\&/ /g' -e 's/&/ /g'` ; do
                [ -z "$param" ] && continue
                varname=`echo $param | cut -f 1 -d =`
                value=`echo $param | cut -f 2 -d =`
                case "$varname" in
                        pc) PC=$value ;;
                esac
        done
fi

cat << EOF
<form name="movieopen" method="get" action="/cgi-bin/pxe/movieopen.cgi">
	<table align="center">
		<tr>
			<td>
				url pour pc$PC: 
			</td>
			<td>
				<input type="text" name="url" style="width: 320px;">
				<input type="hidden" name="pc" value="$PC">
			</td>
		</tr>
	</table>
</form>
EOF
