# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StationEquipmentSummary(models.Model):
    _name = 'funenc_xa_station.station_equipment_summary'

    def init_methods_action(self):
        return

    @api.model
    #获取所有车站设备的信息
    def get_equipment_name(self):
        lis = []
        all_record = self.env['funenc_xa_station.station_equipment'].search([])
        for record in all_record:
            dic = {}
            dic['equipment_fname']=record.name

            dic['equipment_count']=record.count
            lis.append(dic)

        return lis

    @api.model
    #获取所有的设备名称的集合
    def get_name_all(self):
        lis = []
        all_record = self.env['funenc_xa_station.station_equipment'].search([])
        for record in all_record:
            dic = {}
            dic['name']=record.name

            dic['id']=record.count
            lis.append(dic)

        return lis





