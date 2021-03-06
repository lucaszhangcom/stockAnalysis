# -*- coding: UTF-8 -*-
# 每日前N名板块

from dao import DataSource
import logging
import logging.config

import sys


class TopCategoryDailyDao:

    __logger = None

    def __init__(self):
        logging.config.fileConfig("/Users/lucas-joyce/工作/python/stockCrawler/logger.config")
        self.__logger = logging.getLogger('ths_crawler')

    def insert_top_category_daily(self, category_id, ranking, net_inflow, rise, fall):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            sql = "insert into top_category_daily(category_id, ranking, net_inflow, rise, fall) values(%d, %d, %f, %d, %d)"
            cur.execute(sql % (category_id, ranking, net_inflow, rise, fall))
            conn.commit()
        except:
            self.__logger.error("Unexpected error: %s" % sys.exc_info()[0])
            conn.rollback()
        finally:
            cur.close()
            conn.close()
