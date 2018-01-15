# -*- coding: UTF-8 -*-
# 财务数据
#

from model import Stock
from dao import StockDao
from utils import UnitConversionUtil
from proxy import Proxies

from bs4 import BeautifulSoup

import sys


class StockFinanceCrawler:

    __url = "http://stockpage.10jqka.com.cn/%s/"

    def __init__(self):
        print "init StockFinanceCrawler..."

    def __init_stock(self, stock_code, finance_detail):
        unit_conversion_util = UnitConversionUtil()
        net_income = unit_conversion_util.convert_to_yuan(finance_detail[7].string[:-2],
                                                          finance_detail[7].string[-2:-1])
        income = unit_conversion_util.convert_to_yuan(finance_detail[9].string[:-2], finance_detail[9].string[-2:-1])
        total_stock_issue = unit_conversion_util.convert_to_yuan(finance_detail[13].string[:-1],
                                                                 finance_detail[13].string[-1:])
        liqui = unit_conversion_util.convert_to_yuan(finance_detail[14].string[:-1], finance_detail[14].string[-1:])

        stock = Stock(id='', code=stock_code, name='', bps=float(finance_detail[5].string[:-1]),
                      eps=float(finance_detail[6].string[:-1]), net_income=net_income,
                      ngpr=float(finance_detail[8].string[:-1]), income=income,
                      sps=float(finance_detail[10].string[:-1]), fps=float(finance_detail[11].string[:-1]),
                      udpps=float(finance_detail[12].string[:-1]), total_stock_issue=total_stock_issue, liqui=liqui)

        return stock

    def __finance_detail(self, stock_code):
        url = self.__url % stock_code

        proxies = Proxies()
        response = proxies.crawl_url(url, is_get=True)

        try:
            soup = BeautifulSoup(response.read())
            finance_detail = soup.select(".company_details")[0].select("dd")
            stock = self.__init_stock(stock_code, finance_detail)

            stock_dao = StockDao()
            stock_dao.update_finance_info(stock)
            print "update stock(%s) finance info..." % stock.code
        except:
            print "Unexpected error:", sys.exc_value

    def all_finance_detail(self):
        stock_dao = StockDao()
        stocks = stock_dao.query_all_stock()

        for stock_code in stocks.keys():
            self.__finance_detail(stock_code)

    def one_finance_detail(self, stock_code):
        self.__finance_detail(stock_code)

stockFinanceCrawler = StockFinanceCrawler()
#stockFinanceCrawler.all_finance_detail()
stockFinanceCrawler.one_finance_detail('002925')
# stockFinanceCrawler.one_finance_detail('300664')
# stockFinanceCrawler.one_finance_detail('002923')
# stockFinanceCrawler.one_finance_detail('300735')