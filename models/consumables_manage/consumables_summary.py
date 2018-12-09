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
    def search_record_consumables(self,**kw):
        if kw:
            lis= []
            dic_department_id = {}
            # 构建搜索domain
            if kw.get('department'):
                dic_department_id[1] = kw.get('department')  #部门
            if kw.get('line'):
                dic_department_id.clear()
                dic_department_id[2] = kw.get('line')  # 线路
            if kw.get('site'):
                dic_department_id.clear()
                dic_department_id[3] = kw.get('site') # 站点
            if dic_department_id:
                department_hierarchy = list(dic_department_id.keys())[0]

                if department_hierarchy == 1:
                    department_tmp = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(dic_department_id[1])
                    line_ids =self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('parentid', '=', department_tmp.departmentId)])
                    tmp_site_ids = []
                    for line_id in line_ids:
                        site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                            [('parentid', '=', line_id.departmentId)]).ids
                        tmp_site_ids = tmp_site_ids +site_ids

                    domain_ids = [department_tmp.id] + line_ids.ids + tmp_site_ids
                    domain = [('inventory_department_id', 'in', domain_ids)]
                elif department_hierarchy == 2: #搜索为线路
                    department_tmp = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(dic_department_id[2])
                    site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('parentid', '=', department_tmp.departmentId)]).ids
                    domain_ids = [department_tmp.id] + site_ids
                    domain = [('inventory_department_id', 'in', domain_ids)]
                else: #搜索为站点

                    domain_ids = [dic_department_id[3]]
                    domain = [('inventory_department_id', 'in', domain_ids)]



            else:
                search_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('department_hierarchy', '=',3)]).ids
                domain = [('inventory_department_id','in',search_department_ids)]

            if kw.get('consumables_type'):
                consumables_type = kw.get('consumables_type')[len(kw.get('consumables_type'))-1]
                domain.append(('consumables_type','=',consumables_type))

            consumables_inventory_ids = self.env['funenc_xa_station.consumables_inventory'].search_read(domain,['consumables_type','inventory_count'])
            # 构建 耗材类型数据
            consumables_type_dic = {}
            for consumables_inventory_id in consumables_inventory_ids:
                consumables_type_dic[consumables_inventory_id.get('consumables_type')[0]] = consumables_inventory_id.get('consumables_type')[1]
            table_data = []
            for key in list(consumables_type_dic.keys()):
                count = 0
                for value in consumables_inventory_ids:
                    if key == value.get('consumables_type')[0]:
                        count = count + value.get('inventory_count')
                table_data.append(
                    {
                        'consumables_type':consumables_type_dic[key],
                        'inventory':count
                    }
                )
            return table_data
        else:
            return []


