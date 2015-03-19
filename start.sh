#!/bin/bash
sleep 0.7
for ((i=50; i<=85; i++))
do
#    sleep 0.01
    amixer -q set 'PCM' ${i}%
done
