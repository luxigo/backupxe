#!/bin/sh
. /pxe/etc/config

ACTION=/cgi-bin/pxe/pxeconfig_default_apply.cgi

echo Content-type: text/html
echo Pragma: no-cache
echo
echo '<html>'
echo '<body>'

echo "<H3>PXE Configuration</H3>"
echo
echo "S&eacute;lectionnez le fichier de d&eacute;marrage r&eacute;seau par d&eacute;faut"
echo '<br><br>' 
echo "<form action=\"$ACTION\" method=\"POST\">"

echo '<table>'
echo '<tr>'
echo '<td>'

echo '<select name=default>'

cd /tftpboot/pxelinux/pxelinux.cfg
if [ $? -eq 1 ] ; then
   echo cannot change to directory /tftpboot/pxelinux/pxelinux.cfg
   exit 1
fi

list=`ls -1`
default_one=`ls -l default | sed -r -n -e 's/.* -> (.*)/\1/p'`

for pxeconfig in $list ; do

  [ "$pxeconfig" = "default" ] && continue
  echo $pxeconfig | egrep -q ^01- && continue

  selected=
  if [ "$pxeconfig" = "$default_one" ] ; then
      selected=" selected"
  fi

  echo "<option value=\"$pxeconfig\"$selected>$pxeconfig</option>"

done
     
echo '</select>'
echo '</td>'
echo '</tr>'

echo '</table><br>'

echo "<input type=\"submit\" value=\"Appliquer\" name=\"submit\">"
echo '</form>'

echo '</body>'
echo '</html>'
