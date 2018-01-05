# -*- coding: UTF-8 -*-
# 股东报表

import re
import sys

from proxy import Proxies
from utils import UnitConversionUtil
from bs4 import BeautifulSoup

from dao import StockDao
from dao import ShareholderReportDao

class ShareholderReportCrawler:

    __holder_url = 'http://basic.10jqka.com.cn/%s/holder.html'
    __url = "http://stockpage.10jqka.com.cn/%s/holder/"

    __shareholder_report_dao = None

    def __init__(self):
        self.__shareholder_report_dao = ShareholderReportDao()

    def holder_report(self, stock_code, stock_id, shareholder_report_dict=None):
        if shareholder_report_dict is None:
            shareholder_report_dict = self.__shareholder_report_dao.query_newest_report(stock_code)

        unitConversionUtil = UnitConversionUtil()

        print self.__holder_url % stock_code
        proxy = Proxies()
        response = proxy.crawl_url(self.__holder_url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())

        data_tbody = soup.select(".data_tbody")
        thead = data_tbody[0].select(".top_thead")[0].select("th")
        tbody = data_tbody[0].select(".tbody")[0].select("tr")

        for i in range(0, len(thead)):
            report_date = thead[i].string
            if shareholder_report_dict is not None and shareholder_report_dict[stock_code] == report_date:
                break

            total_shareholder = tbody[0].select("td")[i].string

            shareholder_chain = tbody[1].select("td")[i].contents[0]
            avg_tradable_share = tbody[2].select("td")[i].get_text()
            avg_tradable_share_chain = tbody[3].select("td")[i].contents[0]

            matches = re.search(r'(\d+\.\d+%)', shareholder_chain)
            if matches:
                shareholder_chain = matches.group(1)
            else:
                shareholder_chain = tbody[1].select("td")[i].select("span")[0].get_text()

            matches = re.search(r'(\d+\.\d+%)', avg_tradable_share_chain)
            if matches:
                avg_tradable_share_chain = matches.group(1)
            else:
                avg_tradable_share_chain = tbody[3].select("td")[i].select("span")[0].get_text()

            shareholder_chain = unitConversionUtil.prent_to_fload(shareholder_chain)
            avg_tradable_share_chain = unitConversionUtil.prent_to_fload(avg_tradable_share_chain)

            if total_shareholder[-1:] == u'亿' or total_shareholder[-1:] == u'万':
                total_shareholder = unitConversionUtil.convert_to_yuan(total_shareholder[:-1], total_shareholder[-1:])

            if avg_tradable_share[-1:] == u'亿' or avg_tradable_share[-1:] == u'万':
                avg_tradable_share = unitConversionUtil.convert_to_yuan(avg_tradable_share[:-1], avg_tradable_share[-1:])

            self.__shareholder_report_dao.insert_shareholder_report(stock_id, report_date, int(float(total_shareholder)),
                                                                    shareholder_chain, int(float(avg_tradable_share)),
                                                                    avg_tradable_share_chain)
            print stock_id, report_date, total_shareholder, shareholder_chain, avg_tradable_share,avg_tradable_share_chain

    def all_holder_report(self):
        stock_dao = StockDao()
        all_stock = stock_dao.query_all_stock()

        for stock_code, stock in all_stock.items():
            try:
                self.holder_report(stock.code, stock.id)
            except:
                print "Unexpected error:", sys.exc_value

shareholderReportCrawler = ShareholderReportCrawler()
shareholderReportCrawler.all_holder_report()
