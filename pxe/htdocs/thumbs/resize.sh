#!/bin/sh
if [ -z "$1" ] ; then
  echo 'usage: resize.sh <size> (eg: 16x16)'
fi
for f in pc*.png ; do convert -resize $1  $f `basename $f .png`_$1.png ; done
