#!/bin/sh
. /pxe/etc/config

ACTION=/cgi-bin/pxe/power_apply.cgi
MACLINK=/cgi-bin/pxe/choosesav.cgi
WORKDIR=/pxe
PXEUSER=int4

echo Content-type: text/html
echo Pragma: no-cache
echo
echo '<html>'
echo '<body>'

echo '<form action="/pxe/empty.html" target=frame2>'
echo '</form>'
echo '<script>document.forms[0].submit()</script>'

echo "<H3>Allumer / Eteindre les machines</H3>"
echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / power<br><br>"
echo
echo "Cocher les machines &agrave; allumer.<br>"
echo "D&eacute;cocher les machines &agrave; &eacute;teindre.<br>"
echo "Cliquer sur appliquer.<br><br>"

echo "<form action=\"$ACTION\" method=\"POST\">"

maclist=`/pxe/bin/maclist.sh 1`
echo "<input type=hidden name=maclist value=\"$maclist\">"

echo '<table>'

for mac in $maclist ; do
   if grep -q $mac $WORKDIR/etc/hosts.mac ; then
     name=`grep $mac $WORKDIR/etc/hosts.mac | cut -f 2 -d \ `
     if [ -z "$name" ] ; then
        name=$mac
     fi
   else
     name=$mac
  fi
  checked=
  mac0=`echo $mac | tr - : | tr A-Z a-z`
  ip=`dhcplease $mac0`
  if [ -n "$ip" ] ; then
    online=0
    ssh -o PasswordAuthentication=no $PXEUSER@$ip pwd > /dev/null && online=1
    if [ $online -eq 0 ] ; then
      if ping -c 3 $ip 2> /dev/null ; then
         online=1
      fi
    fi  
    if [ $online -eq 1 ] ; then
      checked=" checked=on"
    fi
  fi

  echo '<tr>'
  echo '<td>'
#  echo "<INPUT TYPE=checkbox NAME=\"$mac\"$checked><a href=\"$MACLINK?$name\">$name</a>"
  echo "<INPUT TYPE=checkbox NAME=\"$mac\"$checked>$name"
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
