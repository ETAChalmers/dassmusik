class Packetizer:
    def __init__( self ):
        self.buffer = ''

    def push( self, str ):
        self.buffer += str

    def pop( self ):
        (first, s, last) = self.buffer.partition( "\n" )
        if last != '':
            self.buffer = last
            fields = first.split( ' ' )
            if fields[0].lower() == 'pkt':
                id = int( fields[1], 16 )
                ext = int( fields[2], 16 )
                flagb = int( fields[3], 16 )
                data = [ int( x, 16 ) for x in fields[4:] ]
                return (id, ext, flagb, data)
        return None
