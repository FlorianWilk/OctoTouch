#!/bin/sh

export DISPLAY=:0
while true 
do
    git pull
    python3 octotouch.py
    ret=$?
    if [ $ret -ne 3 ]; then 
        exit 0
    fi
done
