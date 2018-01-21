# -*- coding: UTF-8 -*-
# 新股上市

import sys
from datetime import datetime

from proxy import Proxies
from bs4 import BeautifulSoup

from dao import StockDao
import logging
import logging.config


class IpoCrawler:
    __url = "http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/1/order/desc/ajax/1/"

    __logger = None

    def __init__(self):
        logging.config.fileConfig("/Users/lucas-joyce/工作/python/stockCrawler/logger.config")
        self.__logger = logging.getLogger('ths_crawler')
        self.__logger.info("init IpoCrawler...")

    def ipo(self):
        system_encoding = sys.getfilesystemencoding()
        stock_dao = StockDao()
        proxies = Proxies()

        response = proxies.crawl_url(self.__url, is_get=True)
        if response is None:
            sys.exit()

        date = datetime.date(datetime.now())
        now = date.today()

        soup = BeautifulSoup(response.read().decode("gbk").encode(system_encoding))
        soup.prettify()

        trs = soup.find(attrs={"id": "maintable"}).tbody.select("tr")
        for tr in trs:
            tds = tr.select("td")
            if tds[14].string == '-':
                continue

            splits = tds[14].string.split('-')
            ipo_date = datetime.date(datetime.now())
            ipo_date = ipo_date.replace(month=int(splits[0]), day=int(splits[1]))
            if now == ipo_date:
                stock_dao.insert_stock(tds[0].a.string, tds[1].string)
                self.__logger.info("ipo:%s\t%s" % (tds[0].a.string, tds[1].string))

ipoCrawler = IpoCrawler()
ipoCrawler.ipo()
