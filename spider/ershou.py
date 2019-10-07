import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from bs4 import BeautifulSoup
import re


def download(url, user_agent='wsap', num_retries=2):
    print('Downloading: ', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            # 5xx错误
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries=num_retries - 1)
    return html


def num_ershou_in(area):
    url = 'https://hz.lianjia.com/ershoufang/' + area + '/'
    html = download(url)
    soup = BeautifulSoup(html, 'html.parser')
    num = soup.find(attrs={'class': 'total fl'}).text
    num = int(re.findall(r'\d+', num)[0])
    return num


def num_ershou():
    areas = ['xihu', 'qiantangxinqu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'binjiang',
             'yuhang', 'xiaoshan', 'chunan1', 'fuyang', 'linan']
    nums = []
    for area in areas:
        nums.append(num_ershou_in(area))
    return dict(zip(areas, nums))


print(num_ershou())
