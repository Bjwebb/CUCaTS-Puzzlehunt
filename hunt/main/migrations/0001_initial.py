# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Puzzle'
        db.create_table(u'main_puzzle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('fromnode', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tonode', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('solution', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('clue', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'main', ['Puzzle'])

        # Adding model 'Team'
        db.create_table(u'main_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('score1', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('score2', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'main', ['Team'])

        # Adding M2M table for field members on 'Team'
        db.create_table(u'main_team_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'main.team'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'main_team_members', ['team_id', 'user_id'])

        # Adding M2M table for field puzzles_completed on 'Team'
        db.create_table(u'main_team_puzzles_completed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'main.team'], null=False)),
            ('puzzle', models.ForeignKey(orm[u'main.puzzle'], null=False))
        ))
        db.create_unique(u'main_team_puzzles_completed', ['team_id', 'puzzle_id'])

        # Adding model 'TeamPuzzle'
        db.create_table(u'main_teampuzzle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Team'])),
            ('puzzle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Puzzle'])),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'main', ['TeamPuzzle'])

        # Adding model 'Guess'
        db.create_table(u'main_guess', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('puzzle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Puzzle'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Team'], null=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pagehit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['track.PageHit'], null=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Guess'])

        # Adding model 'Announcement'
        db.create_table(u'main_announcement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Announcement'])

        # Adding M2M table for field teams_read on 'Announcement'
        db.create_table(u'main_announcement_teams_read', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('announcement', models.ForeignKey(orm[u'main.announcement'], null=False)),
            ('team', models.ForeignKey(orm[u'main.team'], null=False))
        ))
        db.create_unique(u'main_announcement_teams_read', ['announcement_id', 'team_id'])

        # Adding model 'Message'
        db.create_table(u'main_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Team'])),
            ('judges', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Puzzle'
        db.delete_table(u'main_puzzle')

        # Deleting model 'Team'
        db.delete_table(u'main_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table('main_team_members')

        # Removing M2M table for field puzzles_completed on 'Team'
        db.delete_table('main_team_puzzles_completed')

        # Deleting model 'TeamPuzzle'
        db.delete_table(u'main_teampuzzle')

        # Deleting model 'Guess'
        db.delete_table(u'main_guess')

        # Deleting model 'Announcement'
        db.delete_table(u'main_announcement')

        # Removing M2M table for field teams_read on 'Announcement'
        db.delete_table('main_announcement_teams_read')

        # Deleting model 'Message'
        db.delete_table(u'main_message')


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
        u'main.message': {
            'Meta': {'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Team']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
        u'track.pagehit': {
            'Meta': {'object_name': 'PageHit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['main']