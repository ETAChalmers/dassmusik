#!/bin/bash
DASSMUSIK_FOLDER=/home/eta/dassmusik
screen -ls | grep -q dassmusik
if [ $? -eq 1 ]
then
	echo "Starting dassmusik screen."
    cd $DASSMUSIK_FOLDER
	screen -d -m -S dassmusik ./run_dassmusik.sh
else
	echo "Dassmusik screen is already running."
fi
