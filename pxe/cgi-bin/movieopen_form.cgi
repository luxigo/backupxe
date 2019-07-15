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
<iframe id="movieopeniframe" src="/cgi-bin/pxe/movieopen_frame.cgi?pc=$PC" frameborder="1" scrolling="no" style="width: 100%; height: 48px;"></iframe>
<table style="width: 100%;">
	<tr>
		<td width="50%" align="left">
			<input type="button" class="button" value="Annuler" onclick="innerHTML_restore('divmapupload')" style="width: 50%" />
		</td>
		<td width="50%" align="right">
			<input type="button" onclick="document.getElementById('movieopeniframe').contentDocument.forms[0].submit();" class="button" value="Envoyer" style="width: 50%" />
		</td>
	</tr>
</table>


EOF
