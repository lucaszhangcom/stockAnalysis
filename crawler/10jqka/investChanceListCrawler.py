# -*- coding: UTF-8 -*-
# 投资机会

import sys
from proxy import Proxies
from bs4 import BeautifulSoup


class InvestChanceListCrawler:
    __url_path = "http://stock.10jqka.com.cn/tzjh_list/"

    def __init__(self):
        print "init InvestChanceListCrawler"

    def crawl_list(self):
        url = self.__url_path + "index.shtml"
        proxies = Proxies()

        response = proxies.crawl_url(url)
        if response is None:
            sys.exit()

        soup = BeautifulSoup(response.read())
        article_list = soup.select(".arc-title")
        print article_list

        for article in article_list:
            h = article.a['href']
            title = article.a['title']
            publish_date = article.span.string
            print "%s\t%s\t%s" % (h, title, publish_date)


investChanceList = InvestChanceListCrawler()
investChanceList.crawl_list()
