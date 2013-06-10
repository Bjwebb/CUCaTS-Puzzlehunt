# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Response'
        db.create_table(u'questionnaire_response', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('most_interesting_puzzle', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='response_most_interesting', null=True, to=orm['main.Puzzle'])),
            ('least_interesting_puzzle', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='response_least_interesting', null=True, to=orm['main.Puzzle'])),
            ('length_of_puzzlehunt', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('opinion_of_overall_structure', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('aspects_of_puzzles_you_liked', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('aspects_of_puzzles_you_disliked', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('website_suggestions', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('other_comments', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('would_you_compete_again', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True)),
        ))
        db.send_create_signal(u'questionnaire', ['Response'])

        # Adding model 'PuzzleResponse'
        db.create_table(u'questionnaire_puzzleresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Response'])),
            ('puzzle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Puzzle'])),
            ('difficulty', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('interest', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'questionnaire', ['PuzzleResponse'])


    def backwards(self, orm):
        # Deleting model 'Response'
        db.delete_table(u'questionnaire_response')

        # Deleting model 'PuzzleResponse'
        db.delete_table(u'questionnaire_puzzleresponse')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.puzzle': {
            'Meta': {'object_name': 'Puzzle'},
            'clue': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'fromnode': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'solution': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Team']", 'through': u"orm['main.TeamPuzzle']", 'symmetrical': 'False'}),
            'tonode': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.team': {
            'Meta': {'object_name': 'Team'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'puzzles_completed': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Puzzle']", 'symmetrical': 'False', 'blank': 'True'}),
            'score1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'score2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'})
        },
        u'main.teampuzzle': {
            'Meta': {'object_name': 'TeamPuzzle'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Puzzle']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Team']"})
        },
        u'questionnaire.puzzleresponse': {
            'Meta': {'object_name': 'PuzzleResponse'},
            'difficulty': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Puzzle']"}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Response']"})
        },
        u'questionnaire.response': {
            'Meta': {'object_name': 'Response'},
            'aspects_of_puzzles_you_disliked': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'aspects_of_puzzles_you_liked': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'least_interesting_puzzle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'response_least_interesting'", 'null': 'True', 'to': u"orm['main.Puzzle']"}),
            'length_of_puzzlehunt': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'most_interesting_puzzle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'response_most_interesting'", 'null': 'True', 'to': u"orm['main.Puzzle']"}),
            'opinion_of_overall_structure': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'other_comments': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'website_suggestions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'would_you_compete_again': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['questionnaire']