#!/bin/sh
FILM=$1
if [ -z "$FILM" ] ; then 
	FILM=1
	MAX=24
else
	MAX=$FILM
fi

VGA=789
SPACE=" "

while [ $FILM -le 24 ] ; do

if [ $FILM -gt 9 ] ; then
	SPACE=
fi

(

cat << EOF
prompt 0
noescape 1
menu master passwd stpxe
default menu.c32
ontimeout boot/geexbox/vmlinuz initrd=boot/geexbox/initrd$FILM.gz root=/dev/ram0 load_ramdisk=1 prompt_ramdisk=0 rw init=linuxrc boot=nfs lang=fr remote=atiusb receiver=atiusb keymap=qwertz splash=silent vga=$VGA video=vesafb:ywrap,mtrr nfsroot=nfsrootserver:/nfs/geexbox/i386/GEEXBOX loopURL=http://movieserver/cgi-bin/pxe/getmovie.cgi?$FILM volume=90

timeout 50 
                
menu title Film$FILM
                                                
label film$FILM                                     
  menu label ^film$FILM$SPACE   - Voir le Film $SPACE$FILM en boucle
  menu default                                                                                                               
  kernel boot/geexbox/vmlinuz                                                                                                
  append initrd=boot/geexbox/initrd$FILM.gz root=/dev/ram0 load_ramdisk=1 prompt_ramdisk=0 rw init=linuxrc boot=nfs lang=fr remote=atiusb receiver=atiusb keymap=qwertz splash=silent vga=$VGA video=vesafb:ywrap,mtrr nfsroot=nfsrootserver:/nfs/geexbox/i386/GEEXBOX loopURL=http://movieserver/cgi-bin/pxe/getmovie.cgi?$FILM volume=90

                                            
label exit                                  
  menu label ^exit    - Retour au menu Films
  kernel menu.c32           
  append pxelinux.cfg/movies

EOF

 ) > film$FILM

FILM=`expr $FILM + 1`

done
