# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Puzzle.function'
        db.add_column(u'main_puzzle', 'function',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Puzzle.function'
        db.delete_column(u'main_puzzle', 'function')


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
        u'main.announcement': {
            'Meta': {'object_name': 'Announcement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teams_read': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Team']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        u'main.guess': {
            'Meta': {'object_name': 'Guess'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pagehit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['track.PageHit']", 'null': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Puzzle']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Team']", 'null': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'main.hunt': {
            'Meta': {'object_name': 'Hunt'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'debriefed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'main.message': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Team']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'main.node': {
            'Meta': {'object_name': 'Node'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.puzzle': {
            'Meta': {'object_name': 'Puzzle'},
            'clue': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Node']", 'unique': 'True', 'null': 'True'}),
            'show_solution_box': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'solution': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Team']", 'through': u"orm['main.TeamPuzzle']", 'symmetrical': 'False'})
        },
        u'main.team': {
            'Meta': {'object_name': 'Team'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'nodes_visible': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[0, 1, 2, 3]', 'to': u"orm['main.Node']", 'symmetrical': 'False'}),
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
        u'main.token': {
            'Meta': {'object_name': 'Token'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        u'track.pagehit': {
            'Meta': {'object_name': 'PageHit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['main']