#!/bin/sh
# launcher.sh
# this will nagivate to the home directyory, then to this directory, execute
# the script 'boot.py' and then go back to home.

cd /
cd home/kaeden/Documents/Code/SMART-MIRROR
sudo /home/kaeden/Documents/Code/SMART-MIRROR/.venv/bin/python3  /home/kaeden/Documents/Code/SMART-MIRROR/boot.py >> /home/kaeden/Documents/Code/SMART-MIRROR/smart_mirror.log 2>&1
cd /
