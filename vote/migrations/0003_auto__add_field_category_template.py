# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.template'
        db.add_column('vote_category', 'template',
                      self.gf('django.db.models.fields.CharField')(default='category_basic.jade', max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.template'
        db.delete_column('vote_category', 'template')


    models = {
        'vote.alreadyvoted': {
            'Meta': {'object_name': 'AlreadyVoted'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'vote.ballot': {
            'Meta': {'object_name': 'Ballot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'vote.ballotcategory': {
            'Meta': {'object_name': 'BallotCategory'},
            'ballot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Ballot']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'vote.ballotoption': {
            'Meta': {'object_name': 'BallotOption'},
            'ballot_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.BallotCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Option']"}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'vote.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'category_basic.jade'", 'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'vote.option': {
            'Meta': {'object_name': 'Option'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['vote']