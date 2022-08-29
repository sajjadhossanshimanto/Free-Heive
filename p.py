#%%
import re
import requests
import json
from bs4 import BeautifulSoup


#%%
url = "https://vimeo.com/api/oembed.json?url=https%3A%2F%2Fvimeo.com%2F622338938"
url = "https://vimeo.com/api/oembed.json?"

vimeo_id = 622338938

headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
  'sec-ch-ua-platform': '"Linux"',
  'Accept': '*/*',
  'Origin': 'https://eduhive.com.bd',
  'Referer': 'https://eduhive.com.bd/',
  'Accept-Language': 'en-US,en;q=0.9',
}

print(response.json())

class EduHive:
    def __init__(self) -> None:
        pass

    # def 

class Vimeo:
    embed_url = "https://vimeo.com/api/oembed.json?"

    def __init__(self, vimeo_id) -> None:
        self.vimeo_id = vimeo_id

    def embed_link(self):
        payload={
            "url": f"https://vimeo.com/{video_id}"
        }
        r = requests.request("GET", self.embed_url, headers=headers, params=payload)
        
        url = re.search(
            r'src="([^"]+)"',
            r.json()['html'] 
        ).group(1)
        return url

    def player(self):
        pass

