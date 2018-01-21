# -*- coding: UTF-8 -*-
# 每日行业版块排名数据

import sys

from proxy import Proxies
from bs4 import BeautifulSoup

from model import TopCategoryDaily

from dao import CategoryDao
from dao import StockDao
from dao import CategoryStockMappingDao
from dao import TopCategoryDailyDao

import logging
import logging.config


class CategoryCrawler:
    # 行业分类
    __category_all = -1
    __category_industry = 1
    __category_concept = 2

    __category_industry_url = "http://q.10jqka.com.cn/thshy/"
    __category_concept_url = "http://q.10jqka.com.cn/gn/"
    __category_concept_detail_url = "http://q.10jqka.com.cn/gn/detail/code/%s/"
    # 板块成分股列表
    __category_industry_stock_url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/$$page$$/ajax/1/code/"
    __category_concept_stock_url = "http://q.10jqka.com.cn/gn/detail/order/desc/page/$$page$$/ajax/1/code/"
    
    __categories = None
    __logger = None

    def __init__(self):
        if self.__categories is None:
            category_dao = CategoryDao()
            self.__categories = category_dao.query_category(self.__category_all)

        logging.config.fileConfig("/Users/lucas-joyce/工作/python/stockCrawler/logger.config")
        self.__logger = logging.getLogger('ths_crawler')

    def top15_concept_daily(self):
        top_category_daily_dao = TopCategoryDailyDao()

        category_dao = CategoryDao()
        categories = category_dao.query_category(self.__category_concept)

        top_categories = []
        proxy = Proxies()

        for category_code in categories.keys():
            self.__logger.info(self.__category_concept_detail_url + category_code)
            response = proxy.crawl_url(self.__category_concept_detail_url % category_code, is_get=True)
            # print soup.prettify()
            try :
                soup = BeautifulSoup(response.read())
                board_info = soup.select(".board-infos")[0].select("dl")

                increase = board_info[5].dd.string[:-1]
                net_inflow = board_info[8].dd.string
                rise = board_info[7].dd.select("span")[0].string
                fall = board_info[7].dd.select("span")[1].string

                top_category_daily = TopCategoryDaily(-1, categories[category_code].id, float(increase), float(net_inflow), int(rise), int(fall))
                top_categories.append(top_category_daily)
            except:
                self.__logger.error("Unexpected error: %s" % sys.exc_info()[0])
                continue

            self.__logger.info("%s\t%s\t%s\t%s" % (categories[category_code].id, net_inflow, rise, fall))

        top_categories.sort(key=lambda tc: tc.ranking, reverse=True)
        for i in range(0, 15):
            top_category = top_categories[i]
            top_category_daily_dao.insert_top_category_daily(top_category.category_id, i + 1, top_category.net_inflow,
                                                             top_category.rise, top_category.fall)
            self.__logger.info("%s\t%s\t%s\t%s\t%s" % (top_category.category_id, i + 1, top_category.net_inflow,
                                                             top_category.rise, top_category.fall))

    def top10_industry_daily(self):
        top_category_daily_dao = TopCategoryDailyDao()

        category_dao = CategoryDao()
        categories = category_dao.query_category(self.__category_industry)

        proxy = Proxies()
        response = proxy.crawl_url(self.__category_industry_url, is_get=True)
        soup = BeautifulSoup(response.read())

        # print soup.prettify()

        closing_quotation = soup.find(attrs={"class": "m-table m-pager-table"})
        trs = closing_quotation.tbody.select("tr")
        for i in range(0, 10):
            tds = trs[i].select("td")
            category_code = tds[1].a['href'][-7: -1]

            category_id = categories[category_code].id
            net_inflow = float(tds[5].string)
            rise = int(tds[6].string)
            fall = int(tds[7].string)
            top_category_daily_dao.insert_top_category_daily(category_id, i+1, net_inflow, rise, fall)
            self.__logger.info("%s\t%s\t%s\t%s\t%s" % (category_id, i+1, net_inflow, rise, fall))

    def __cate_stock(self, category_code, category_type, page_num):
        if category_type == self.__category_industry:
            url = self.__category_industry_stock_url.replace("$$page$$", str(page_num)) + category_code
        else:
            url = self.__category_concept_stock_url.replace("$$page$$", str(page_num)) + category_code

        system_encoding = sys.getfilesystemencoding()

        self.__logger.info(url)

        stock_codes = []
        proxy = Proxies()
        response = proxy.crawl_url(url)
        if response is None:
            return stock_codes

        soup = BeautifulSoup(response.read().decode("gbk").encode(system_encoding))
        stocks = soup.find(attrs={"class": "m-table m-pager-table"})
        trs = stocks.tbody.select("tr")
        for tr in trs:
            tds = tr.select("td")
            stock_codes.append(tds[1].string)

        return stock_codes

    def __get_category(self, cate_url, cate_type):
        stock_dao = StockDao()
        stocks = stock_dao.query_all_stock()

        cate_stock_mapping_dao = CategoryStockMappingDao()
        category_stock_mappings = cate_stock_mapping_dao.query_all()

        category_dao = CategoryDao()
        proxy = Proxies()

        # 行业板块
        response = proxy.crawl_url(cate_url)
        soup = BeautifulSoup(response.read())

        page_info = soup.select(".page_info")[0].string
        idx = page_info.find("/")
        if idx == -1:
            page_total_num = int(page_info)
        else:
            page_total_num = int(page_info[idx + 1])

        cate_items = soup.select(".cate_items")
        for cate_item in cate_items:
            for industry in cate_item.select("a"):
                url = industry['href']
                code = url[-7:-1]
                name = industry.string

                if code not in self.__categories:
                    category_dao.insert_category(code, name, cate_type, url)
                    self.__logger.info("%s\t%s\t%s\t%s" % (code, name, cate_type, url))
                    continue

                # TODO 板块成分股应该在新的方法中进行处理
                category = self.__categories[code]
                for cur_page in range(1, page_total_num+1):
                    try:
                        stock_codes = self.__cate_stock(code, cate_type, cur_page)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        continue

                    for stock_code in stock_codes:
                        stock = stocks.get(stock_code)
                        if stock is None:
                            continue

                        key = "%s_%s" % (category.id, stock.id)
                        if key not in category_stock_mappings:
                            category_dao.insert_category_stock_mapping(stock.id, category.id)

    def all_category(self):
        # 行业板块
        self.__get_category(self.__category_industry_url, self.__category_industry)
        # 概念板块
        self.__get_category(self.__category_concept_url, self.__category_concept)


categoryCrawler = CategoryCrawler()
categoryCrawler.top10_industry_daily()
categoryCrawler.top15_concept_daily()
