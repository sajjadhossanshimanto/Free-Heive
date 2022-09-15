#%%
import re
from time import time
import requests
import json
from urllib.parse import urlparse, unquote

#%%
# url = "https://vimeo.com/api/oembed.json?url=https%3A%2F%2Fvimeo.com%2F622338938"
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
  'sec-ch-ua-platform': '"Linux"',
  'Accept': '*/*',
  'Origin': 'https://eduhive.com.bd',
  'Referer': 'https://eduhive.com.bd/',
  'Accept-Language': 'en-US,en;q=0.9',
}

cache={}# TODO; cache vimeo_id and h tag
class Vimeo:
    embed_url = "https://vimeo.com/api/oembed.json"
    # TODO: we can also save h tag and then no need to fetch from embed link

    def __init__(self, vimeo_id) -> None:
        self.vimeo_id = int(vimeo_id)
        self.content: dict = None
        if cache.get(self.vimeo_id):
            self.content = cache[self.vimeo_id]

    def embed_link(self):
        payload={
            "url": f"https://vimeo.com/{self.vimeo_id}"
        }
        r = requests.request("GET", self.embed_url, headers=headers, params=payload)
        
        url = re.search(
            r'src="([^"]+)"',
            r.json()['html'] 
        ).group(1)
        return url

    def get_quality(self):
        if self.content:
            for k in self.content: break
            url = self.content[k]
            exp = re.search('exp=(\d+)', url).group(1)
            if int(exp)>time():
                return self.content
        
        url = self.embed_link()
        r = requests.request("GET", url, headers=headers)
        r = re.search(
            r" var config = (.+?); if \(!config",
            r.text
        ).group(1)
        
        config = json.loads(r)
        self.content = {
            i['quality']:i['url']
            for i in config['request']["files"]['progressive']
        }
        cache[self.vimeo_id]=self.content
        return self.content

    def refresh_link(self):
        ''' forcefully refresh links '''
        self.content.clear()
        self.get_quality()

    def download(self, quality):
        pass


if __name__=='__main__':
    vimeo_id = 622338938
    p=Vimeo(vimeo_id)
    print(p.player())


{
    1:1,
    2:2,
    3:3
}.popitem()

url="https://vod-progressive.akamaized.net/exp=1661480862~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4467%2F24%2F622338938%2F2880029581.mp4~hmac=fb6a2b60a8276046d8a9ae6dc046ba69deed826a43abe50481f3b08036c36607/vimeo-prod-skyfire-std-us/01/4467/24/622338938/2880029581.mp4"

# %%
