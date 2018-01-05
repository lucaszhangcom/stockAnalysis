# -*- coding: UTF-8 -*-
# 股票表操作类

from dao import DataSource
import sys
from model import Stock

class StockDao:

    def __init__(self):
        print "init StockDao..."

    def insert_stock(self, code, name):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute("insert into stock(code, name) values('%s', '%s')" % (code, name))
            conn.commit()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def query_all_stock(self):
        stocks = {}

        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute("select id, code, name, bps ,eps ,net_income ,ngpr ,income ,sps ,fps ,udpps ,total_stock_issue,"
                        "liqui from stock order by id")
            result = cur.fetchall()
            for r in result:
                stock = Stock(r[0], r[1], r[2], r[3], r[4], r[5], r[6],
                              r[7], r[8], r[9], r[10], r[11], r[12])
                stocks[r[1]] = stock

            return stocks
        except:
            print "Unexpected error:", sys.exc_value
            return None
        finally:
            cur.close()
            conn.close()

    def update_finance_info(self, stock):
        sql = "update stock set bps=%f ,eps=%f ,net_income=%f ,ngpr =%f,income=%f ,sps=%f ,fps=%f ,udpps=%f ,total_stock_issue=%f ,liqui=%f where code = '%s'"

        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute(sql % (stock.bps, stock.eps, stock.net_income, stock.ngpr, stock.income, stock.sps, stock.fps, stock.udpps, stock.total_stock_issue, stock.liqui, stock.code))
            conn.commit()
        except:
            print "Unexpected error:", sys.exc_value
            conn.rollback()
        finally:
            cur.close()
            conn.close()