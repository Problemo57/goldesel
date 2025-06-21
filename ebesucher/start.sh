#!/bin/sh
set -e

sh /prepare_firefox.sh

socat TCP-LISTEN:7543,fork TCP:127.0.0.1:6080 &
python3 ebesucher.py
