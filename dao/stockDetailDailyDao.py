# -*- coding: UTF-8 -*-
# 股票每日交易明细

from dao import DataSource
import logging
import logging.config

import sys

class StockDetailDailyDao:

    __logger = None

    def __init__(self):
        logging.config.fileConfig("/Users/lucas-joyce/工作/python/stockCrawler/logger.config")
        self.__logger = logging.getLogger('ths_crawler')

    def insert_detail_daily(self, stock_detail_daily):
        sql = "insert into stock_detail_daily(stock_id, open_price, close_price, highest_price, lowest_price, " \
              "trading_volume, turnover, market_value, circulated_stock_value, amplitude, trading_volume_rate, " \
              "pb_ratio, pe_ratio, large_in, mid_in, small_in, large_out, mid_out, small_out, website) " \
              "values (%d, %f, %f, %f, %f, %d, %f, %d, %d, %f, %f, %f, %f, %d, %d, %d, %d, %d, %d, %d)"

        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute(sql % (stock_detail_daily.stock_id, stock_detail_daily.open_price, stock_detail_daily.close_price,
                               stock_detail_daily.highest_price, stock_detail_daily.lowest_price,
                               stock_detail_daily.trading_volume, stock_detail_daily.turnover, stock_detail_daily.market_value,
                               stock_detail_daily.circulated_stock_value, stock_detail_daily.amplitude, stock_detail_daily.trading_volume_rate,
                               stock_detail_daily.pb_ratio, stock_detail_daily.pe_ratio, stock_detail_daily.large_in,
                               stock_detail_daily.mid_in, stock_detail_daily.small_in, stock_detail_daily.large_out,
                               stock_detail_daily.mid_out, stock_detail_daily.small_out, stock_detail_daily.website))
            conn.commit()
        except:
            conn.rollback()
            self.__logger.error("Unexpected error: %s" % sys.exc_value)
        finally:
            cur.close()
            conn.close()

