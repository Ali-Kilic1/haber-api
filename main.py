import feedparser
import json
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
    bulunan_resim = VARSAYILAN_RESIM
    if 'media_thumbnail' in haber_girdisi and len(haber_girdisi.media_thumbnail) > 0:
        bulunan_resim = haber_girdisi.media_thumbnail[0]['url']
    elif 'media_content' in haber_girdisi and len(haber_girdisi.media_content) > 0:
        bulunan_resim = haber_girdisi.media_content[0]['url']
    elif 'links' in haber_girdisi:
        for link in haber_girdisi.links:
            if 'image' in link.type:
                bulunan_resim = link.href
                break
    if "bbci.co.uk" in bulunan_resim:
        if "/240/" in bulunan_resim:
            bulunan_resim = bulunan_resim.replace("/240/", "/1024/")
        elif "/144/" in bulunan_resim:
            bulunan_resim = bulunan_resim.replace("/144/", "/1024/")
        elif "/320/" in bulunan_resim:
            bulunan_resim = bulunan_resim.replace("/320/", "/1024/")
    return bulunan_resim
veri = feedparser.parse(rss_url)
haber_listesi = []
for haber in veri.entries:
    
    if "Abone olmak için" in haber.title:
        continue
    tarih_objesi = datetime.fromtimestamp(mktime(haber.published_parsed))
    duzenli_tarih = tarih_objesi.strftime('%Y-%m-%d %H:%M:%S')
    temiz_ozet = html_etiketlerini_temizle(haber.summary)
    hd_resim = resim_bul(haber)
    gecici_sozluk = {
        "baslik": haber.title,
        "link": haber.link,
        "ozet": temiz_ozet,
        "tarih": duzenli_tarih, 
        "resim": hd_resim 
    }
    haber_listesi.append(gecici_sozluk)
with open('haberler.json', 'w', encoding='utf-8') as dosya:
    json.dump(haber_listesi, dosya, ensure_ascii=False, indent=4)
