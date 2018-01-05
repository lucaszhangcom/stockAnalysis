# -*- coding: UTF-8 -*-
# 股票表


class Stock:

    def __init__(self, id, code, name, bps, eps, net_income, ngpr, income, sps, fps, udpps, total_stock_issue, liqui):
        self.id = id
        self.code = code
        self.name = name
        self.bps = bps
        self.eps = eps
        self.net_income = net_income
        self.ngpr = ngpr
        self.income = income
        self.sps = sps
        self.fps = fps
        self.udpps = udpps
        self.total_stock_issue = total_stock_issue
        self.liqui = liqui
