#!/bin/sh
. /pxe/etc/config

sav=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 3` 
NAME=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 2` 
what=`echo $1 | sed -r -e 's/\\\&/\t/g' | cut -f 1` 

ACTION=/cgi-bin/pxe/choosedisk_apply.cgi
SAVLINK=/cgi-bin/pxe/choosepart.cgi
WORKDIR=/pxe

echo Content-type: text/html
echo
echo '<html>'
echo '<body>'

if egrep -q \ $NAME\$ $WORKDIR/etc/hosts.mac ; then
  mac=`egrep \ $NAME\$ $WORKDIR/etc/hosts.mac | cut -f 1 -d \ `
else 
  mac=$NAME
fi

case "$what" in
  save)
    echo "<H3>S&eacute;lectionnez les disques &agrave; sauvegarder</H3>"
    echo " $what / $NAME / $sav<br><br>"

    echo
    echo "Clicker sur le nom du disque pour indiquer<br>"
    echo "quelles partitions sauvegarder<br><br>"
    ;;

  restore)
    echo "<H3>S&eacute;lectionnez les disques &agrave; restaurer</H3>"
     
    echo "$what / $NAME / $sav<br><br>"

    echo
    echo "Clicker sur le nom du disque pour indiquer<br>"
    echo "quelles partitions restaurer.<br><br>"
    echo
    ;;

  default)
    echo invalid parameter
    exit 1 ;;
esac

echo "<form action=\"$ACTION\" method=\"POST\">"
echo "<input type=hidden name=mac value=\"$mac\">"
echo "<input type=hidden name=what value=\"$what\">"

echo '<table>'

for disk in `disklist.sh $sav` ; do
  echo '<tr>'
  echo '<td>'
     if [ "$WORKDIR/image/$mac/$sav" = "$current" ] ; then
       checked=" checked=on"
     else
       checked=
     fi
  echo "<INPUT TYPE=checkbox NAME=\"$mac/$sav/$disk\"$checked><a href=\"$SAVLINK?$what&$NAME&$sav&$disk\">$disk</a>"
  echo '</td>'
  echo '</tr>'

done

echo '<tr>'
echo '<td>'
echo '</td>'
echo '</tr>'
echo '</table><br>'

echo '<input type="submit" value="Appliquer" name="submit">'
echo '</form>'

echo '</body>'
echo '</html>'
