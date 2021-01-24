#!/bin/bash

if [ `whoami` != 'root' ]
  then
    echo "error: you cannot perform this operation unless you are root."
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
Name=OldReality
Exec=oldreality
Icon=oldreality
Terminal=false
" > /usr/share/applications/oldreality.desktop

cp oldreality.png /usr/share/pixmaps/oldreality.png

chmod +x /usr/bin/oldreality

mkdir /usr/share/oldreality/
cp -r app/ /usr/share/oldreality/

echo ".TH OldReality 6
.SH TITLE
OldReality - collection of retro arcade games
.SH DESCRIPTION
.B oldreality
is a game launcher which i wrote for people who want to nostalgic for retro games
.SH FILES
.I \$HOME/.config/oldreality/config.txt
.RS
Local system configuration file.
.RE
.SH AUTHOR
yayguy.4618@yandex.com https://github.com/yayguy4618/" > oldreality.6
gzip oldreality.6
cp oldreality.6.gz /usr/share/man/man6/
rm oldreality.6.gz
