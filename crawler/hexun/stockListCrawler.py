# -*- coding: UTF-8 -*-
import time
import urllib2
import exceptions
from bs4 import BeautifulSoup
import random
import httplib
import codecs

import sys
from proxy import Proxies
from dao import StockDao

stockDao = StockDao()

systemEncoding = sys.getfilesystemencoding()

szList = ["600", "601", "603", "000", "002", "300"]

stockUrl = "http://stockdata.stock.hexun.com/"

successFile = codecs.open("/tmp/stockList.txt", "a", systemEncoding)
failFile = codecs.open("/tmp/failStockList.txt", "a", systemEncoding)


proxies = Proxies()
stockDao = StockDao()

random.seed(time.time())
for sz in szList:
    for idx in range(1, 999):
        if idx < 10:
            stockId = sz + "00" + str(idx)
        elif idx < 100:
            stockId = sz + "0" + str(idx)
        else:
            stockId = sz + str(idx)

        url = stockUrl + stockId + ".shtml"
        try:
            print url
            response = proxies.crawl_url(url)
            if response is None:
                sys.exit()

            doc = response.read()
            soup = BeautifulSoup(doc.decode("gb18030").encode(systemEncoding))

            keywords = soup.find(attrs={"name": "keywords"})['content']
            splits = keywords.split(",")
            if stockId != splits[1]:
                print stockId + " is error"
            else:
                print splits[1] + "\t" + splits[0]
                stockDao.insert_stock(splits[1], splits[0])
                successFile.write(splits[1] + "\t" + splits[0] + "\n")
                print keywords + " is ok"
        except urllib2.HTTPError, e:
            print("%s\t%s" % (stockId, e.code))
            if e.code != 404 and e.code != 501:
                print stockId + "\t" + str(e.code)
                failFile.write("%s\t%s\n" % (stockId, e.code))
        except urllib2.URLError, e:
            print e.reason
            failFile.write(str(stockId) + " read timed out\n")
        except httplib.BadStatusLine, e:
            print e
            failFile.write("%s\t%s\n" % (stockId, e))
        except exceptions.UnicodeDecodeError, e:
            print e.reason
            failFile.write("%s\t%s\n" % (stockId, e.reason))
        except:
            failFile.write("%s\t%s\n" % (stockId, sys.exc_info()[0]))
            print "Unexpected error:", sys.exc_info()[0]


successFile.close()
failFile.close()


