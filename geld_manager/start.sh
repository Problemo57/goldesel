#!/bin/sh
chmod +x -R /network_measure
cp /network_measure/* /var/lib/goldesel

python3 app.py
