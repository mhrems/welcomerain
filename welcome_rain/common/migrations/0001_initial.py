# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'vo_UserProfile'
        db.create_table('common_vo_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
            ('grahp_realtime_interval', self.gf('django.db.models.fields.IntegerField')(default=30000)),
        ))
        db.send_create_signal('common', ['vo_UserProfile'])

        # Adding model 'vo_Chart'
        db.create_table('common_vo_chart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cluster', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datasource', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['vo_Chart'])

        # Adding model 'vo_Host'
        db.create_table('common_vo_host', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['vo_Host'])

        # Adding model 'vo_Favorite'
        db.create_table('common_vo_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('grid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cluster', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datasource', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['vo_Favorite'])

        # Adding model 'vo_Server'
        db.create_table('common_vo_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('server_version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('server_userid', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('server_password', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('gmond_install_flag', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('plugin_lists', self.gf('django.db.models.fields.TextField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('common', ['vo_Server'])

        # Adding model 'vo_Progress'
        db.create_table('common_vo_progress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.vo_Server'])),
            ('server_ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['vo_Progress'])

        # Adding model 'vo_Plugin'
        db.create_table('common_vo_plugin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('plugin_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('conf_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('script_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('common', ['vo_Plugin'])

        # Adding model 'vo_Alert'
        db.create_table('common_vo_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.vo_Plugin'])),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('threhhold_vale', self.gf('django.db.models.fields.IntegerField')()),
            ('descriptions', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('common', ['vo_Alert'])

        # Adding model 'vo_AlertHistory'
        db.create_table('common_vo_alerthistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.vo_Server'])),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.vo_Plugin'])),
            ('alert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.vo_Alert'])),
            ('server_ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descriptions', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('common', ['vo_AlertHistory'])


    def backwards(self, orm):
        # Deleting model 'vo_UserProfile'
        db.delete_table('common_vo_userprofile')

        # Deleting model 'vo_Chart'
        db.delete_table('common_vo_chart')

        # Deleting model 'vo_Host'
        db.delete_table('common_vo_host')

        # Deleting model 'vo_Favorite'
        db.delete_table('common_vo_favorite')

        # Deleting model 'vo_Server'
        db.delete_table('common_vo_server')

        # Deleting model 'vo_Progress'
        db.delete_table('common_vo_progress')

        # Deleting model 'vo_Plugin'
        db.delete_table('common_vo_plugin')

        # Deleting model 'vo_Alert'
        db.delete_table('common_vo_alert')

        # Deleting model 'vo_AlertHistory'
        db.delete_table('common_vo_alerthistory')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.vo_alert': {
            'Meta': {'object_name': 'vo_Alert'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'descriptions': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.vo_Plugin']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'threhhold_vale': ('django.db.models.fields.IntegerField', [], {}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_alerthistory': {
            'Meta': {'object_name': 'vo_AlertHistory'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.vo_Alert']"}),
            'descriptions': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.vo_Plugin']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.vo_Server']"}),
            'server_ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.vo_chart': {
            'Meta': {'object_name': 'vo_Chart'},
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'datasource': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_favorite': {
            'Meta': {'object_name': 'vo_Favorite'},
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'datasource': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'grid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_host': {
            'Meta': {'object_name': 'vo_Host'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_plugin': {
            'Meta': {'object_name': 'vo_Plugin'},
            'conf_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plugin_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'script_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.vo_progress': {
            'Meta': {'object_name': 'vo_Progress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.vo_Server']"}),
            'server_ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_server': {
            'Meta': {'object_name': 'vo_Server'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'gmond_install_flag': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'plugin_lists': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'server_password': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'server_userid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'server_version': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.vo_userprofile': {
            'Meta': {'object_name': 'vo_UserProfile'},
            'grahp_realtime_interval': ('django.db.models.fields.IntegerField', [], {'default': '30000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']