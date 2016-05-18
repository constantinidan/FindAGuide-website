# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('Profile_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('Profile', ['Profile'])

        # Adding model 'City'
        db.create_table('Profile_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('Profile', ['City'])

        # Adding unique constraint on 'City', fields ['city_name', 'country']
        db.create_unique('Profile_city', ['city_name', 'country'])

        # Adding model 'Category_Activity'
        db.create_table('Profile_category_activity', (
            ('category_name', self.gf('django.db.models.fields.CharField')(primary_key=True, max_length=120, default='ABC')),
        ))
        db.send_create_signal('Profile', ['Category_Activity'])

        # Adding model 'Guide_Activity'
        db.create_table('Profile_guide_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Profile.City'])),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Profile.Profile'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Profile.Category_Activity'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30, default='')),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=120, default='')),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
        ))
        db.send_create_signal('Profile', ['Guide_Activity'])


    def backwards(self, orm):
        # Removing unique constraint on 'City', fields ['city_name', 'country']
        db.delete_unique('Profile_city', ['city_name', 'country'])

        # Deleting model 'Profile'
        db.delete_table('Profile_profile')

        # Deleting model 'City'
        db.delete_table('Profile_city')

        # Deleting model 'Category_Activity'
        db.delete_table('Profile_category_activity')

        # Deleting model 'Guide_Activity'
        db.delete_table('Profile_guide_activity')


    models = {
        'Profile.category_activity': {
            'Meta': {'object_name': 'Category_Activity'},
            'category_name': ('django.db.models.fields.CharField', [], {'primary_key': 'True', 'max_length': '120', 'default': "'ABC'"})
        },
        'Profile.city': {
            'Meta': {'unique_together': "(('city_name', 'country'),)", 'object_name': 'City'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Profile.guide_activity': {
            'Meta': {'object_name': 'Guide_Activity'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Profile.Category_Activity']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Profile.City']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120', 'default': "''"}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Profile.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "''"})
        },
        'Profile.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Profile']