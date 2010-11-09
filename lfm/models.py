from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AbstractContent(models.Model):
	objects = models.Manager()
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True
		app_label = 'lfm'

class AbstractSimilar(AbstractContent):
	match = models.FloatField()
	def __unicode__(self):
		return '<%s> (%s%)'%(str(self.from_id),self.match)
	class Meta:
		abstract = True
		app_label = 'lfm'
		
class LFMContent(AbstractContent):
	name = models.CharField(max_length=255)
	tags = models.ManyToManyField("Tag")
	url = models.URLField(verify_exists=False)
	mbid = models.CharField(max_length=36)
	listeners = models.IntegerField(max_length=10)
	playcount = models.IntegerField(max_length=10)
	class Meta:
		abstract = True
		app_label = 'lfm'
		
class Tag(AbstractContent):
	name = models.CharField(max_length=50)
	reach = models.IntegerField()
	summary = models.CharField(max_length=100)
	
class Image(AbstractContent):
	url = models.URLField(max_length=100)
	size = models.CharField(max_length=10)

class Artist(LFMContent):
	similar = models.ManyToManyField("self", through="SimilarArtist", symmetrical=False)
	images = models.ManyToManyField(Image)
	
class Album(LFMContent):
	artist = models.ForeignKey(Artist, related_name='albums')
	images = models.ManyToManyField(Image)
	lfmid = models.CharField(max_length=25,null=True,blank=True)
	
class Track(LFMContent):
	artist = models.ForeignKey(Artist, related_name='tracks')
	album = models.ForeignKey(Album, related_name='tracks')
	similar = models.ManyToManyField("self", through="SimilarTrack", symmetrical=False)
	lfmid = models.CharField(max_length=25, null=True,blank=True)
	duration = models.IntegerField(max_length=10)
	
class SimilarArtist(AbstractSimilar):
	from_id = models.ForeignKey(Artist,related_name='similar_from')
	to_id = models.ForeignKey(Artist,related_name='similar_to')
	
class SimilarTrack(AbstractSimilar):
	from_id = models.ForeignKey(Track,related_name='similar_from')
	to_id = models.ForeignKey(Track,related_name='similar_to')

class UserTrack(AbstractContent):
	useraccount = models.ForeignKey("UserAccount")
	track = models.ForeignKey(Track)
	location = models.CharField(max_length=50,blank=True)
	
class UserAccount(AbstractContent):
	user = models.ForeignKey(User, unique=True)
	tracks = models.ManyToManyField(Track, through="UserTrack")
