#!/usr/bin/python

import socket
import sys
import time
import datetime

import os
from fnmatch import fnmatch
import random

import packetizer
import subprocess

import alsaaudio

piz = packetizer.Packetizer()
NumRuns = 0
CurrentSong=None

mixer = alsaaudio.Mixer(control="PCM")

def untilNone( fnc ):
    res = fnc()
    while res != None:
        yield res
        res = fnc()

def readFiles(dir, pattern):
    fileList = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if fnmatch(name, pattern):
                fileList.append(os.path.join(path, name))
    return fileList

try:
    host = sys.argv[1]
    port = int( sys.argv[2] )
except:
    print "Script to play music accoring to opening and closing of bathroom door."
    print "Depends upon having a can->telnet interface using the auml homeautomation protocol."
    print "Usage: dassmusik.py candaemon_ip candaemon_port "
    sys.exit(1)

attemptTimeout = 15 # Time in seconds.
musicDirectory = '/home/eta/musik' # Directory in which music to play can be found.
songList = readFiles(musicDirectory, "*.mp3")

FNULL = open(os.devnull, 'w')

print "Read", len(songList), "songs from", musicDirectory

print "Starting dassmusik.py"
connected = False
while not connected:
    try:
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( (host, port) )
        connected = True
        print "Connected to %s:%s" % (host, port)
    except socket.error, msg:
        print "Socket error: ", msg
        print "Trying again in %s seconds." % (attemptTimeout)
        time.sleep(attemptTimeout)
        print "\r\nNew attempt to connect to %s:%s" % (host, port)

def startMplayer():
    print "Starting mplayer process."
    MusicCmd = 'mplayer -quiet -idle -slave -softvol'
    MusicProcess = subprocess.Popen(MusicCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    time.sleep(2) # Wait for mplayer to start properly.
    print "mplayer process started."
    mixer.setvolume(0)
    return MusicProcess

MusicProcess = startMplayer()

def stop():
    global FNULL
    for i in xrange(85,-1,-1):
        time.sleep(0.3/5)
        mixer.setvolume(i)

def stopAudio():
    stop()
    MusicProcess.stdin.write('pause\n')

def start():
    global FNULL
    time.sleep(0.7)
    for i in xrange(50, 85):
        time.sleep(0.3/5)
        mixer.setvolume(i)


def shellquote(s):
    return "'" + s.replace("'", "\\'") + "'"

def startAudio():
    global NumRuns, CurrentSong
    NumRuns = NumRuns + 1
    if MusicProcess.returncode != None:
        # mplayer has somehow crashed, reload!
        global MusicProcess
        MusicProcess = startMplayer()
    CurrentSong = random.choice(songList)
    MusicProcess.stdin.write("loadfile "+shellquote(CurrentSong)+"\n")
    start()

data = sock.recv( 1024 )

# Print text headers
print "CAN Source: %s:%s" % (host, port)

def printTimestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

oldState = 1;
while len( data ):
    piz.push( data )

    for (id, ext, f, data) in untilNone( piz.pop ):
        if id  == 0x14006401: #Toanod
            newState = data[1]
            if newState != oldState: # Changed state
                if newState == 0:
                    startAudio()
                    print "%s - Closed - Current song: %s" % (printTimestamp(), CurrentSong)
                if newState == 1:
                    print "%s - Open - #%s" % (printTimestamp(), NumRuns)
                    stopAudio()
                oldState = newState

    data = sock.recv( 1024 )

sock.close()

sys.exit( 0 );

