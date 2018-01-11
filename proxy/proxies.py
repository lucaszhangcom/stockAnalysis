# -*- coding: UTF-8 -*-

import random
import urllib2

import sys

from bs4 import BeautifulSoup


class Proxies:

    __proxies = []

    __test_url = "http://www.baidu.com"

    __headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                 'Referer': 'http://www.hexun.com',
                 'Accept-Language': 'zh-CN,zh;q=0.9',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Connection': 'keep-alive'}

    __data = ""

    def __init__(self):
        if len(self.__proxies) == 0:
            proxy_file = "/Users/lucas-joyce/工作/python/stockCrawler/proxy/allProxies.txt"
            # proxy_file = "/home/lucaszhang/workspace/python/stockCrawler/proxy/allProxies.txt"
            f = open(proxy_file, "r")
            for l in f:
                split = l.split("\t")
                proxy = {split[0]: split[1].replace("\n", "")}
                if proxy not in self.__proxies:
                    self.__proxies.append(proxy)
            f.close()

            # self.crawl_newest_proxy()

            print "load %s proxy..." % len(self.__proxies)

    def _get_proxy(self):
        while len(self.__proxies):
            random_idx = random.randint(0, len(self.__proxies) - 1)
            print "proxy idx:" + str(random_idx)

            try:
                proxy_handler = urllib2.ProxyHandler(self.__proxies[random_idx])
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)

                request = urllib2.Request(url=self.__test_url)
                # request = urllib2.Request(url=self.__test_url, data=self.__data, headers=self.__headers)
                urllib2.urlopen(request, timeout=5)

                return self.__proxies[random_idx]
            except:
                del self.__proxies[random_idx]

                print "Unexpected error:", sys.exc_info()[0]
                print str(len(self.__proxies)) + " proxy are alive..."

        if len(self.__proxies) == 0:
            return None

    def set_header(self, name, value):
        self.__headers[name] = value

    def crawl_url(self, url, timeout=5, is_get=False):
        proxy = self._get_proxy()
        if proxy is None:
            print "all proxy are dead"
            return None

        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        if is_get:
            request = urllib2.Request(url, headers=self.__headers)
        else:
            request = urllib2.Request(url, self.__data, self.__headers)

        try:
            return urllib2.urlopen(request, timeout=timeout)
        except:
            print "Unexpected error:", sys.exc_value
            return None

    def crawl_newest_proxy(self):
        cookie = '_ga=GA1.2.2091969811.1511755096; yd_cookie=58d13f31-b3c6-495e6bae32b7473cf52c2c303e7c80fb4baa; channelid=0; _gid=GA1.2.1307501978.1513334676; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1511755096,1513334676; _ydclearance=493958ffc814a897b587f03b-8dc2-465f-b833-0997ba69b175-1513349113; sid=1513341798232407; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1513341919'
        host = 'www.kuaidaili.com'
        referer = 'http://www.kuaidaili.com/free/inha/2/'

        self.__headers['Cookie'] = cookie
        self.__headers['Host'] = host
        self.__headers['Referer'] = referer

        print "crawl newest proxy..."

        # sys_charset = sys.getfilesystemencoding()
        url = "http://www.kuaidaili.com/free/inha/1/"
        response = self.crawl_url(url, is_get=True)

        doc = response.read()
        soup = BeautifulSoup(doc)

        proxy_list = soup.find(attrs={"class": "table table-bordered table-striped"})
        tbody = proxy_list.tbody
        # print proxy_list

        # proxy_file = "/Users/lucas-joyce/工作/python/stockCrawler/proxy/allProxies.txt"
        proxy_file = "/home/lucaszhang/workspace/python/stockCrawler/proxy/allProxies.txt"
        f = open(proxy_file, "a")
        for tr in tbody.select("tr"):
            tds = tr.select("td")

            proxy = {tds[3].string : tds[0].string + ":" + tds[1].string}
            if proxy not in self.__proxies:
                self.__proxies.append(proxy)
                f.write("\n%s\t%s" % (tds[3].string, tds[0].string + ":" + tds[1].string))

                print "%s\t%s\t%s" % (tds[3].string, tds[0].string, tds[1].string)

        f.close()

# t = Proxies()
# t.crawl_newest_proxy()

