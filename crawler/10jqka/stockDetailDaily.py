# -*- coding: UTF-8 -*-
# 个股每日交易明细
# 每天执行一次

from proxy import Proxies
from utils import UnitConversionUtil
from bs4 import BeautifulSoup


class StockDetailDaily:
    __url = "http://stockpage.10jqka.com.cn/%s/funds/"

    def __init__(self):
        print

    def __crawl(self, stock_code):
        proxy = Proxies()
        response = proxy.crawl_url(self.__url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())
        print soup.prettify()

    def crawl_all_stock(self):
        self.__crawl('600025')


stockDetailDaily = StockDetailDaily()
stockDetailDaily.crawl_all_stock()