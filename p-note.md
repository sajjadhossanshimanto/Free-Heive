1. master.json
- all the segment id list
2. type document 
- all the need 
3. what is firebase token 


4. oembed.json 
  - fetch info only ussing vidmeo id
```curl
curl 'https://vimeo.com/api/oembed.json?url=https%3A%2F%2Fvimeo.com%2F622338938&url=https%3A%2F%2Fvimeo.com%2F622338938&autoplay=true&muted=false&loop=false&playsinline=false&controls=true&autopause=false&byline=false&portrait=false&title=false&quality=auto' \
  -H 'Connection: keep-alive' \
  -H 'sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="98"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Accept: */*' \
  -H 'Origin: https://eduhive.com.bd' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://eduhive.com.bd/' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  --compressed
```
- we get different info but the important one is the embeded html

4. get the link with presifique headers 
```
Connection:keep-alive
sec-ch-ua:"(Not(A:Brand";v="8", "Chromium";v="98"
sec-ch-ua-mobile:?0
sec-ch-ua-platform:"Linux"
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site:cross-site
Sec-Fetch-Mode:navigate
Sec-Fetch-Dest:iframe
Referer:https://eduhive.com.bd/
Accept-Language:en-US,en;q=0.9
```

---
## subject -> chapter -> sub chapter -> topi -> content
---
### 1. list subject
- https://api.eduhive.com.bd/subjects?status=active&videoEnabled=true&className=hsc&group[]=all&group[]=science
- also includes chapter id
```
curl 'https://api.eduhive.com.bd/subjects?status=active&videoEnabled=true&className=hsc&group\[\]=all&group\[\]=science' \
  -H 'authority: api.eduhive.com.bd' \
  -H 'sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="98"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'origin: https://eduhive.com.bd' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://eduhive.com.bd/' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cookie: _fbp=fb.2.1657192628729.859043117; _fw_crm_v=8674f72e-55e5-48b1-9249-437489be9ead; _ga=GA1.3.2064830738.1657192750; _gid=GA1.3.1448756031.1661677447; eduhive_techhive=s%3AmgNHpi_znA2nc2jKkNdgrhmmFu5IpzxP.%2FhM00bhAaJE6GRozB35JVGvKF3doptCe8ToShVoIFyM; _gat=1' \
  -H 'if-none-match: W/"480a-+tmf8rIxa6kU7BDMGvsWWpNMVg4"' \
  --compressed
```

### 2. list chapter 
- https://api.eduhive.com.bd/subjects/60b7322ae9358a41edd165c7
```
curl 'https://api.eduhive.com.bd/subjects/60b7322ae9358a41edd165c7' \
  -H 'authority: api.eduhive.com.bd' \
  -H 'sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="98"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'origin: https://eduhive.com.bd' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://eduhive.com.bd/' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cookie: _fbp=fb.2.1657192628729.859043117; _fw_crm_v=8674f72e-55e5-48b1-9249-437489be9ead; _ga=GA1.3.2064830738.1657192750; _gid=GA1.3.1448756031.1661677447; eduhive_techhive=s%3AmgNHpi_znA2nc2jKkNdgrhmmFu5IpzxP.%2FhM00bhAaJE6GRozB35JVGvKF3doptCe8ToShVoIFyM; _gat=1' \
  -H 'if-none-match: W/"7dd-IazuLt8lDhBov3pohjdEZWNv8ps"' \
  --compressed
```

2. original course `list sub chapters`
- https://api.eduhive.com.bd/get-original-course-details?subject=60b7322ae9358a41edd165c7&chapterId=60b7322ae9358a41edd165c8
- this also includes content list 
```
curl 'https://api.eduhive.com.bd/get-original-course-details?subject=60b7322ae9358a41edd165c7&chapterId=60b7322ae9358a41edd165c8' \
  -H 'authority: api.eduhive.com.bd' \
  -H 'sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="98"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'origin: https://eduhive.com.bd' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://eduhive.com.bd/' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cookie: _fbp=fb.2.1657192628729.859043117; _fw_crm_v=8674f72e-55e5-48b1-9249-437489be9ead; _ga=GA1.3.2064830738.1657192750; _gid=GA1.3.1448756031.1661677447; eduhive_techhive=s%3AmgNHpi_znA2nc2jKkNdgrhmmFu5IpzxP.%2FhM00bhAaJE6GRozB35JVGvKF3doptCe8ToShVoIFyM' \
  -H 'if-none-match: W/"2222-I/LkNol61sUdKE884A8eZc721co"' \
  --compressed
```



5. get content list under a section 
- the main important thing is the cookie 
- each chapter is consedered as a `course`  ( a set of sun-chapters )
- and course have differect section 
- under whitch
- https://api.eduhive.com.bd/courses/615adbca12de8a3ceaddcdcf/sections/615adbca12de8a3ceaddcdd0
```
authority:api.eduhive.com.bd
sec-ch-ua:"(Not(A:Brand";v="8", "Chromium";v="98"
accept:application/json, text/plain, */*
sec-ch-ua-mobile:?0
user-agent:Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36
sec-ch-ua-platform:"Linux"
origin:https://eduhive.com.bd
sec-fetch-site:same-site
sec-fetch-mode:cors
sec-fetch-dest:empty
referer:https://eduhive.com.bd/
accept-language:en-US,en;q=0.9
cookie:_fbp=fb.2.1657192628729.859043117; _fw_crm_v=8674f72e-55e5-48b1-9249-437489be9ead; _ga=GA1.3.2064830738.1657192750; _gid=GA1.3.1448756031.1661677447; _gat=1; eduhive_techhive=s%3ApR_L6syqSOaX28a-wZ2wSHvcYmVI5sZ-.NsBuKEUvvJ2NxiJ3L6eSQo7XfwmUSMO5%2FD4XF3nUxQg
if-none-match:W/"2a7a-M358TOWeso4gC4SOb0Pr8vLNGbw"
```


