# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('lfm_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reach', self.gf('django.db.models.fields.IntegerField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('lfm', ['Tag'])

        # Adding model 'Image'
        db.create_table('lfm_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=100)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('lfm', ['Image'])

        # Adding model 'Artist'
        db.create_table('lfm_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('listeners', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('playcount', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('lfm', ['Artist'])

        # Adding M2M table for field tags on 'Artist'
        db.create_table('lfm_artist_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['lfm.artist'], null=False)),
            ('tag', models.ForeignKey(orm['lfm.tag'], null=False))
        ))
        db.create_unique('lfm_artist_tags', ['artist_id', 'tag_id'])

        # Adding M2M table for field images on 'Artist'
        db.create_table('lfm_artist_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['lfm.artist'], null=False)),
            ('image', models.ForeignKey(orm['lfm.image'], null=False))
        ))
        db.create_unique('lfm_artist_images', ['artist_id', 'image_id'])

        # Adding model 'Album'
        db.create_table('lfm_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('listeners', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('playcount', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='albums', to=orm['lfm.Artist'])),
            ('lfmid', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('lfm', ['Album'])

        # Adding M2M table for field tags on 'Album'
        db.create_table('lfm_album_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['lfm.album'], null=False)),
            ('tag', models.ForeignKey(orm['lfm.tag'], null=False))
        ))
        db.create_unique('lfm_album_tags', ['album_id', 'tag_id'])

        # Adding M2M table for field images on 'Album'
        db.create_table('lfm_album_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['lfm.album'], null=False)),
            ('image', models.ForeignKey(orm['lfm.image'], null=False))
        ))
        db.create_unique('lfm_album_images', ['album_id', 'image_id'])

        # Adding model 'Track'
        db.create_table('lfm_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('listeners', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('playcount', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['lfm.Artist'])),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['lfm.Album'])),
            ('lfmid', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('lfm', ['Track'])

        # Adding M2M table for field tags on 'Track'
        db.create_table('lfm_track_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm['lfm.track'], null=False)),
            ('tag', models.ForeignKey(orm['lfm.tag'], null=False))
        ))
        db.create_unique('lfm_track_tags', ['track_id', 'tag_id'])

        # Adding model 'SimilarArtist'
        db.create_table('lfm_similarartist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('match', self.gf('django.db.models.fields.FloatField')()),
            ('from_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_from', to=orm['lfm.Artist'])),
            ('to_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_to', to=orm['lfm.Artist'])),
        ))
        db.send_create_signal('lfm', ['SimilarArtist'])

        # Adding model 'SimilarTrack'
        db.create_table('lfm_similartrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('match', self.gf('django.db.models.fields.FloatField')()),
            ('from_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_from', to=orm['lfm.Track'])),
            ('to_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_to', to=orm['lfm.Track'])),
        ))
        db.send_create_signal('lfm', ['SimilarTrack'])

        # Adding model 'UserTrack'
        db.create_table('lfm_usertrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('useraccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lfm.UserAccount'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lfm.Track'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('lfm', ['UserTrack'])

        # Adding model 'UserAccount'
        db.create_table('lfm_useraccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('lfm', ['UserAccount'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('lfm_tag')

        # Deleting model 'Image'
        db.delete_table('lfm_image')

        # Deleting model 'Artist'
        db.delete_table('lfm_artist')

        # Removing M2M table for field tags on 'Artist'
        db.delete_table('lfm_artist_tags')

        # Removing M2M table for field images on 'Artist'
        db.delete_table('lfm_artist_images')

        # Deleting model 'Album'
        db.delete_table('lfm_album')

        # Removing M2M table for field tags on 'Album'
        db.delete_table('lfm_album_tags')

        # Removing M2M table for field images on 'Album'
        db.delete_table('lfm_album_images')

        # Deleting model 'Track'
        db.delete_table('lfm_track')

        # Removing M2M table for field tags on 'Track'
        db.delete_table('lfm_track_tags')

        # Deleting model 'SimilarArtist'
        db.delete_table('lfm_similarartist')

        # Deleting model 'SimilarTrack'
        db.delete_table('lfm_similartrack')

        # Deleting model 'UserTrack'
        db.delete_table('lfm_usertrack')

        # Deleting model 'UserAccount'
        db.delete_table('lfm_useraccount')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lfm.album': {
            'Meta': {'object_name': 'Album'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'albums'", 'to': "orm['lfm.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Image']", 'symmetrical': 'False'}),
            'lfmid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'lfm.artist': {
            'Meta': {'object_name': 'Artist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Image']", 'symmetrical': 'False'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'similar': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Artist']", 'through': "orm['lfm.SimilarArtist']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'lfm.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        },
        'lfm.similarartist': {
            'Meta': {'object_name': 'SimilarArtist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_from'", 'to': "orm['lfm.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.FloatField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_to'", 'to': "orm['lfm.Artist']"})
        },
        'lfm.similartrack': {
            'Meta': {'object_name': 'SimilarTrack'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_from'", 'to': "orm['lfm.Track']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.FloatField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_to'", 'to': "orm['lfm.Track']"})
        },
        'lfm.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reach': ('django.db.models.fields.IntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lfm.track': {
            'Meta': {'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': "orm['lfm.Album']"}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': "orm['lfm.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lfmid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'similar': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Track']", 'through': "orm['lfm.SimilarTrack']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'lfm.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Track']", 'through': "orm['lfm.UserTrack']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'lfm.usertrack': {
            'Meta': {'object_name': 'UserTrack'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.Track']"}),
            'useraccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.UserAccount']"})
        }
    }

    complete_apps = ['lfm']
