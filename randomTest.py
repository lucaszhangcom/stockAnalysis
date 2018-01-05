# -*- coding: UTF-8 -*-
# 一周交易备忘

import urllib
import urllib2
import sys
import time
from bs4 import BeautifulSoup

from dao import dataSource

datasource = dataSource.DataSource()

type = sys.getfilesystemencoding()

proxies = [{"https": "106.14.241.155:80"}, {"http": "114.44.179.194:8080"}, {"http": "37.17.56.44:80"}, {"http": "182.61.117.113:80"}]

url = "http://www.kuaidaili.com/free/inha/2/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
           'Referer': 'http://www.hexun.com'}
data = ""

# 设置代理服务器
proxy_s = urllib2.ProxyHandler(proxies[0])
opener = urllib2.build_opener(proxy_s)
urllib2.install_opener(opener)

request = urllib2.Request(url, data, headers)

response = urllib2.urlopen(request)
doc = response.read()

soup = BeautifulSoup(doc)
print soup.prettify()
