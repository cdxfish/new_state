# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConsumablesSummary(models.Model):

    _name = 'funenc_xa_station.consumables_summary'

    @api.model
    def init_methods_action(self):
        lis= []
        record = self.env['funenc_xa_station.consumables_type'].search([])
        for i in record:
            count_one = 0
            dic = {}
            dic['consumables_type'] = i.consumables_type
            count = self.env['funenc_xa_station.consumables_inventory'].search([("consumables_type", "=", i.id)])
            for count_self in count:
                count_one += count_self.inventory_count
            dic['inventory'] = count_one
            lis.append(dic)
        return lis


    @api.model
    def get_department(self):
        lis = []

        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('department_hierarchy', '=', 1)])
        for i in department:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis

    @api.model
    def get_line(self, date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                      ['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis

    @api.model
    def get_site(self, date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                      ['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis

    @api.model
    def search_record_consumables(self,department,line,site,options):
        lis= []
        op = [opt for opt in options if type(opt).__name__ == 'list']


        record = self.env['funenc_xa_station.consumables_inventory'].search([('consumables_type','=',2)])
        sure_list = []
        record_count = 0
        for re in record:
            if re.consumables_type.consumables_type not in sure_list:
                dic = {}
                dic['consumables_type'] = re.consumables_type.consumables_type
                for count in record:
                    record_count += count.inventory_count
                dic['inventory'] = record_count
                sure_list.append(re.consumables_type.consumables_type)
                lis.append(dic)
        return lis


        # record = self.env['funenc_xa_station.consumables_type'].search([])
        # for i in record:
        #     count_one = 0
        #     count = self.env['funenc_xa_station.consumables_inventory'].search([("consumables_type", "=", i.id)])
        #     site_record = self.env['funenc_xa_station.consumables_inventory'].search(
        #                                     [("inventory_department_id", "=", site)])
        #     for site_id in site_record:
        #         dic = {}
        #         site_id.consumables_type.consumables_type
        #     for count_self in count:
        #         count_one += count_self.inventory_count
        #     dic['inventory'] = count_one
        #     dic['consumables_type'] = i.consumables_type
        #     lis.append(dic)
        # return lis
