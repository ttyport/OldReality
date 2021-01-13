#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "error: you cannot perform this operation unless you are root."
  exit
fi

pip3 install -r requirements.txt

echo "#!/bin/bash
python3 /usr/share/oldreality/app/main.py" > /usr/bin/oldreality

echo "[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Description=Collection of old retro games
Categories=Game;
Name=oldreality
Exec=oldreality
Icon=oldreality
Terminal=false
" > /usr/share/applications/oldreality.desktop

cp oldreality.png /usr/share/pixmaps/oldreality.png

chmod +x /usr/bin/oldreality

mkdir /usr/share/oldreality/
cp -r app/ /usr/share/oldreality/
