#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "error: you cannot perform this operation unless you are root."
  exit
fi

pip3 install -r requirements.txt

echo "#!/bin/bash
python3 /usr/share/oldreality/app/main.py" > /usr/bin/oldreality

chmod +x /usr/bin/oldreality

mkdir /usr/share/oldreality/
cp -r app/ /usr/share/oldreality/
