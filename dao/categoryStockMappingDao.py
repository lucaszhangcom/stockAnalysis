# -*- coding: UTF-8 -*-
# 成分股表

from dao import DataSource
from model import CategoryStockMapping

import sys

class CategoryStockMappingDao:

    def __init__(self):
        print "CategoryStockMappingDao init..."

    def query_all(self):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            category_stock_mappings = {}
            cur.execute("select id, stock_id, category_id from stock_category_mapping")
            result = cur.fetchall()
            for r in result:
                category_stock_mapping = CategoryStockMapping(r[0], r[1], r[2])
                category_stock_mappings["%s_%s" % (r[2], r[1])] = category_stock_mapping

            return category_stock_mappings
        except:
            print "Unexpected error:", sys.exc_info()[0]
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()