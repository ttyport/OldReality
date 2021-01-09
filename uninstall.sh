#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "error: you cannot perform this operation unless you are root."
  exit
fi

rm /usr/bin/oldreality

rm -r /usr/share/oldreality/

