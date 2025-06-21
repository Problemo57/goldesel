#!/bin/sh

sleep 5

random_id=$(head -c 16 /dev/random | od -An -tx1 | tr -d ' \n')

/var/lib/goldesel/update_usage_today.sh $random_id &
/var/lib/goldesel/update_usage_total.sh $random_id &

echo "Start Measure"
