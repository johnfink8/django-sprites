# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Sprite.extension'
        db.add_column('sprites_sprite', 'extension', self.gf('django.db.models.fields.CharField')(default='jpg', max_length=4), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Sprite.extension'
        db.delete_column('sprites_sprite', 'extension')


    models = {
        'sprites.sprite': {
            'Meta': {'object_name': 'Sprite'},
            'extension': ('django.db.models.fields.CharField', [], {'default': "'jpg'", 'max_length': '4'}),
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
