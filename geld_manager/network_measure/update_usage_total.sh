#!/bin/sh

mkdir -p "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/$1/"
while true; do
    pid=$(pidof $NETWORK_MEASURE_PROGRAM)
    cp "/proc/$pid/net/dev" "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/$1/net_total"
    sleep 60
done
