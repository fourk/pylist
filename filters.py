#---------- Playlist generation ------#
import random
def make_playlist(artists,songcount):
    """ Makes a playlist selection of length songcount from global artists"""
    potential_picks = []
    songs = []
    for artist in artists: #artist objs are pylast.Artist instances
        for track in artist.tracks: #track objs are lfmgather.Hybrid_Track objects
            potential_picks.append(artist)
    if songcount > len(potential_picks):
        print 'You chose more songs than you even have. Program aborting.'
        return
    picks = random.sample(potential_picks, songcount)
    for pick in picks:
        song = pick_song(pick)
        songs.append(song)
    for song in songs:
        print unicode(song)
    return songs
        #playlist.addTrack(song)

def make_playlist2(artists,songcount):
    """Returns a playlist using ratio info"""
    songs = []
    for artist in artists:
        artist.weight = artist.ratio * artist.trackcount
    for i in range(songcount):
        artist = pick_artist(artists)
        if len(artist.tracks)==1:
            artists.remove(artist)
        song = pick_song(artist)
        artist.weight = artist.ratio * artist.trackcount
        songs.append(song)
    return songs

#---------- Filters/Sorts -- return filtered/sorted lists
def filter_artists_by_minPlaycount(artists,minPlaycount):
    """Returns a list of artists filtered by minimum personal playcount info"""
    newartists = []
    for artist in artists:
        if int(artist.userplaycount) >= minPlaycount:
            newartists.append(artist)
    return newartists

def filter_artists_by_maxPlaycount(artists,maxPlaycount): #personal playcount info
    """Returns a list of artists filtered by maximum personal playcount info"""
    newartists = []
    for artist in artists:
        if int(artist.userplaycount) <= maxPlaycount:
            newartists.append(artist)
    return newartists

def filter_tracks_by_minPlaycount(artists,minPlaycount):
    """Returns a list of tracks filtered by minimum personal playcount info"""
    newartists = []
    for artist in artists:
        newtracks = []
        for track in artist.tracks:
            if int(track.userplaycount) >= minPlaycount:
                newtracks.append(track)
        if newtracks != []:
            artist.tracks = newtracks
            artist.playcount = 0
            for track in artist.tracks:
                artist.playcount += track.playcount
            newartists.append(artist)
    return newartists

def filter_tracks_by_maxPlaycount(artists,maxPlaycount):
    """Returns a list of tracks filtered by maximum personal playcount info"""
    newartists = []
    for artist in artists:
        newtracks = []
        for track in artist.tracks:
            if int(track.userplaycount) <= maxPlaycount:
                newtracks.append(track)
        if newtracks != []:
            artist.tracks = newtracks
            artist.playcount = 0
            for track in artist.tracks:
                artist.playcount += track.playcount
            newartists.append(artist)
    return newartists

def sort_ratios(items):
    import operator
    items.sort(key=operator.attrgetter('ratio'),reverse=True)
    return items
def filter_tracks_by_minRatio(artists,minRatio):
  newartists = []
  for artist in artists:
    newtracks = []
    for track in artist.tracks:
      if int(track.ratio) >= minRatio:
        newtracks.append(track)
    if newtracks != []:
      artist.tracks = newtracks
      artist.playcount = 0
      for track in artist.tracks:
        artist.playcount += track.playcount
      newartists.append(artist)
  return newartists
        #EXCEPTION: 'Error with filter_tracks_by_minRatio. Have you calculated ratios yet?'
def checkdoubles(): #returns a list of duplicate tracks in individual_artists based on MBID.
    mbid_to_track = {}
    mbids = []
    duplicates = []
    for artist in individual_artists:
        for track in artist.tracks:
            if track.mbid not in mbids:
                mbids.append(track.mbid)
                mbid_to_track[track.mbid] = track
                
            else:
                print 'WTFWTFWTF'
                duplicates.append(track)
                duplicates.append(mbid_to_track[track.mbid])
    return duplicates

def pick_artist(artists):
    totalweight = 0.0
    count = 0.0
    for a in artists:
        totalweight += a.weight
    r = random.uniform(0,totalweight)
    for a in artists:
        #print r,a.weight,count
        count += a.weight
        #print '+',a.weight,'=',count,'<',r
        if count >= r:
            return a
        #else:
            #print 'skipping',a


def pick_song(artist):
    """Given an artist object, picks a song based on playcount weights"""
    count = 0
    r = random.randint(1,artist.sum_playcount)
    for i in range(len(artist.tracks)):
        count += artist.tracks[i].lfm_playcount
        if r <= count:
            artist.trackcount -= 1
            artist.sum_playcount -= artist.tracks[i].lfm_playcount
            return artist.tracks.pop(i)
            
def filter_similar_tracks(artists):
    tracklist = []
    for artist in artists:
      for track in artist.tracks:
        tracklist.append(track)
    
    for track1 in tracklist:
      new_similar_tracks = []
      for tuple in track1.similar_tracks:
        for track2 in tracklist:
          if tuple['item'] == track2:
            new_similar_tracks.append(tuple)
      track1.similar_tracks = new_similar_tracks
    return artists,tracklist
