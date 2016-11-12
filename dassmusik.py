#!/usr/bin/python

import socket
import sys
import time
import datetime

import packetizer
import subprocess

piz = packetizer.Packetizer()
NumRuns = 0

def untilNone( fnc ):
    res = fnc()
    while res != None:
        yield res
        res = fnc()

try:
    host = sys.argv[1]
    port = int( sys.argv[2] )
except:
    print "Script to play music accoring to opening and closing of bathroom door."
    print "Depends upon having a can->telnet interface using the auml homeautomation protocol."
    print "Usage: dassmusik.py candaemon_ip candaemon_port "
    sys.exit(1)

attemptTimeout = 15 # Time in seconds.
musicDirectory = '/home/eta/musik/**' # Directory in which music to play can be found.

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
    MusicCmd = 'mplayer -quiet -slave -softvol -shuffle %s' % musicDirectory
    MusicProcess = subprocess.Popen(MusicCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    time.sleep(2) # Wait for mplayer to start properly.
    MusicProcess.stdin.write('pause\n')
    print "mplayer process started."
    return MusicProcess

def stopAudio():
    subprocess.call(['./stop.sh'])
    MusicProcess.stdin.write('pause\n')

def startAudio():
    global NumRuns
    NumRuns = NumRuns + 1
    MusicProcess.stdin.write('mute 1\n')
    MusicProcess.stdin.write('pt_step 1\n')	
    MusicProcess.stdin.write('mute 0\n')
    subprocess.call(['./start.sh'])

MusicProcess = startMplayer()

data = sock.recv( 1024 )

# Print text headers
print "CAN Source: %s:%s" % (host, port)

oldState = 1;
while len( data ):
    piz.push( data )

    for (id, ext, f, data) in untilNone( piz.pop ):
        if (id & 0xFFFFFF00)  == 0x14006400: # type=chn, chn=toanod 0x0064
            newState = data[1]
            if newState != oldState: # Changed state
                if newState == 0:
                    print "%s - Closed" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                    startAudio()
                if newState == 1:
                    print "%s - Open - #%s" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), NumRuns)
                    stopAudio()
                oldState = newState

    data = sock.recv( 1024 )

sock.close()

sys.exit( 0 );
