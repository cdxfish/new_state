# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime


class GoodDeedsSummary(models.Model):
    _name = 'funenc_xa_station.good_deeds_summary'

    @api.model
    def init_methods_action(self):
        lis = []
        type =  self.env['funenc_xa_station.good_deeds_type'].search_read([],['good_type'])
        for i in type:
            dic = {}
            count = self.env['fuenc_station.good_deeds'].search([('type','=',i.get('id'))])
            dic['good_deeds_type'] = i.get('good_type')
            dic['frequency'] = len(count)
            lis.append(dic)
        return lis

    @api.model
    def get_department(self):
        lis = []

        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('department_hierarchy','=',1)])
        for i in department:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis

    @api.model
    def get_line(self,date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id','=',date)],['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('parentid','=',department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis

    @api.model
    def get_site(self,date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id','=',date)],['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('parentid','=',department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis

    @api.model
    def search_record(self,department,line,site,date_time):
        start_time_one = date_time[0][:10]
        d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        open_time = d + delta
        start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')

        end_time_one = date_time[1][:10]
        d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
        delta_1 = datetime.timedelta(days=1)
        open_time_1 = d_1 + delta_1
        end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')

        lis = []
        change = []
        record = self.env['fuenc_station.good_deeds'].search([('site_id','=',site),('open_time','>',start_new),('open_time','<',end_new)])
        for i in record:
            dic = {}
            if i.type.good_type not in change:
                dic['good_deeds_type'] = i.type.good_type
                count = self.env['fuenc_station.good_deeds'].search([('type','=',i.type.id)])
                dic['frequency'] = len(count)
                lis.append(dic)
            change.append(i.type.good_type)




        return lis





