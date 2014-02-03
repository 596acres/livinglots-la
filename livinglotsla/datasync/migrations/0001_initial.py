# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataSource'
        db.create_table(u'datasync_datasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('healthy', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('synchronizer_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['external_data_sync.SynchronizerRecord'], null=True, blank=True)),
            ('synchronize_in_progress', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('synchronize_frequency', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('next_synchronize', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_synchronized', self.gf('django.db.models.fields.DateTimeField')()),
            ('batch_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'datasync', ['DataSource'])


    def backwards(self, orm):
        # Deleting model 'DataSource'
        db.delete_table(u'datasync_datasource')


    models = {
        u'datasync.datasource': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'DataSource'},
            'batch_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'healthy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synchronized': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_synchronize': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'synchronize_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'synchronize_in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synchronizer_record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['external_data_sync.SynchronizerRecord']", 'null': 'True', 'blank': 'True'})
        },
        u'external_data_sync.synchronizerrecord': {
            'Meta': {'object_name': 'SynchronizerRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'synchronizer_class': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'synchronizer_module': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['datasync']