#!/bin/bash

if [ `whoami` != 'root' ]
  then
    echo "error: you cannot perform this operation unless you are root."
    exit
fi

rm /usr/bin/oldreality

rm /usr/share/applications/oldreality.desktop
rm /usr/share/pixmaps/oldreality.png

rm -r /usr/share/oldreality/

rm /usr/share/man/man6/oldreality.6.gz

