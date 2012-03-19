from django.db import models
import settings
from PIL import Image
import os
from django.db.models import Max,Sum
import urllib2
from django.core.files.base import File
import uuid
from django.core.files.temp import NamedTemporaryFile
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.dispatch import receiver

# In your settings.py, set SPRITE_PATH or SPRITE_ITEM_PATH to 
# override the upload_to path for Sprites and SpriteItems, which
# is appended to MEDIA_ROOT when saving files to determine the
# full path

SPRITE_PATH=getattr(settings, 'SPRITE_PATH', 'sprites')
SPRITE_ITEM_PATH=getattr(settings, 'SPRITE_ITEM_PATH', 'sprite_items')

EXTENSIONS = {
    'JPEG':'jpg',
    'PNG':'png',
}

class Sprite(models.Model):
    image=models.ImageField(upload_to=SPRITE_PATH,null=True,blank=True)
    extension=models.CharField(max_length=4,default='jpg')
    ready=models.BooleanField(default=True)
    
    def build(self):
        if not self.ready:
            return
        self.ready=False
        self.save()
        img_data = {}
        img_data["items"] = self.spriteitem_set.filter(height__isnull=False)
        img_data["sprite"] = {}
        img_sprite = Image.new("RGBA", (img_data["items"].aggregate(Max('width'))['width__max'],img_data["items"].aggregate(Sum('height'))['height__sum']))
        item_count = len(img_data["items"])
        item_loop = 0
        item_top = 0
        print 'build called with %i images'%(item_count)
        
        for obj_item in img_data["items"]:
            if obj_item.height is not None:
                pasteBox = (0, item_top, obj_item.width, item_top+obj_item.height)
                obj_item.top=item_top
                imgItem = Image.open(obj_item.image)
                self.extension=EXTENSIONS[imgItem.format]
                obj_item.save(build=False)
                item_top += obj_item.height
                img_sprite.paste(imgItem, pasteBox)
                imgItem = None
                item_loop += 1
                
        self.save()

        img_temp = NamedTemporaryFile(suffix='.'+self.extension)
        filename=uuid.uuid1().hex + '.' + self.extension
        img_sprite.save(img_temp)
        img_sprite = None
        self.ready=True
        self.image.save(filename,File(img_temp))
    
    @classmethod
    def create_from_urls(cls,urls):
        self=cls.objects.create(ready=False)
        for url in urls:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(url).read())
            filename=uuid.uuid1().hex
            item=SpriteItem(sprite=self)
            item.image.save(filename,File(img_temp))
            item.save(build=False)
        self.ready=True
        self.save()
        self.build()
        return self
    
    @classmethod
    def create_from_local_files(cls,filenames):
        self=cls.objects.create(ready=False)
        for filename in filenames:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(open(filename,'r').read())
            item=SpriteItem(sprite=self)
            item.image.save(filename,File(img_temp))
            item.save(build=False)
        self.ready=True
        self.save()
        self.build()
        return self
            

    
class SpriteItem(models.Model):
    sprite=models.ForeignKey(Sprite)
    image = models.ImageField(upload_to=SPRITE_ITEM_PATH,width_field='width',height_field='height')
    top = models.IntegerField(null=True,blank=True)
    width=models.IntegerField(null=True,blank=True)
    height=models.IntegerField(null=True,blank=True)
    css_id=models.CharField(max_length=127,null=True,default=None,blank=True)
    css_class=models.CharField(max_length=127,default='',blank=True)
    internal_html=models.TextField(default='',blank=True)
    
    def save(self,build=True,*args,**kwargs):
        super(SpriteItem,self).save(*args,**kwargs)
        if build:
            self.sprite.build()
    
    @property
    def style(self):
        return "display:block;background:url(%s) no-repeat; background-position:0px -%spx;width:%spx;height:%spx;"%(self.sprite.image.url,self.top,self.width,self.height)
    @property
    def css(self):
        if self.css_id is None or self.css_id == '':
            raise Exception("Can't generate CSS without a css_id value.")
        return "#%s {%s}"%(self.css_id,self.style)
    @property
    def tag_with_style(self):
        try:
            file=self.image.file
        except:
            return None
        id=""
        if self.css_id is not None:
            id=' id="%s"'%(self.css_id,)
        return mark_safe('<span%s style="%s" class="%s">%s&nbsp;</span>'%(id,self.style,self.css_class,self.internal_html))
    
@receiver(pre_save, sender=SpriteItem)
def spriteitem_presave(sender, **kwargs):
    instance=kwargs['instance']
    try:
        sprite=instance.sprite
    except:
        instance.sprite=Sprite.objects.create()

