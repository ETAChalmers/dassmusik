#!/bin/bash

for ((i=85; i>=0; i--))
do
    sleep 0.02
    amixer -q set 'PCM' ${i}% > /dev/null
done
