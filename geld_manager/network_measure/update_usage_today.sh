#!/bin/sh

mkdir -p "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/$1/"
mkdir -p "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/timestamp/"
while true; do
    pid=$(pidof $NETWORK_MEASURE_PROGRAM)
    cp "/proc/$pid/net/dev" "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/$1/net_today"

    # Warte bis Mitternacht
    current_time=$(date +%s)
    # Berechne Zeitpunkt der nächsten Mitternacht
    seconds_today=$(( current_time % 86400 ))
    target_time=$(( current_time - seconds_today + 86400 ))
    sleep_seconds=$(( target_time - current_time ))
    sleep $sleep_seconds

    current_time=$(date +%s)
    cp "/proc/$pid/net/dev" "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/timestamp/${current_time}_total"
    cp "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/$1/net_today" "/var/lib/goldesel/$NETWORK_MEASURE_PROGRAM/timestamp/${current_time}_today"
done
