# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GoodDeedsSummary(models.Model):
    _name = 'funenc_xa_station.good_deeds_summary'

    def init_methods_action(self):
        return

