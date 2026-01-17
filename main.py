import feedparser
import json
import os
import re 
from datetime import datetime
from time import mktime 
rss_url = "http://feeds.bbci.co.uk/turkce/rss.xml"
VARSAYILAN_RESIM = "https://news.bbcimg.co.uk/news/special/2015/newsspec_10857/bbc_news_logo.png?cb=1"
feedparser.USER_AGENT = "HaberBotu/1.0 (Mobile App Data Fetcher)"
def html_etiketlerini_temizle(metin):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', metin)
def resim_bul(haber_girdisi):
    if 'media_thumbnail' in haber_girdisi and len(haber_girdisi.media_thumbnail) > 0:
        return haber_girdisi.media_thumbnail[0]['url']
    if 'media_content' in haber_girdisi and len(haber_girdisi.media_content) > 0:
        return haber_girdisi.media_content[0]['url']
    if 'links' in haber_girdisi:
        for link in haber_girdisi.links:
            if 'image' in link.type:
                return link.href
    return VARSAYILAN_RESIM
veri = feedparser.parse(rss_url)
haber_listesi = []
for haber in veri.entries:
    if "Abone olmak için" in haber.title:
        continue
    tarih_objesi = datetime.fromtimestamp(mktime(haber.published_parsed))
    duzenli_tarih = tarih_objesi.strftime('%Y-%m-%d %H:%M:%S')
    temiz_ozet = html_etiketlerini_temizle(haber.summary)
    gecici_sozluk = {
        "baslik": haber.title,
        "link": haber.link,
        "ozet": temiz_ozet,
        "tarih": duzenli_tarih, 
        "resim": resim_bul(haber) 
    }
    haber_listesi.append(gecici_sozluk)
with open('haberler.json', 'w', encoding='utf-8') as dosya:
    json.dump(haber_listesi, dosya, ensure_ascii=False, indent=4)
