# -*- coding: UTF-8 -*-
# 个股每日交易明细
# 每天执行一次

from proxy import Proxies
from bs4 import BeautifulSoup
from model import StockDetailDaily
from dao import StockDao
from dao import StockDetailDailyDao

import json
import sys
import time
import random


class StockDetailDailyCrawler:
    __detail_data_url = "http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js"
    __fund_url = "http://stockpage.10jqka.com.cn/spService/%s/Funds/realFunds"

    __stock_detail_daily_dao = None

    def __init__(self):
        print "init StockDetailDailyCrawler..."
        self.__stock_detail_daily_dao = StockDetailDailyDao()

    def _byteify(self, data, ignore_dicts=False):
        # if this is a unicode string, return its string representation
        if isinstance(data, unicode):
            return data.encode('utf-8')
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [self._byteify(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self._byteify(key, ignore_dicts=True): self._byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
                }
        # if it's anything else, return it in its original form
        return data

    def __crawl_detail_data(self, stock_code):
        cookie = 'spversion=20130314; searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1513693109,1513780630,1513845199,1514904192; historystock=000001%7C*%7C600025%7C*%7C600460%7C*%7C600621%7C*%7C002839; v=Ap_D9SBwORmGcz0FozQdyct-KPgtBPHhDVn3mjHsOsOXcLHuOdSD9h0ohoRB'
        referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'

        proxy = Proxies()
        proxy.set_header('Cookie', cookie)
        proxy.set_header('Referer', referer)

        response = proxy.crawl_url(self.__detail_data_url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())
        json_str = soup.prettify()
        json_str = json_str.lstrip('quotebridge_v2_realhead_hs_%s_last(' % stock_code)
        json_obj = json.loads(json_str[:-2], object_hook=self._byteify)

        return json_obj.get('items')

    def __crawl_fund(self, stock_code):
        cookie = 'spversion=20130314; searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1513693109,1513780630,1513845199,1514904192; historystock=000001%7C*%7C600025%7C*%7C600460%7C*%7C600621%7C*%7C002839; v=Ap_D9SBwORmGcz0FozQdyct-KPgtBPHhDVn3mjHsOsOXcLHuOdSD9h0ohoRB'
        referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'

        proxy = Proxies()
        proxy.set_header('Cookie', cookie)
        proxy.set_header('Referer', referer)

        response = proxy.crawl_url(self.__fund_url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())
        return json.loads(soup.prettify(), object_hook=self._byteify)

    def __crawl(self, stock):
        print "crawl %s detail daily..." % stock.code
        detail_data = self.__crawl_detail_data(stock.code)
        fund_data = self.__crawl_fund(stock.code)

        stock_detail_daily = StockDetailDaily()
        stock_detail_daily.stock_id = stock.id
        stock_detail_daily.open_price = float(detail_data.get('7'))
        stock_detail_daily.close_price = float(detail_data.get('10'))
        stock_detail_daily.highest_price = float(detail_data.get('8'))
        stock_detail_daily.lowest_price = float(detail_data.get('9'))
        stock_detail_daily.trading_volume_rate = float(detail_data.get('1968584'))/100
        stock_detail_daily.pb_ratio = float(detail_data.get('592920'))
        stock_detail_daily.pe_ratio = float(detail_data.get('2034120'))
        stock_detail_daily.amplitude = float(detail_data.get('526792'))/100
        stock_detail_daily.market_value = float(detail_data.get('3541450'))
        stock_detail_daily.circulated_stock_value = float(detail_data.get('3475914'))
        stock_detail_daily.turnover = float(detail_data.get('19'))

        trading_volume = float(detail_data.get('13'))
        stock_detail_daily.trading_volume = trading_volume

        turnover = fund_data.get('title')['zlc'] + fund_data.get('title')['zlr']
        for fund in fund_data.get('flash'):
            if fund.get('name') == '\xe5\xa4\xa7\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#大单流出
                stock_detail_daily.large_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe4\xb8\xad\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#中单流出
                stock_detail_daily.mid_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xb0\x8f\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#小单流出
                stock_detail_daily.small_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xb0\x8f\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#小单流入
                stock_detail_daily.small_in = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe4\xb8\xad\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#中单流入
                stock_detail_daily.mid_in = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xa4\xa7\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#大单流入
                stock_detail_daily.large_in = int(float(fund.get('sr')) / turnover * trading_volume)

        self.__stock_detail_daily_dao.insert_detail_daily(stock_detail_daily)

    def crawl_all_stock(self):
        stock_dao = StockDao()
        all_stocks = stock_dao.query_all_stock()
        for stock in all_stocks.items():
            try:
                self.__crawl(stock[1])
            except:
                print "Unexpected error:", sys.exc_value

            sleep_time = random.randint(10, 80)
            print "sleep %d second...\n" % sleep_time
            time.sleep(sleep_time)


stockDetailDaily = StockDetailDailyCrawler()
stockDetailDaily.crawl_all_stock()