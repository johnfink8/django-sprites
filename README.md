django-sprites
====================
 ...is a Django app with two bundled models that handle 
Sprites and their associated SpriteItems.


* A Sprite is a combined image, consisting of one or more 
  SpriteItems, each of which is an image intended to be used as an 
  image background for an HTML element.

* Combining these background images into a single image can 
  enormously save on load times.  There is a lot of time loss in 
  sequentially requesting multiple images from the same server, and 
  only 2-4 can be requested simultaneously.  So if you have 20 or 
  30, that could add hundreds or thousands of milliseconds to your 
  overall page load.

* Each SpriteItem contains the info actually relevant to your site 
  design, like the image itself, dimensions (which are calculated),
  HTML attributes like class and id, and these are used by the 
  model methods to generate styling, full CSS lines, and/or an HTML
  tag source with the relevant image behind it and any input HTML 
  inside.

Requirements:
---------------------

*  PIL, with libjpeg support

*  Django (obviously)

*  Uuid

*  urllib2
    
Setup:
---------------------

*  pip install django-sprites

*  Add to your settings.py INSTALLED_APPS:
'sprites',

*  Also in settings.py:

    `MEDIA_ROOT = 'path/to/your/actual/intended/media/root'`

    This will be used along with the relative paths in the next 
    config items to determine save locations for images.


    `MEDIA_URL = 'http://myserver.mydomain.com/media'`

    This is used by Django to generate URLs for ImageFiles, in
    addition to the relative paths below.  Fully-qualified path is
    not actually required, but it's better to make it fully-
    qualified here so that you can use the HTML on any domain, not
    just the same as your Django app.

*  Also in settings.py (optional):

    `SPRITE_PATH = '<some relative path to store sprites>'`

    `SPRITE_ITEM_PATH = '<another relative path>'`

    These default to 'sprites' and 'sprite_items', respectively.
    
Usage:
---------------------
    
*  Bulk load images into a sprite by calling:

    `sprite=Sprite.create_from_urls(['http://path.to/first.jpg',`

    'http://path.to/second.jpg'...])`

    or...

    `sprite=Sprite.create_from_local_files(['/path/to/first/file',`

    `'/path/to/second/file'])`


*  SpriteItem properties
  - `spriteitem.style` - outputs CSS style directives, without 
  specifying it with a selector
  i.e.: "display:block; background: url(whatever); etc.;"
   
  - `spriteitem.css` - outputs the same style directives, with a 
  selector based on spriteitem.css_id
  i.e.: `"#myimage {display:block; etc.;}"`
   
  - `spriteitem.tag_with_style` - ouputs a safe-marked (ready to 
  use in a template) HTML span tag with embedded style attrib,
  including any internal HTML given by `spriteitem.internal_html`
    
  - `spriteitem.thumbnail` - If created, this is a OneToOne that 
  links to another SpriteItem, which by convention (but not 
  as a requirement) is a thumbnail of spriteitem.
   
  - `spriteitem.make_thumbnail(width=64,height=64)` - return a 
  PIL.Image copy of spriteitem.image of size width,height.  
  Aspect ratio is preserved, so size may not match exactly.
    
      This is used by `sprite.create_thumbnails(width,height)`, 
      which generates new spriteitems, associates those 
      spriteitems with those of sprite as their thumbnails, and 
      returns the newly created sprite.
    
  - `spriteitem.sprite.build()` should be called after making 
  changes to a sprite.  The methods internal to this app handle
  this sanely, but if you make changes you'll have to determine
  when and how often to re-build your sprites.  I'd suggest 
  building a set of sprites to build first, so you don't 

*  Middleware

    Adding `'sprites.middleware.SpriteReplaceByClass',` to 
`MIDDLEWARE_CLASSES` enables the replacement of IMG elements
with styled DIVs.  The SRC of the IMG will become the (sprite)
background of the DIV.  The DOM translation isn't perfect 
going from IMG to DIV, so be careful with this.  By default, 
IMGs with css class `'sprite_img'` will be replaced.  The class 
can be changed with `SPRITE_REPLACE_CSS_CLASS` in settings.py.

    Note:  The middleware relies on BeautifulSoup. Because one 
does not simply regex into HTML.  It is folly.

         
*  Other than the middleware, this isn't really meant to be 
used by itself.  Ideally, you'll have some kind of model that 
you'll ForeignKey relate to SpriteItem, like:

&nbsp;

    class SiteElement(models.Model):
        spriteitem=models.ForeignKey(SpriteItem)
        link=models.CharField(max_length=255,null=True,blank=True)
        
        def get_tag(self):
            if self.link is not None:
                return '<a href="%s">%s</a>'%(
                    self.link,self.spriteitem.tag_with_style)
            return self.spriteitem.tag_with_style`
    
*  Should support django-storages backend extensions.  Tested 
working with S3BotoStorage, at least.

*  Detects and sets image filetype based on the PIL-detected format 
of the component SpriteItem images.  Ultimately it uses the last
SpriteItem attached to the Sprite to set the format.


ToDo:
---------------------
    
*  Make it split up by image format, maybe.  Mixing JPEGs into a 
sprite detected as GIF looks atrocious.
       
*  Write tests
    
*  Finish ToDo list
    
    
