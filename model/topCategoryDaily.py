# -*- coding: UTF-8 -*-
# 每日板块排名

class TopCategoryDaily:

    def __init__(self, id, category_id, ranking, net_inflow, rise, fall):
        self.id = id
        self.category_id = category_id
        self.ranking = ranking
        self.net_inflow = net_inflow
        self.rise = rise
        self.fall = fall
