#!/bin/sh

# Make sure Thonny is closed or this won't work.

# You might have to run:
#     mpremote connect list
# and then something like
#     mpremote connect /dev/cu.usbmodem101
# to connect the device before running this script.

cd micropython

mpremote fs ls firmware > /dev/null || mpremote fs mkdir firmware

for file in firmware/*; do 
    if [ -f "$file" ]; then 
        if [[ $file != */__init__.py ]]; then
            mpremote fs cp $file :/$file
        fi
    fi 
done

mpremote fs ls lib > /dev/null || mpremote fs mkdir lib

for file in lib/*; do 
    if [ -f "$file" ]; then 
        if [[ $file != */__init__.py ]]; then
            mpremote fs cp $file :/$file
        fi
    fi 
done