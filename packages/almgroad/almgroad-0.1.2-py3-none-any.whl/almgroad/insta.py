import random
import json,asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup

def random_ip():
    ips = ['46.227.123.', '37.110.212.', '46.255.69.', '62.209.128.', '37.110.214.', '31.135.209.', '37.110.213.']
    prefix = random.choice(ips)
    return prefix + str(random.randint(1, 255))

async def instagram(url):
    result = []
    data = {'q': url, 'vt': 'home'}
    headers = {
        'origin': 'https://snapinsta.io',
        'referer': 'https://snapinsta.io/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'X-Forwarded-For': random_ip(),
        'X-Client-IP': random_ip(),
        'X-Real-IP': random_ip(),
        'X-Forwarded-Host': 'snapinsta.io'
    }
    base_url = 'https://snapinsta.io/api/ajaxSearch'
    async with ClientSession() as session:
        async with session.post(base_url, data=data, headers=headers) as response:
            jsonn = json.loads(await response.text())
            
            if jsonn['status'] == 'ok':
                data = jsonn['data']
                soup = BeautifulSoup(data, 'html.parser')
                for i in soup.find_all('div', class_='download-items__btn'):
                    url = i.find('a')['href']
                    result.append(url)
                tt = [jj for jj in result]
                return result 
            else:
                return "حدث خطأ : تاكد من الرابط بشكل صحيح"




