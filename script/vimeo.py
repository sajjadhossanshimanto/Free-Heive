#%%
import re
import requests
import json


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
        self.content = None

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
            return self.content
        
        url = self.embed_link()
        r = requests.request("GET", url, headers=headers)
        r = re.search(
            r" var config = (.+?); if \(!config",
            r.text
        ).group(1)
        
        config = json.loads(r)
        self.content = {
            i['quality']:i
            for i in config['request']["files"]['progressive']
        }
        return self.content

    def download(self, quality):
        pass


if __name__=='__main__':
    vimeo_id = 622338938
    p=Vimeo(vimeo_id)
    print(p.player())


