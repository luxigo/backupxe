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
<form name="pciconupload" method="post" action="/cgi-bin/pxe/pciconupload.cgi" enctype="multipart/form-data">
	<table align="center">
		<tr>
			<td>
				Remplacer  
			</td>
			<td valign="center">
				<img src="/pxe/thumbs/pc${PC}_24x24.png">
			</td>
			<td>
				par:
			</td>
			<td>
				<input type="file" class="file" name="$PC" value="...">
			</td>
		</tr>
	</table>
</form>
EOF
