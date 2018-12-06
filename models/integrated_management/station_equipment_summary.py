# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StationEquipmentSummary(models.Model):
    _name = 'funenc_xa_station.station_equipment_summary'

    def init_methods_action(self):
        return

