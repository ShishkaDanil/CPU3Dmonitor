#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip
pip3 install pyqt5 matplotlib psutil

sudo cp CPU3Dmonitor.py /usr/local/bin/CPU3Dmonitor.py
sudo chmod +x /usr/local/bin/CPU3Dmonitor.py

cat <<EOF > ~/.config/autostart/CPU3Dmonitor.desktop
[Desktop Entry]
Type=Application
Exec=python3 /usr/local/bin/CPU3Dmonitor.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=CPU3Dmonitor
Name=CPU3Dmonitor
Comment=System monitor in 3D
Icon=CPU3Dmonitor.icon
EOF

echo "Installation complete. The application will start automatically on the next login."
