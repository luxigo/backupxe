#!/bin/sh
. /pxe/etc/config

ACTION=/cgi-bin/pxe/pxeconfig_apply.cgi
MACLINK=/cgi-bin/pxe/choosesav.cgi
WORKDIR=/pxe
PXEUSER=Administrateur

echo Content-type: text/html
echo Pragma: no-cache
echo
echo '<html>'
echo '<body>'

echo '<form action="/pxe/backuplan2.html" target=frame2>'
echo '</form>'
echo '<script>document.forms[0].submit()</script>'

echo "<H3>PXE Configuration</H3>"
echo " / <a href=\"/pxe/home.html\" target=frame0>home</a> / pxe<br><br>"

echo "S&eacute;lectionnez le fichier de d&eacute;marrage r&eacute;seau"
echo '<br><br>'
echo "<form action=\"$ACTION\" method=\"POST\" target=frame2>"

echo '<table>'
echo '<tr>'
echo '<td>'
echo "<input type=checkbox name=default>Par D&eacute;faut"
echo '</td>'
echo '<td>'

echo '<select name=cfg.default>'

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
echo '</td></tr>'
echo '<tr><td><br></td></tr>'


maclist=`/pxe/bin/maclist.sh 1`


for mac in $maclist ; do

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
  echo "<input type=checkbox name=\"$mac\">$name"
  echo '</td>'
  echo '<td>'
  echo "<select name=cfg.$mac>"

  cd /tftpboot/pxelinux/pxelinux.cfg
  if [ $? -eq 1 ] ; then
     echo cannot change to directory /tftpboot/pxelinux/pxelinux.cfg
     exit 1
  fi

  list=`ls -1`

  default_one=`ls -l default | sed -r -n -e 's/.* -> (.*)/\1/p'`

  current_one=
  for pxeconfig in $list ; do
     if [ "$pxeconfig" = "01-$mac" ] ; then
       current_one=`ls -l $pxeconfig | sed -r -n -e 's/.* -> (.*)/\1/p'`
       break
     fi
  done

  for pxeconfig in $list ; do

    echo $pxeconfig | egrep -q ^01- && continue 

    selected=
    if [ -n "$current_one" ] ; then
       if [ "$pxeconfig" = "$current_one" ] ; then
          selected=" selected"
       fi
    else
       if [ "$pxeconfig" = "default" ] ; then
          selected=" selected"
       fi
    fi

    echo "<option value=\"$pxeconfig\"$selected>$pxeconfig</option>"

  done
     
  echo '</select>'
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
