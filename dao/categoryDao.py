# -*- coding: UTF-8 -*-
# 行业，概念版块表

from model import Category
from dao import DataSource
import sys


class CategoryDao:

    def __init__(self):
        print

    def insert_category(self, code, name, category_type, url):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute("insert into category(code, name, cate_type, url) values('%s', '%s', '%s', '%s')" % (code, name, category_type, url))
            conn.commit()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def insert_category_stock_mapping(self, categroy_id, stock_id):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute("insert into stock_category_mapping(stock_id, category_id) values(%d, %d)" % (categroy_id, stock_id))
            conn.commit()

            print "insert category_stock_mapping %s %s" % (categroy_id, stock_id)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def query_category(self, cate_type):
        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            categories = {}
            sql = "select id, code, name, cate_type, url from category"
            if cate_type != -1:
                sql += " where cate_type = %d" % cate_type

            cur.execute(sql)
            result = cur.fetchall()
            for r in result:
                category = Category(r[0], r[1], r[2], r[3], r[4])
                categories[r[1]] = category

            return categories
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return None
        finally:
            cur.close()
            conn.close()