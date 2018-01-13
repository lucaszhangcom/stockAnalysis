# -*- coding: UTF-8 -*-
# 一周交易备忘

import urllib
import urllib2
import sys
import time
from bs4 import BeautifulSoup

type = sys.getfilesystemencoding()

proxies = [{"https": "106.14.241.155:80"}, {"http": "114.44.179.194:8080"}, {"http": "37.17.56.44:80"}, {"http": "182.61.117.113:80"}]

url = "http://stockdata.stock.hexun.com/2008/yzjybw.aspx?"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
           'Referer': 'http://www.hexun.com'}
data = ""

# 设置代理服务器
proxy_s = urllib2.ProxyHandler(proxies[0])
opener = urllib2.build_opener(proxy_s)
urllib2.install_opener(opener)

oneDay = 60 * 60 * 24
today = time.time()
for i in range(1, 2):
    currentDay = time.strftime("%Y.%m.%d", time.localtime(today + oneDay * i))

    params = {"d": currentDay}
    encodedParam = urllib.urlencode(params)

    urlWithParam = url + encodedParam
    print urlWithParam

    request = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(request)
        doc = response.read()

        soup = BeautifulSoup(doc.decode("gb18030").encode(type))

        trs = soup.find_all("tr")
        trsLen = len(trs) - 1
        for tr in trs[2: trsLen]:
            tds = tr.find_all("td")

            if u"除权除息" in tds[3].string or u"股权登记" in tds[3].string:
                print tds[0].string
                print tds[1].string
                print tds[3].string
    except urllib2.HTTPError, e:
        print e.code + "\t" + urlWithParam


