# Dassmusik
This is the wonderful set of scripts that gives the bathroom at ETA its lovely soundtrack.


## Depedencies
* python 2.x
* screen
* mplayer
* alsamixer + utils

## Setup
Follow the steps below! 

### 1. Get the Dassmusik repo 
Clone the Dassmusik repo to a folder of your choice:

    git clone https://github.com/ETAChalmers/dassmusik.git

### 2. Configure Dassmusik
There are a few things that are installation specific, if you're at ETA then you might not need to worry.

#### dassmusik.py
Change ```musicDirectory```to the directory containing music to be played. Make sure to use the globbing ** found in bash to traverse all subdirectories as well.

    musicDirectory = '<path to your music directory>'

#### start.sh & stop.sh
Make sure that the volume to control is set to the proper name, in rthe RPi case, this is PCM. The limits of ```i```can be set according to what value makes the sound clip.

    amixer -q set 'PCM' ${i}% > /dev/null

#### run_dassmusik.sh
Point the python script arguments to the candaemon source.

    python ./dassmusik.py <CanDaemon IP> <CanDaemon Port>

#### start_dassmusik_screen.sh
Update the variable ```DASSMUSIK_FOLDER``` to point to the folder where dassmusik resides. This is in order to be able to call the script from anywhere.

    DASSMUSIK_FOLDER=/home/eta/dassmusik

### 3. Configure mplayer
Edit your ```~/.mplayer/config``` and add the following lines:
    
    af-add=volnorm=2:0.75
    ao=alsa

This enables volume normalization and sets ALSA as audio output driver.

### 4. Set Dassmusik to start on boot.
The easiest way to do this is to use the user crontab.

Run ```crontab -e``` and enter the following line, adjusted for where you put the Dassmusik folder:

    @reboot /home/eta/dassmusik/start_dassmusik_screen.sh

This will start a screen running Dassmusik on computer start, emitting lovely music when the bathroom door is closed!
