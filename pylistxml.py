#
# pylistfm - A Python module that creates last.fm playlists.
# Copyright (C) 2008 James Burkhart
#
# pylistfm is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pylistfm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import xml.sax.handler
import datamgmt
import string

SAVE_ITUNES_DB_FNAME = 'itunes.db'
class ITunesHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.parsing_tag = False
        self.tag = ''
        self.value = ''
        self.tracks = []
        self.track = None

    def startElement(self, name, attributes):
        if name == 'key':
            self.parsing_tag = True

    def characters(self, data):
        if self.parsing_tag:
            self.tag = data
            self.value = ''
        else:
            #could be multiple lines so append data
            self.value = self.value + data
            
    def endElement(self,name):
        if name == 'key':
            self.parsing_tag = False
        else:
            if self.tag == 'Track ID':
                #start of a new track, so new
                #object is needed
                self.track = Itunes_Track()
            elif self.tag == 'Name' and self.track:
                self.track.track = self.value
            elif self.tag == 'Artist' and self.track:
                self.track.artist = self.value
            elif self.tag == 'Album' and self.track:
                self.track.album = self.value
            elif self.tag == 'Persistent ID' and self.track:
                self.track.id = self.value
            elif self.tag == 'Total Time' and self.track:
                self.track.duration = self.value
            elif self.tag == 'Track Number' and self.track:
                self.track.track_number = self.value
            elif self.tag == 'Track Count' and self.track:
                self.track.track_count = self.value
            elif self.tag == 'Bit Rate' and self.track:
                self.track.bit_rate = self.value
            elif self.tag == 'Sample Rate' and self.track:
                self.track.sample_rate = self.value
            elif self.tag == 'Play Count' and self.track:
                self.track.playcount = self.value
            elif self.tag == 'Location' and self.track:
                self.track.location = self.value
                #assume this is all the data we
                #need. so append the track object
                #to the list and reset track object
                #to none
                self.tracks.append(self.track)
                self.track = None

class Itunes_Track:
    def __init__(self):
        self.track = None
        self.name_lower = None
        self.artist = None
        self.artist_lower = None
        self.album = None
        self.location = None
        self.id = None
        self.track_number = None
        self.track_count = None
        self.duration = None
        self.bit_rate = None
        self.sample_rate = None
        self.playcount = 0

    def __str__(self):
        return 'ITUNES: Track = %s\nArtist = %s\n' % (self.track,self.artist)
class Itunes_Artist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.track_names_lower = []
        self.duplicate_tracks = []
        self.duplicate_track_names = []
        self.albums = []
    def __str__(self):
        return "ITUNES: Artist %s (%d tracks)" % (self.name, len(self.tracks))


class Itunes_Library:
    def __init__(self, artists):
        self.artists = artists
        self.artists.sort()
        self.artistcount = len(artists)
        self.trackcount = sum([len(a.tracks) for a in artists])
        
    def __str__(self):
        return "ITUNES: %d artists with a total of %d tracks" % (self.artistcount, self.trackcount)

def parse_itunes(fname):
    itunes_fname = SAVE_ITUNES_DB_FNAME
    if itunes_fname==None: 
      itunes_fname = 'itunes.db'
    parser = xml.sax.make_parser()
    handler = ITunesHandler()
    parser.setContentHandler(handler)
    parser.parse(fname)

    parsed_artists = [] #strings of artist names
    parsed_artists_lower = [] #lowercase strings of all artist name strings added to parsed_artists
    parsed_tracks = []
    
    for track in handler.tracks:
        parsed_tracks.append(track)
        if type(track.artist) != type(None): # otherwise blank artist field causes error
            if unicode.lower(track.artist) not in parsed_artists_lower:
                parsed_artists.append(track.artist)
                parsed_artists_lower.append(unicode.lower(track.artist))
  
    for i in range(len(parsed_artists)):
        parsed_artists[i] = Itunes_Artist(parsed_artists[i]) #convert strings into Itunes_Artist objects

    count = 0
    total_count = len(parsed_artists)
    report_at = [10,20,30,40,50,60,70,80,90,99,1000] #1000 included just in case
    
    for artist in parsed_artists: #itunes_artist objects
        for track in parsed_tracks: #itunes_track objects
            if type(track.artist) != type(None) and type(artist.name) != type(None) and type(track.track) != type(None):
                if unicode.lower(track.artist) == unicode.lower(artist.name) and unicode.lower(track.track) not in artist.track_names_lower:
                    artist.track_names_lower.append(string.lower(track.track))
                    artist.tracks.append(track)
                elif unicode.lower(track.artist) == unicode.lower(artist.name) and unicode.lower(track.track) in artist.track_names_lower:
                    artist.duplicate_track_names.append(unicode.lower(track.track))
                
        count += 1
        progress = int((float(count) / total_count) * 100)
        if progress >= report_at[0]:
            print 'Progress: %3d' % (progress),'%'
            report_at.remove(report_at[0])

    print 'Processing duplicate tracks...'
    for artist in parsed_artists:
      [artist.duplicate_tracks.append(track) for track in artist.tracks if string.lower(track.track) in artist.duplicate_track_names]
      
    print 'Creating library file...'
    library = Itunes_Library(parsed_artists)
    print 'Complete! Library being saved as \'%s\''%(itunes_fname)
    datamgmt.save(library,itunes_fname)
    
def load(fname):
    import pickle
    f = open(fname,'rb')
    lib = pickle.load(f)
    f.close()
    return lib
