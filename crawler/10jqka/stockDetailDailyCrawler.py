# -*- coding: UTF-8 -*-
# 个股每日交易明细
# 每天执行一次

from proxy import Proxies
from bs4 import BeautifulSoup
from model import StockDetailDaily
from dao import StockDao
from dao import StockDetailDailyDao

import json
import sys
import time
import random


class StockDetailDailyCrawler:
    __detail_data_url = "http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js"
    __fund_url = "http://stockpage.10jqka.com.cn/spService/%s/Funds/realFunds"

    __stock_detail_daily_dao = None

    __cookies = [
        'spversion=20130314; searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1513693109,1513780630,1513845199,1514904192; historystock=000001%7C*%7C600025%7C*%7C600460%7C*%7C600621%7C*%7C002839; v=Ap_D9SBwORmGcz0FozQdyct-KPgtBPHhDVn3mjHsOsOXcLHuOdSD9h0ohoRB',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; log=; cmsad_170_0=0; cmsad_171_0=0; cmsad_172_0=0; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1513845199,1514904192,1515423544,1516026098; Hm_lvt_22a3c65fd214b0d5fd3a923be29458c7=1513845199,1514904193,1515423544,1516026099; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1516026119; Hm_lpvt_22a3c65fd214b0d5fd3a923be29458c7=1516026119; historystock=600569%7C*%7C600059%7C*%7C002925%7C*%7C000001; v=AhRIlA8ZMpuR1KZX4n2P5Zkl41mCbThPepHMm671oB8imbpP1n0I58qhnCf_',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AsOfYWQsnXY83FECWA3QuMJIVIxpOFemkcybKvWgHyKZtO16fQjnyqGcK_YE',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AnsnWexEpd7ENJlq4ymYQMpQDFTh0I8OieRTAm04V3qRzJUC9aAfIpm049t8',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=ArPvMfRc7QZMjKHS6_0gaLI4RLzZ6EdPAXyLWmVQD1IJZN2q7bjX-hFMGz50',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=ArnlAzoyx_S6Sptg9Zh6eoS-zi6Xxq2kl7rRiNvuNeBfYtdYIxa9SCcK4dZq',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Asaa-kHT4I2x-7RpXuY9s7-PEbdMJwv13Gs-wbDvsunEs2hhGLda8az7jkaB',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Al8DNeCweUoAaH1WXyk0VA4c6LjtxLJ6zRi33vGs-45VgHGu-ZRDtt3oR7wA',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Ai9zpRBAqfqweK3Gjt1kpN5suEg91ILYHSiHbkG8yx6lkEE-SaQTRi34FyNQ',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AtCM2OvNvg87TWILxfyT8eVZpxUmmbXN1n0IY8qhnCv-BX4DcqmEcyaN2Gsb',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AlAMWGtNPo-7zeKLRbsTcWXZJ5WmGTVNVv2I40ohHKt-hf6D8ikE86YNWOib',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AhJOnh3XnPHFt-CNsz6xX6vzZdPwIxeTSCcKZdxrPkWw77xFxLNmzRi3WtOt',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=ArTotO85Urt3gcZ3PiQvxTkFg3kijdlZGrFsP04VQD_CuVqvdp2oB2rBPG6f',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AlUJ10ZGo8j-loe0h_deFsByYloLUghK0wbtPNf6EUwbLnuMn6IZNGNW_aBm',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AvaqShHDsB0B60T5UNbNI--_QSf8Fzt_jFtuMWDf4ll0o5iRyKeKYVzrvu4x',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=ApfL7ehIgbKIwAU-GSF8fPbkIADl3GoQRbDvNunEs2bNGLn28az7jlWAfyz4',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Ajllg7qyR3Q6yhvgCg_6-gQ-Tq4XRizWFzpRCFtutWDf4lfYo5Y9yKeKYW3q',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AtqGJhU_VIm939gl1Y5pNyNrLYv4C1_L0I_SDeRThm04V3Q9zJuu9aAfIq21',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AnsnWexEpd7ENJlqnOGYQMpQDFTh0I78ieRTAm04V3qRzJUC9aAfIpm04-F8',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AhxA_EfBqnNPCV6vZ8gHndGd6zHKlcGRQjnUB_YdKIfqQbJnHqWQT5JJpClH',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Ar7ikgkraDX5E7wRWjaFG2fXCd8E_4NXFMM22WjHKoH8C1BJ0I_SieRThlA5',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Al8DNeCweUoAaH1WI-E0VA4c6LjtxLJIzRi33vGs-45VgHGu-ZRDtt3oR-oA',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=At-DtWAw-cqA6P3Woya01I6caDhtRDLITZg3XnEsew7VAPEueRTDNl1ox2mA',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AqH9yxK6XywSUvPYsZPSsjy2tma_ThRuP8K50AN2nagHas-QS54lEM8SyWKS',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AiF9S5I636yS0nNYMVRSMrw2NuY_zpTuv0I5UIP2HSiH6k8Qyx6lkE-SSe0S',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AuS4BL8pYgvHsZbHbdj_dWk1s-nSfQnJyqGcr_4FcK9yqYrfJo3YdxqxbPdP',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AoXZpxa2c1hOhlcENPNuhnBiksq7Qjj6g_YdrIfqQbzLHqs8T5JJpBNGLbcW',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AiZ62uEzQO3RmxRJg5qd0x-vcZesB2vvPEueoRDPEskkk8gBeJe60Qzb7mfh',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Asebfbi4UQJY8NWOSgUM7CaUUHCVzJqA9aAfppm049Z9COlmoZwr_gVwryeo',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Amk1EwqiF8SK-itwvxOKarQufh7HNlxGxyqBeAte5dCP0odIU4ZtOFd6kZSa',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AgpWtuUvZBkNz-i1AOo5p1MbXfuo-497gH8CfZRDtt3oR6StfIveZVAPUlJl',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AorWNmWv5JmNT2g1gKW5J9Ob3Xsoew_7AP-C_RTDNl1oxyQt_Ate5dCP0tfl',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AkwQTBcxesMfOW4_kizXDQGNG6F6hfEB8ikEd6YNWPeaMeKXzpXAv0I51OL3',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Au6yYtkbOIVJA0zhjSpVi5fHOU-077PHxLNmSRi3WvGs-4D5gH8C-ZRDtrnp',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Avmlw3ryh7T6ilsgToA6OkT-Dm7XBuyW1_oRyBsudSCfoheYY1b9iGdKIXSq',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AprGZtV_lMl9nxhlERmpd2Mr7Uu4yx-LkE-SzaQTRi34FzT9jFtutWDf4jJ1',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AjtnmayE5R6E9Nmq2P7YgAoQzBShkE68SaQTwi34FzpRjFXCtWDf4ll0o_g8',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=At2Bv37uWyA2_j8MyUBWDpiq6rLT-hBiGy51pJ-iGTRjVvMkZ0ohHKt-hYEu',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=An4i0slrqHW50_xRnrnFW6eXyZ_Ev0MX1IP2mSiH6kG8yxAJkE-SSaQTRln5',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Ah9DdaDwuYrAKL2WZxZ0lE7cqHithHIIjdh3nrFsu04VQDFuuVQDdp2oBx3A',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=Aqr2VkXPhDntLwhVok1Zh_N7_RtIGy9bIJ-inTRjVv2IZ0SNHKt-hfAv8lEF',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; v=AksXyRxUlU50BMmaa6LI0Jqg3OQx4F5M2fQjkr1IJwrh3GWSRbDvsunEsx3M',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AprGZtV_lMkGwxhlE5Wpd2Mr7Uu4yx-LkE-SzaQTRi34FzT9jFtutWDf4id1',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AlwAvIeBajP0FR5vIRzHXZHdK3EK1QHRgnkURzZdaMcqgfKnXuXQj9KJ5NKH',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AtyAPAcB6rN0lZ7voUNH3RFdq_GKVYFRAvmUx7bd6EeqAXIn3mVQD1IJZFcH',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AkAcaPv9Dl-w4fJbrQhjIdWJF8UWySXfxq14E7rRDNvuNe7zYtn0Ixa9SKAL',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AuK-Dk3nzGEO29A9lO7hr3vDNWNAM-cBmDfa9Sx7DtUA_4zVFMM2XWjHKgv9',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AmI-js1nTOGOW1C9FClhL_tDtePAs2eBGLdadaz7jlWAfwxVlEO23ehHqox9',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AiR4xP_pIst8rVaHJki_NSl18ykSvUlrCuHc7z5FsO-y6cofZs0Yt1rxrGuP',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AmQ4hD-p4os8bRZH5sx_9em1M2lS_YkqSiEcL36F8C_yKQpfpg1Y95ox7KjP',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AoTYJB_JgivczTbnhuAfVYkVUwlynalpasE8z54lEM8SySo_xq14l7rRDE3v',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AiF9S5I636zpjnNYOpdSMrw2NuY_zpRTv0I5UIP2HSiH6k8Qyx6lkE-SST0S',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AqH9yxK6XyxpDvPYukjSsjy2tma_ThTTP8K50AN2nagHas-QS54lEM8SybiS',
        'searchGuide=sg; __utma=156575163.978863046.1511865338.1512626144.1513047360.4; __utmz=156575163.1513047360.4.4.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; cmsad_170_0=0; historystock=600569; log=; v=AmM_AcTMPRbnYPEiTFlwmGKo9KwJWPYJMew7SpXAv0I51I1aHSiH6kG8y4Gk'
    ]

    def __init__(self):
        print "init StockDetailDailyCrawler..."
        self.__stock_detail_daily_dao = StockDetailDailyDao()

    def _byteify(self, data, ignore_dicts=False):
        # if this is a unicode string, return its string representation
        if isinstance(data, unicode):
            return data.encode('utf-8')
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [self._byteify(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self._byteify(key, ignore_dicts=True): self._byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
                }
        # if it's anything else, return it in its original form
        return data

    def __crawl_detail_data(self, stock_code):
        cookie = self.__cookies[random.randint(0, len(self.__cookies))]
        referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'

        proxy = Proxies()
        proxy.set_header('Cookie', cookie)
        proxy.set_header('Referer', referer)

        response = proxy.crawl_url(self.__detail_data_url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())
        json_str = soup.prettify()
        json_str = json_str.lstrip('quotebridge_v2_realhead_hs_%s_last(' % stock_code)
        json_obj = json.loads(json_str[:-2], object_hook=self._byteify)

        return json_obj.get('items')

    def __crawl_fund(self, stock_code):
        cookie = self.__cookies[random.randint(0, len(self.__cookies))]
        referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'

        proxy = Proxies()
        proxy.set_header('Cookie', cookie)
        proxy.set_header('Referer', referer)

        response = proxy.crawl_url(self.__fund_url % stock_code, is_get=True)

        soup = BeautifulSoup(response.read())
        return json.loads(soup.prettify(), object_hook=self._byteify)

    def __crawl(self, stock):
        print "crawl %s detail daily..." % stock.code
        detail_data = self.__crawl_detail_data(stock.code)
        fund_data = self.__crawl_fund(stock.code)

        stock_detail_daily = StockDetailDaily()
        stock_detail_daily.stock_id = stock.id
        stock_detail_daily.open_price = float(detail_data.get('7'))
        stock_detail_daily.close_price = float(detail_data.get('10'))
        stock_detail_daily.highest_price = float(detail_data.get('8'))
        stock_detail_daily.lowest_price = float(detail_data.get('9'))
        stock_detail_daily.trading_volume_rate = float(detail_data.get('1968584'))/100
        stock_detail_daily.pb_ratio = float(detail_data.get('592920'))
        stock_detail_daily.pe_ratio = float(detail_data.get('2034120'))
        stock_detail_daily.amplitude = float(detail_data.get('526792'))/100
        stock_detail_daily.market_value = float(detail_data.get('3541450'))
        stock_detail_daily.circulated_stock_value = float(detail_data.get('3475914'))
        stock_detail_daily.turnover = float(detail_data.get('19'))

        trading_volume = float(detail_data.get('13'))
        stock_detail_daily.trading_volume = trading_volume

        turnover = fund_data.get('title')['zlc'] + fund_data.get('title')['zlr']
        for fund in fund_data.get('flash'):
            if fund.get('name') == '\xe5\xa4\xa7\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#大单流出
                stock_detail_daily.large_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe4\xb8\xad\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#中单流出
                stock_detail_daily.mid_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xb0\x8f\xe5\x8d\x95\xe6\xb5\x81\xe5\x87\xba':#小单流出
                stock_detail_daily.small_out = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xb0\x8f\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#小单流入
                stock_detail_daily.small_in = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe4\xb8\xad\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#中单流入
                stock_detail_daily.mid_in = int(float(fund.get('sr')) / turnover * trading_volume)
            elif fund.get('name') == '\xe5\xa4\xa7\xe5\x8d\x95\xe6\xb5\x81\xe5\x85\xa5':#大单流入
                stock_detail_daily.large_in = int(float(fund.get('sr')) / turnover * trading_volume)

        self.__stock_detail_daily_dao.insert_detail_daily(stock_detail_daily)

    def crawl_all_stock(self):
        stock_dao = StockDao()
        all_stocks = stock_dao.query_all_stock()
        i = 1
        total = len(all_stocks)
        for stock in all_stocks.items():
            print "%d of %d stocks..." %(i, total)
            try:
                self.__crawl(stock[1])
            except:
                print "Unexpected error:", sys.exc_value

            sleep_time = random.randint(5, 20)
            print "sleep %d second...\n" % sleep_time
            time.sleep(sleep_time)

            i += 1


stockDetailDaily = StockDetailDailyCrawler()
stockDetailDaily.crawl_all_stock()