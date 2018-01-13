# -*- coding: UTF-8 -*-
# 股东报表

from dataSource import DataSource

import sys


class ShareholderReportDao:

    def __init__(self):
        print "init ShareholderReportDao..."

    def insert_shareholder_report(self, stock_id, report_date, total_shareholder,
                                  shareholder_chain, avg_tradable_share,avg_tradable_share_chain):
        sql = "insert into shareholder_report(stock_id, report_date, total_shareholder, shareholder_chain, " \
              "avg_tradable_share, avg_tradable_share_chain) values(%d, '%s', %d, %f, %d, %f)"

        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            cur.execute(sql % (stock_id, report_date, total_shareholder,
                               shareholder_chain, avg_tradable_share,avg_tradable_share_chain))
            conn.commit()
        except:
            conn.rollback()
            print "Unexpected error:", sys.exc_value
        finally:
            cur.close()
            conn.close()

    def query_newest_report(self, stock_code=''):
        sql = 'select s.code as code, to_char(max(sr.report_date),\'YYYY-MM-DD\') as report_date ' \
              'from stock s ' \
              'join shareholder_report sr on s.id = sr.stock_id '

        if stock_code != '':
            sql += "where s.code = '%s' " % stock_code

        sql += 'group by s.code'

        data_source = DataSource()
        conn = data_source.get_conn()

        cur = conn.cursor()
        try:
            report_map = {}
            cur.execute(sql)
            result = cur.fetchall()
            for r in result:
                report_map[r[0]] = r[1]

            return report_map
        except:
            print "Unexpected error:", sys.exc_value
            return None
        finally:
            cur.close()
            conn.close()
