# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DaysAfterAddedMailing'
        db.create_table(u'mailings_daysafteraddedmailing', (
            (u'mailing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['livinglots_mailings.Mailing'], unique=True, primary_key=True)),
            ('days_after_added', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mailings', ['DaysAfterAddedMailing'])


    def backwards(self, orm):
        # Deleting model 'DaysAfterAddedMailing'
        db.delete_table(u'mailings_daysafteraddedmailing')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'livinglots_mailings.mailing': {
            'Meta': {'object_name': 'Mailing'},
            'duplicate_handling': ('django.db.models.fields.CharField', [], {'default': "'each'", 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'target_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contenttypes.ContentType']", 'symmetrical': 'False'}),
            'text_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'mailings.daysafteraddedmailing': {
            'Meta': {'object_name': 'DaysAfterAddedMailing', '_ormbases': [u'livinglots_mailings.Mailing']},
            'days_after_added': ('django.db.models.fields.IntegerField', [], {}),
            u'mailing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['livinglots_mailings.Mailing']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['mailings']