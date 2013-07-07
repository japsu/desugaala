# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OptionPicture'
        db.create_table('vote_optionpicture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.related.OneToOneField')(related_name='picture', unique=True, to=orm['vote.Option'])),
            ('thumbnail', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('preview', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('vote', ['OptionPicture'])


    def backwards(self, orm):
        # Deleting model 'OptionPicture'
        db.delete_table('vote_optionpicture')


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
        },
        'vote.optionpicture': {
            'Meta': {'object_name': 'OptionPicture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'option': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'picture'", 'unique': 'True', 'to': "orm['vote.Option']"}),
            'preview': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['vote']