#!/bin/sh
. /pxe/etc/config

ACTION=/cgi-bin/pxe/register_apply.cgi
WORKDIR=/pxe

echo Content-type: text/html
echo
echo '<html>'
echo '<body>'

echo '<form action="/pxe/empty.html" target=frame2>'
echo '</form>'
echo '<script>document.forms[0].submit()</script>'

echo "<H3>R&eacute;f&eacute;rencer les machines</H3>"
echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / register<br><br>"
echo "Cochez les machines &agrave; r&eacute;f&eacute;rencer puis cliquez sur \"Appliquer\"<br><br>"

#echo "Si la machine ne s'allume pas apr&egrave;s avoir cliqu&eacute;<br>"
#echo "sur \"Appliquer\", essayez de la rallumer une fois manuellement<br>"
#echo "puis de l'&eacute;teindre normalement (menu d&eacute;marrer).<br><br>"
#echo "Si la machine ne d&eacute;marre pas sur le r&eacute;seau,<br>"
#echo "v&eacute;rifiez que le d&eacute;marrage r&eacute;seau<br>"
#echo "est activ&eacute; dans le BIOS de la machine cible<br><br>"

echo "<form action=\"$ACTION\" method=\"POST\">"
echo "<input type=hidden name=what value=$what>"
echo '<table>'

referenced=`/pxe/bin/maclist.sh`
for mac in `/pxe/bin/maclist.sh 1` ; do

   for mac2 in $referenced ; do
      [ "$mac" = "$mac2" ] && break
   done
   [ "$mac" = "$mac2" ] && continue

   if grep -q $mac $WORKDIR/etc/hosts.mac ; then
     name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
     if [ -z "$name" ] ; then
        name=$mac
     fi
   else
     name=$mac
  fi

  echo '<tr>'
  echo '<td>'
  echo "<INPUT TYPE=checkbox NAME=\"$mac\">$name"
  echo '</td>'
  echo '</tr>'

done

echo '<tr>'
echo '<td>'
echo '</td>'
echo '</tr>'
echo '</table><br>'

echo "<input type=\"submit\" value=\"Appliquer\" name=\"submit\">"
echo '</form>'

echo '</body>'
echo '</html>'
