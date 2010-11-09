from django.db import models
from django.contrib.auth.models import User

class AbstractContent(models.Model):
	objects = models.Manager()
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True
		app_label = 'rb'
		
class UserProfile(AbstractContent):
	user = models.ForeignKey(User,unique=True)
	lfmusername=models.CharField(max_length=25)
	artists = models.ManyToManyField('Artist')
	
class Track(AbstractContent):
	name = models.CharField(max_length=40)
	artist = models.ForeignKey('Artist',related_name='tracks')
	
class Artist(AbstractContent):
	name = models.CharField(max_length=40)