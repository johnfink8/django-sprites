try:
    from BeautifulSoup import BeautifulSoup,Tag
except:
    raise Exception('Sorry, the django-sprites middleware relies on BeautifulSoup.  Install it with `pip install beautifulsoup` or similar')

import urllib2,urlparse
import settings
from sprites.models import Sprite,SpriteItem
from hashlib import md5

SPRITE_REPLACE_CSS_CLASS = getattr(settings,'SPRITE_REPLACE_CSS_CLASS','sprite_img')

class SpriteReplaceByClass(object):

    def process_response(self, request, response):
        html=response.content
        location=request.build_absolute_uri()
        soup=BeautifulSoup(html)
        to_process=[]
        for img in soup.findAll('img',SPRITE_REPLACE_CSS_CLASS):
            try:
                spriteitem=SpriteItem.objects.get(origin_hash=md5(urlparse.urljoin(location,img['src'])).hexdigest())
                tag=Tag(soup,'div',[("style",spriteitem.style)])
                img.replaceWith(tag)
            except:
                to_process.append(img)
        if len(to_process)>0:
            Sprite.create_from_urls([urlparse.urljoin(location,img['src']) for img in to_process],location=location)
        for img in soup.findAll('img',SPRITE_REPLACE_CSS_CLASS):
            spriteitem=SpriteItem.objects.get(origin_hash=md5(urlparse.urljoin(location,img['src'])).hexdigest())
            img.replaceWith(spriteitem.tag_with_style)
        response.content = str(soup)
        return response

