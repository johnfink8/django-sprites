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
from hashlib import md5

# In your settings.py, set SPRITE_PATH or SPRITE_ITEM_PATH to 
# override the upload_to path for Sprites and SpriteItems, which
# is appended to MEDIA_ROOT when saving files to determine the
# full path

SPRITE_PATH=getattr(settings, 'SPRITE_PATH', 'sprites')
SPRITE_ITEM_PATH=getattr(settings, 'SPRITE_ITEM_PATH', 'sprite_items')

EXTENSIONS = {
    'JPEG':'jpg',
    'PNG':'png',
    'GIF':'gif',
}

class Sprite(models.Model):
    image=models.ImageField(upload_to=SPRITE_PATH,null=True,blank=True)
    extension=models.CharField(max_length=4,default='jpg')
    ready=models.BooleanField(default=True)
    location_hash=models.CharField(max_length=127,null=True,blank=True,unique=True)
    
    def build(self):
        if not self.ready:
            return
        self.ready=False
        self.save()
        try:
            self.image.delete()
        except:
            pass
        spriteitems = self.spriteitem_set.filter(height__isnull=False)
        if len(spriteitems) == 0:
            self.ready=True
            self.save()
            return 
        img_sprite = Image.new("RGBA", (spriteitems.aggregate(Max('width'))['width__max'],spriteitems.aggregate(Sum('height'))['height__sum']))
        item_loop = 0
        item_top = 0
        
        for obj_item in spriteitems:
            if obj_item.height is not None:
                pasteBox = (0, item_top, obj_item.width, item_top+obj_item.height)
                obj_item.top=item_top
                imgItem = Image.open(obj_item.image)
                self.extension=EXTENSIONS[imgItem.format]
                obj_item.save()
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
        try:
            self.image.delete()
        except:
            pass
        self.image.save(filename,File(img_temp))
    
    @classmethod
    def create_from_urls(cls,urls,location=None):
        if location is not None:
            try:
                self=cls.objects.get(location_hash=md5(location).hexdigest())
                self.ready=False
                self.save()
            except:
                self=cls.objects.create(ready=False,location_hash=md5(location).hexdigest())
        else:
            self=cls.objects.create(ready=False,location_hash=uuid.uuid1().hex)
        rebuild=[self]
        for url in urls:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(url).read())
            filename=uuid.uuid1().hex
            try:
                item=SpriteItem.objects.get(origin_hash=md5(url).hexdigest())
            except:
                item=SpriteItem(sprite=self,origin_hash=md5(url).hexdigest())
            try:
                item.image.delete()
            except:
                pass
            rebuild.append(item.sprite)
            item.sprite=self
            item.image.save(filename,File(img_temp))
            item.save()
        rebuild_set=set(rebuild)
        rebuild_set.remove(self)
        for sprite in rebuild_set:
            sprite.ready=True
            sprite.save()
            sprite.build()
        self.ready=True
        self.save()
        self.build()
        return self
    
    @classmethod
    def create_from_local_files(cls,filenames):
        self=cls.objects.create(ready=False,location_hash=uuid.uuid1().hex)
        for filename in filenames:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(open(filename,'r').read())
            item=SpriteItem(sprite=self,origin_hash=md5(filename).hexdigest())
            try:
                item.image.delete()
            except:
                pass
            item.sprite=self
            item.image.save(filename,File(img_temp))
            item.save()
        self.ready=True
        self.save()
        self.build()
        return self
    
    def create_thumbnails(self,width=64,height=64):
        location_hash = self.location_hash+ 'thumbsprite'
        try:
            thumbsprite = Sprite.objects.get(location_hash=location_hash)
            thumbsprite.ready=False
            thumbsprite.save()
        except:
            thumbsprite=Sprite.objects.create(location_hash=location_hash,ready=False)
        for img in self.spriteitem_set.filter(width__isnull=False):
            thumb_image=img.make_thumbnail(width,height)
            img_temp = NamedTemporaryFile(suffix='.'+EXTENSIONS[thumb_image.format])
            thumb_image.save(img_temp,thumb_image.format)
            origin_hash=img.origin_hash+'thumb'
            filename=uuid.uuid1().hex + '.'+EXTENSIONS[thumb_image.format]
            try:
                thumbspriteitem=SpriteItem.objects.get(origin_hash=origin_hash)
                thumbspriteitem.sprite=thumbsprite
            except:
                thumbspriteitem=SpriteItem(origin_hash=origin_hash,sprite=thumbsprite)
            try:
                thumspriteitem.image.delete()
            except:
                pass
            thumbspriteitem.image.save(filename,File(img_temp))
            img.thumbnail = thumbspriteitem
            img.save()
        thumbsprite.ready=True
        thumbsprite.save()
        thumbsprite.build()
        return thumbsprite
            

    
class SpriteItem(models.Model):
    sprite=models.ForeignKey(Sprite)
    image = models.ImageField(upload_to=SPRITE_ITEM_PATH,width_field='width',height_field='height')
    top = models.IntegerField(null=True,blank=True)
    width=models.IntegerField(null=True,blank=True)
    height=models.IntegerField(null=True,blank=True)
    css_id=models.CharField(max_length=127,null=True,default=None,blank=True)
    css_class=models.CharField(max_length=127,default='',blank=True)
    internal_html=models.TextField(default='',blank=True)
    origin_hash=models.CharField(max_length=127,null=True,blank=True,unique=True)
    thumbnail=models.OneToOneField('self',related_name='fullsize',null=True,blank=True)
    
    def make_thumbnail(self,width=64,height=64):
        im=Image.open(self.image)
        image_format=im.format
        im.thumbnail((width,height),Image.ANTIALIAS)
        return im
    
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

