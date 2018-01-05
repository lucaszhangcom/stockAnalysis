# -*- coding: UTF-8 -*-
# 货币工具


class UnitConversionUtil:
    def __init__(self):
        print

    def convert_to_yuan(self, value, util=u'无'):
        if util == u'亿':
            v = float(value) * 10000 * 10000
        elif util == u'万':
            v = float(value) * 10000
        else:
            v = float(value)

        return v

    def prent_to_fload(self, prent, decimals=4):
        p_float = float(prent[:-1]) / 100
        return round(p_float, decimals)

