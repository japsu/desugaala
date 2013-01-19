# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Watch'
        db.create_table('status_watch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Category'])),
        ))
        db.send_create_signal('status', ['Watch'])

        # Adding model 'WatchOption'
        db.create_table('status_watchoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('watch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['status.Watch'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Option'])),
        ))
        db.send_create_signal('status', ['WatchOption'])


    def backwards(self, orm):
        # Deleting model 'Watch'
        db.delete_table('status_watch')

        # Deleting model 'WatchOption'
        db.delete_table('status_watchoption')


    models = {
        'status.watch': {
            'Meta': {'object_name': 'Watch'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'status.watchoption': {
            'Meta': {'object_name': 'WatchOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Option']"}),
            'watch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['status.Watch']"})
        },
        'vote.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'vote.option': {
            'Meta': {'object_name': 'Option'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['status']