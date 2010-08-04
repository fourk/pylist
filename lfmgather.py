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

__version__ = '0.2.0'
__doc__ = 'A Python module that creates last.fm playlists'
__author__ = 'James Burkhart'
__email__ = 'jburkhart@gm.slc.edu'
__copyright__ = 'James Burkhart 2008-09 under GNU GPL v3. Dependent upon the included pylast module, copyright Amr Hassan 2008 under GNU GPL v2.'
############################
##########TO DO:############
# Find redundancies in pylast.Track objects and functions which use them.
# Update gui
# Get rid of Itunes_Library class
#
import datamgmt #used for saving and loading stuff
import pylast #used to create pylast track objects
import pylistxml #used to reference Itunes_Track constructor for Hybrid_Track constructor
import time #used by timefunc() and makeprogress()
import os #used to get current dir for NETWORK.enable_caching call. and in 'progress' checking
import filters
NETWORK = pylast.get_lastfm_network(datamgmt.API_KEY,datamgmt.API_SECRET,datamgmt.SESSION_KEY)
NETWORK.enable_caching(os.getcwd()+os.sep+'cachingdb.db')

class Hybrid_Track(pylistxml.Itunes_Track,pylast.Track):
    def __init__(self,itunes_track):
        pylistxml.Itunes_Track.__init__(self)
        pylast.Track.__init__(self,itunes_track.artist,itunes_track.track,NETWORK)
        
        self.track = itunes_track.track
        self.artist_name = itunes_track.artist
        self.album_name = itunes_track.album
        self.location = itunes_track.location
        self.itunes_id = itunes_track.id #switch this to itunes_id?
        self.track_number = itunes_track.track_number
        self.track_count = itunes_track.track_count
        self.file_duration = itunes_track.duration
        self.bit_rate = itunes_track.bit_rate
        self.sample_rate = itunes_track.sample_rate
        self.playcount = itunes_track.playcount
        self.artist = self.get_artist()
        self.album = self.get_album()
        self.listener_count = 0 #unsure of why, but there was an error 12/11/09 with a track that had get_data() called not actually filling in this field
        self.lfm_playcount = 0#see note for .listener_count
        
    def get_data(self):
        self.listener_count = self.get_listener_count()
        self.lfm_playcount = self.get_playcount()
        

    def get_more_data(self): # not actually called by anything as of yet. took this out of get_data to speed up process_artists
        self.similar_tracks = self.get_similar()
        self.tag_tuples = self.get_top_tags()
        self.lfm_duration = self.get_duration()
        self.mbid = self.get_mbid()
        
    def refresh_network(self):
        self.network = NETWORK

    def __str__(self):
        return unicode(self.artist_name +' - '+ self.track)
def get_lfm_info(itunes_library):
    """  Gets info from last.fm for each Itunes_Artist object in the artists field of an itunes_library object.  Saves a list of Hybrid_Track files"""
    tracks = [] #list of all tracks of all artists
    
    #create list of all tracks
    print 'creating list of all tracks'
    for artist in itunes_library.artists:
        for track in artist.tracks:
            tracks.append(track)
    print 'list created, %d tracks to parse'%(len(tracks))
    report_at = [5,10,20,30,40,50,60,70,80,90,1000]
    total_count = len(tracks)

    #lists for fail/success tracks
    fails = []
    no_fail=[]
    
    #make each Itunes_Track in tracks into a Hybrid_Track
    for count in range(total_count):
        try:
            try:
                tracks[count] = Hybrid_Track(tracks[count])
                no_fail.append(tracks[count])
            except pylast.WSError:
                print 'error with', unicode(tracks[count])
                fails.append(tracks[count])
        except:
            print 'ascii error on track',count #this except statement SHOULD be unneccessary now, with the track printed in unicode
            fails.append(tracks[count])
        #    print 'xml error on:',tracks[count]
        progress = int((float(count)/total_count)*100)
        if progress >= report_at[0]:
            print 'Progress %3d' % (progress),'%'
            report_at.remove(report_at[0])
    print 'Progress: 100 %'
    print 'Total failed tracks: %d' % (len(fails))

    #TEST-CODE:
    checksum = len(no_fail)+len(fails)
    if checksum != len(tracks):
        print 'ERROR HAPPEN FFFFFF'

    tracks = no_fail
        
    #save list of Itunes_Artist objects containing Hybrid_Track objects within their tracks field.
    #10/12/09: currently saves list of Hybrid_Track objects
    try:
        artists = []
        print 'woop'
        artistnames=[]
        for track in tracks:
            if track.get_artist().get_name() not in artistnames:
                artists.append(track.get_artist())
                artistnames.append(track.get_artist().get_name())
        for artist in artists:
            artist.tracks = []
            for track in tracks:
                if track.get_artist() == artist:
                    artist.tracks.append(track)
            artist.trackcount=len(artist.tracks)
    except:
        return tracks
    print 'saving!'
    datamgmt.save(artists,'incompleteartists.db')
    datamgmt.save(fails,'failedtracks.db')

#---------- External Data Gathering -----------#
def process_info(fname='incompleteartists.db',v=False): #get playcount info for all artists, returns a new list of artists
    """Gets all playcount info for all artist objects. v=verbose"""
    global artists
    import random
    artists = datamgmt.load(fname)
    fname = 'artists.db'
    random.shuffle(artists)
    newartists =[]
    artist_count = len(artists)
    print 'Getting info for each track by %d artists. This could take a very long time (approximately 1 minute per hundred tracks).' % artist_count
    for i in range(artist_count):
        print '%d/%d' % (i,artist_count)
        try:
            processed_artist = process_artist(artists[i],v)
        except:
            try:
                processed_artist = process_artist(artists[i],v)
            except:
                print 'Errors processing',unicode(artists[i])
        newartists.append(processed_artist)
    artists = newartists
    print 'calculating ratios...'
    calculate_ratios()
    try:
        datamgmt.save(artists,fname)
        print 'saved successfully'
    except:
        try:
            NETWORK.disable_caching()
            datamgmt.save(artists,fname)
            print 'data saved successfully'
            NETWORK.enable_caching()
        except:
            global errors
            errors = newartists
            print 'Error during save. Artists stored as var: errors'
    

def process_artist(artist,v=False): #get playcount info for one artist. used by process_info()
    """Gets all playcount info for one artist object"""
    if v == True:
        print 'Getting info on each track by', unicode(artist.get_name())
    newartist = artist
    newartist.sum_playcount = 0
    newartist.network = NETWORK
    newartist.playcount=newartist.get_playcount()
    newtracks = []
    for track in artist.tracks:
        newtracks.append(process_track(track,v))
        newartist.sum_playcount += track.lfm_playcount
    newartist.tracks = newtracks
    return newartist

def process_track(track,v=False): #get playcount info for one track, used by process_artist()

    """ Gets all playcount info for one Hybrid_Track object"""
    if v == True:
        print '\t\t Getting info for ' +unicode(track.get_name())
    try:
        track.refresh_network()
        track.get_data()
    except:
        track.lfm_playcount = 1
        track.duration = 0
        track.listener_count = 1
        try:
            track.refresh_network()
            track.get_data()
        except:
            print
            print 'ERROR: information for %s by %s unavailable' % (track.title,track.artist_name)
            print
    return track

#---------- Data-Calculation ----------#

def calculate_ratios(): #calculates ratio info for all tracks
    global artists
    for a in artists:
        a.trackcount = 0
        for t in a.tracks:
            if t.listener_count > 1:
                ratio = float(t.lfm_playcount) / float(t.listener_count)
                t.ratio = ratio
                a.trackcount+=1
            else:
                try:
                    print 'The following track has 0 or 1 listeners, indicative of an error somewhere: ',t
                except:
                    print 'A track has 0 or 1 listeners due to a character that does not exist in ascii.'
                t.ratio = 0
    print 'Ratios calculated for individual tracks. Calculating avg ratios for all artists.'
    calculate_artist_ratio()
                
def calculate_artist_ratio(): # calculates ratio info for all artists. called AFTER calculate_ratios()
    global artists
    for a in artists:
        ratios = []
        for t in a.tracks:
            if t.ratio > 0: #ratio = 0 means there's an error getting ratio data for a track, ignore that track.
                ratios.append(t.ratio)
        total = 0
        for r in ratios:
            total += r
        if len(ratios) >= 1:
            a.ratio = total / len(ratios)
        else:
            print 'error with',a,' - Artist did not have any tracks with valid (> 0) ratios.'
            a.ratio = 0
    remove_invalids()

def remove_invalids():
    global artists
    invalid_artist_count = 0
    invalid_track_count = 0
    for a in artists:
        if a.ratio == 0:
            artists.remove(a)
            invalid_artist_count+=1
    for artist in artists:
        for track in artist.tracks:
            if track.ratio == 0:
                artist.tracks.remove(track)
                invalid_track_count +=1
    print 'removed %d invalid artists and %d invalid tracks' %(invalid_artist_count,invalid_track_count)

def makeprogress():
    done = False
    while done==False:
        filenames = os.listdir(os.getcwd())
        if 'artists.db' in filenames:
            done=True #done w/ everything.
            global artists
            artists = datamgmt.load('artists.db')
        elif 'incompleteartists.db' in filenames:
            process_info()
        elif 'itunes.db' in filenames:
            get_lfm_info(datamgmt.load('itunes.db'))
        elif 'Library.xml' in filenames:
            pylistxml.parse_itunes('Library.xml')
        else:
            print 'You need to put an iTunes xml export in the same directory as lfmgather.py'
            print 'Directions:'
            print 'Within iTunes, click File -> Library -> Export Library...'
            print 'Browse to the directory where lfmgather.py is located and save as the default \'Library.xml\''
            print 'Then restart this application.'
            done = True
        if done == False:
            time.sleep(10)
