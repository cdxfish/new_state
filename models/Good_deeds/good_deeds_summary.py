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
    def search_record(self,**kw):
        # 只选择部门的返回结果
        if kw.get('department') and not kw.get('line') and not kw.get('site') and not kw.get('date_time') and not kw.get('good_type'):
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('department'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
                site_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
                    [('id', '=', name_id.id)],['departmentId'])
                site_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', site_name[0].get('departmentId'))])
                for site_children in site_id:
                    lis.append(site_children.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门和类型返回结果
        elif kw.get('department') and not kw.get('line') and not kw.get('site') and not kw.get('date_time') and kw.get('good_type'):
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('department'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
                site_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
                    [('id', '=', name_id.id)],['departmentId'])
                site_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', site_name[0].get('departmentId'))])
                for site_children in site_id:
                    lis.append(site_children.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('type','=',kw.get('good_type'))])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门和时间返回结果
        elif kw.get('department') and not kw.get('line') and not kw.get('site') and kw.get('date_time') and not kw.get('good_type'):
            #获取开始的时间
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            #获取结束的时间
            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('department'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
                site_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
                    [('id', '=', name_id.id)],['departmentId'])
                site_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', site_name[0].get('departmentId'))])
                for site_children in site_id:
                    lis.append(site_children.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('open_time','>',start_new),('open_time','<',end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门,时间,类型返回结果
        elif kw.get('department') and not kw.get('line') and not kw.get('site') and kw.get('date_time') and kw.get('good_type'):
            #获取开始的时间
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            #获取结束的时间
            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('department'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
                site_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
                    [('id', '=', name_id.id)],['departmentId'])
                site_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', site_name[0].get('departmentId'))])
                for site_children in site_id:
                    lis.append(site_children.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('type','=',kw.get('good_type'))
                                                                     ,('open_time','>',start_new),('open_time','<',end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        #只选择部门 分部 的返回结果
        elif kw.get('department') and kw.get('line') and not kw.get('site') and not kw.get('date_time') and not kw.get('good_type'):
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('line'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门 分部 和类型 的返回结果
        elif kw.get('department') and kw.get('line') and not kw.get('site') and not kw.get('date_time') and kw.get('good_type'):
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('line'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('type','=',kw.get('good_type'))])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门 分部和时间 的返回结果
        elif kw.get('department') and kw.get('line') and not kw.get('site') and kw.get('date_time') and not kw.get('good_type'):
            #获取开始的时间
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            #获取结束的时间
            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('line'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('open_time','>',start_new),('open_time','<',end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择部门 分部,时间,类型 的返回结果
        elif kw.get('department') and kw.get('line') and not kw.get('site') and kw.get('date_time') and kw.get('good_type'):
            #获取开始的时间
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            #获取结束的时间
            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')
            lis = []
            department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', kw.get('line'))],
                                                                                          ['departmentId'])
            name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id[0].get('departmentId'))])
            for name_id in name:
                lis.append(name_id.id)
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('type','=',kw.get('good_type')),
                                                                  ('open_time','>',start_new),('open_time','<',end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        #只选择 部门 分部 站点的返回结果
        elif kw.get('department') and kw.get('line') and kw.get('site') and not kw.get('date_time') and not kw.get('good_type'):
            lis = []
            lis.append(kw.get('site'))
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        # 只选择 部门 分部 站点 类型的返回结果
        elif kw.get('department') and kw.get('line') and kw.get('site') and not kw.get('date_time') and kw.get('good_type'):
            lis = []
            lis.append(kw.get('site'))
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),('type','=',kw.get('good_type'))])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        #所有的部门都选择的情况
        elif kw.get('department') and kw.get('line') and kw.get('site') and kw.get('date_time') and not kw.get('good_type'):
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')

            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')

            lis = []
            lis.append(kw.get('site'))
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis),
                                                                  ('open_time','>',start_new),('open_time','<',end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res
        #所有的都选择
        elif kw.get('department') and kw.get('line') and kw.get('site') and kw.get('date_time') and kw.get('good_type'):
            start_time_one = kw.get('date_time')[0][:10]
            d = datetime.datetime.strptime(start_time_one, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            open_time = d + delta
            start_new = open_time.strftime('%Y-%m-%d %H:%M:%S')

            end_time_one = kw.get('date_time')[1][:10]
            d_1 = datetime.datetime.strptime(end_time_one, '%Y-%m-%d')
            delta_1 = datetime.timedelta(days=1)
            open_time_1 = d_1 + delta_1
            end_new = open_time_1.strftime('%Y-%m-%d %H:%M:%S')

            lis = []
            lis.append(kw.get('site'))
            res = []
            change = []
            record = self.env['fuenc_station.good_deeds'].search([('site_id', 'in', lis), ('type','=',kw.get('good_type')),
                                                                  ('open_time', '>', start_new), ('open_time', '<', end_new)])
            for i in record:
                dic = {}
                if i.type.good_type not in change:
                    dic['good_deeds_type'] = i.type.good_type
                    count = self.env['fuenc_station.good_deeds'].search([('type', '=', i.type.id)])
                    dic['frequency'] = len(count)
                    res.append(dic)
                change.append(i.type.good_type)
            return res

    @api.model
    def get_good_deeds_types(self):
        '''
        获取好人好的色所有类型
        :return:
        '''
        lis = []
        all_record = self.env['funenc_xa_station.good_deeds_type'].search([])
        for record in all_record:
            dic = {}
            dic['name'] =record.good_type
            dic['id'] =record.id
            lis.append(dic)

        return lis







