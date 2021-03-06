# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('vote_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('vote', ['Category'])

        # Adding model 'Option'
        db.create_table('vote_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Category'])),
        ))
        db.send_create_signal('vote', ['Option'])

        # Adding model 'Ballot'
        db.create_table('vote_ballot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('vote', ['Ballot'])

        # Adding model 'BallotCategory'
        db.create_table('vote_ballotcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ballot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Ballot'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Category'])),
        ))
        db.send_create_signal('vote', ['BallotCategory'])

        # Adding model 'BallotOption'
        db.create_table('vote_ballotoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('ballot_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.BallotCategory'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Option'])),
        ))
        db.send_create_signal('vote', ['BallotOption'])

        # Adding model 'AlreadyVoted'
        db.create_table('vote_alreadyvoted', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('vote', ['AlreadyVoted'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('vote_category')

        # Deleting model 'Option'
        db.delete_table('vote_option')

        # Deleting model 'Ballot'
        db.delete_table('vote_ballot')

        # Deleting model 'BallotCategory'
        db.delete_table('vote_ballotcategory')

        # Deleting model 'BallotOption'
        db.delete_table('vote_ballotoption')

        # Deleting model 'AlreadyVoted'
        db.delete_table('vote_alreadyvoted')


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

    complete_apps = ['vote']