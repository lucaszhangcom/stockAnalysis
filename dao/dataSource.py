# -*- coding: UTF-8 -*-
# 数据库连接类

import psycopg2


class DataSource:

    # __host = "127.0.0.1"
    __host = "10.10.10.12"
    __port = "5432"
    __db = "stockAnalysis"
    __username = "stockanalysis"
    __passwd = "123456"

    def __init__(self):
        self.conn = psycopg2.connect(database=self.__db, user=self.__username,
                                     password=self.__passwd, host=self.__host, port=self.__port)

    def get_conn(self):
        if self.conn is not None:
            return self.conn
        else:
            return None


dataSource = DataSource()
conn = dataSource.get_conn()
