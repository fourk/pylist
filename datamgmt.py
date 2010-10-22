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
API_KEY = 'a9785e0b1bb8deb9eb4e090b3aba9613'
API_SECRET = '2eabc2dd9f2d1364a7c84bcffdbc9901'
SESSION_KEY = u'02675f176ccc949b43bf118224dcd06d'
import cPickle as pickle
import string
import codecs
def save(data,filename): #saves data as filename
    """Saves data in a given filename"""
    file = open(filename,'wb')
    try:
        pickle.dump(data,file,2)
        print 'data saved!'
    except:
        print 'ERROR SAVING. Are you using ipython? If so, don\'t.'
    file.close() 
def load(fname):
    f = open(fname,'rb')
    data = pickle.load(f)
    f.close()
    return data
def make_m3u(songs):
    f = codecs.open('playlistnew.m3u','w','utf-8')
    f.write(u'#EXTM3U\n')
    for song in songs:
        newstring = u'#EXTINF:'+unicode((int(song.file_duration) / 1000))+u','
        newstring+=unicode(song.track)+u'\n'
        f.write(unicode(newstring))
        newstring = song.location
        newstring = string.replace(newstring,'%20',' ')
        newstring = string.replace(newstring,'%5B','[')
        newstring = string.replace(newstring,'%5D',']')
        newstring = newstring[17:] + '\n'
        f.write(unicode(newstring))
    f.close()
def make_m3u_osx(songs):
    f = codecs.open('playlistnew.m3u','w','utf-8')
    f.write('#EXTM3U\n')
    for song in songs:
        newstring = '#EXTINF:'+str((int(song.file_duration) / 1000))+','+song.__str__()+'\n'
        f.write(unicode(newstring))
        newstring = song.location
        newstring = string.replace(newstring,'%20',' ')
        newstring = string.replace(newstring,'%5B','[')
        newstring = string.replace(newstring,'%5D',']')
        newstring = newstring[16:] + '\n'
        #newstring = '/media/disk' + newstring[2:]
        f.write(newstring)
    f.close()
