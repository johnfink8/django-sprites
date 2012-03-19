# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Sprite'
        db.create_table('sprites_sprite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('sprites', ['Sprite'])

        # Adding model 'SpriteItem'
        db.create_table('sprites_spriteitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sprite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sprites.Sprite'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('top', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('css_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=127, null=True, blank=True)),
            ('css_class', self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True)),
            ('internal_html', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('sprites', ['SpriteItem'])


    def backwards(self, orm):
        
        # Deleting model 'Sprite'
        db.delete_table('sprites_sprite')

        # Deleting model 'SpriteItem'
        db.delete_table('sprites_spriteitem')


    models = {
        'sprites.sprite': {
            'Meta': {'object_name': 'Sprite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'sprites.spriteitem': {
            'Meta': {'object_name': 'SpriteItem'},
            'css_class': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '127', 'blank': 'True'}),
            'css_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'internal_html': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sprite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sprites.Sprite']"}),
            'top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sprites']
