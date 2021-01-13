#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "error: you cannot perform this operation unless you are root."
  exit
fi

rm /usr/bin/oldreality

rm /usr/share/applications/oldreality.desktop
rm /usr/share/pixmaps/oldreality.png

rm -r /usr/share/oldreality/

