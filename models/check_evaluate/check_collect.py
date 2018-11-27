# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime

class CheckCollect(models.Model):
    _name = 'funenc_xa_station.check_collect'
    _inherit = 'funenc_xa_station.check_record'


    @api.model
    def get_action(self):
        user_id = self.env.user.dingtalk_user.id
        print(user_id)
        return {
            'name': '考评汇总',
            'type': 'ir.actions.client',
            'tag':'funenc_xa_check',
            'res_model': 'funenc_xa_station.award_record',
            'context': self.env.context,
        }

    @api.model
    def get_group_2(self):
        if self.user_has_groups('funenc_xa_station.table_evaluation_total'):
            return self.user_has_groups('funenc_xa_station.table_evaluation_total')
        else:
            return

    @api.model
    def get_group_1(self):
        if self.user_has_groups('funenc_xa_station.table_evaluation_record'):
            return self.user_has_groups('funenc_xa_station.table_evaluation_record')
        else:
            return

    @api.model
    def get_group_3(self):
        if self.user_has_groups('funenc_xa_station.table_reward_record'):
            return self.user_has_groups('funenc_xa_station.table_reward_record')
        else:
            return

    @api.model
    def get_group_4(self):
        if self.user_has_groups('funenc_xa_station.table_reward_total'):
            return self.user_has_groups('funenc_xa_station.table_reward_total')
        else:
            return

    @api.model
    def search_site(self, date):
        site_parent = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                       ['departmentId'])
        site_son = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
            [('parentid', '=', site_parent[0]['departmentId'])], ['name'])

        return site_son

    #获取当前线路
    @api.model
    def add_count_line(self):
        line = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy', '=', 2)],
                                                                               ['id', 'name'])
        return line



    @api.model
    def check_record_method(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        startTime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_one = (startTime + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        record = {}
        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.id
        date_time = self.env['funenc_xa_station.check_record'].search_read([('site_id','=',ids)])
        date_list = [check_record for check_record in date_time if check_record.get('check_time')[:7] == date_one[:7]]

        for list1 in date_list:
            record[list1.get('job_number')] = list1
        # count  得分
        for list2 in record:
            i = 0
            fs = 0
            for list3 in date_list:
                if list2 == list3.get('job_number'):
                    i = i +1
                    fs = fs + list3.get('sure_grede')
            record[list2].update({'comment_count':i})
            record[list2].update({'mouth_grade': fs + 100})
            record[list2].update({'line_id':list3.get('line_id')[1]})
            record[list2].update({'site_id':list3.get('site_id')[1]})
            record[list2].update({'staff':list3.get('staff')[1]})

        return [record.get(key) for key in record]
    @api.model
    def search_record_method(self, date,line,site,person_id):

        startTime = datetime.datetime.strptime(date[:10], '%Y-%m-%d')
        date_one = (startTime + datetime.timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')
        record = {}
        if not person_id:
            date_time = self.env['funenc_xa_station.check_record'].search_read([('site_id','=',site)])
            date_list = [check_record for check_record in date_time if check_record.get('check_time')[:7] == date_one[:7]]

            for list1 in date_list:
                record[list1.get('job_number')] = list1
            # count  得分
            for list2 in record:
                i = 0
                fs = 0
                for list3 in date_list:
                    if list2 == list3.get('job_number'):
                        i = i +1
                        fs = fs + list3.get('sure_grede')
                record[list2].update({'comment_count':i})
                record[list2].update({'mouth_grade': fs + 100})
                record[list2].update({'line_id':list3.get('line_id')[1]})
                record[list2].update({'site_id':list3.get('site_id')[1]})
        elif person_id:
            date_time = self.env['funenc_xa_station.check_record'].search_read(['|',('staff', '=', person_id),
                                                                                   ('check_number', '=', person_id)])
            date_list = [check_record for check_record in date_time if
                         check_record.get('check_time')[:7] == date_one[:7]]

            for list1 in date_list:
                record[list1.get('job_number')] = list1
            # count  得分
            for list2 in record:
                i = 0
                fs = 0
                for list3 in date_list:
                    if list2 == list3.get('job_number'):
                        i = i + 1
                        fs = fs + list3.get('sure_grede')
                record[list2].update({'comment_count': i})
                record[list2].update({'mouth_grade': fs + 100})
                record[list2].update({'line_id': list3.get('line_id')[1]})
                record[list2].update({'site_id': list3.get('site_id')[1]})
                record[list2].update({'staff': list3.get('staff')[1]})


        return [record.get(key) for key in record]

    @api.model
    def get_line_self(self):
        '''
        自动获取当前线路的数据
        :return:
        '''
        if self.env.user.id ==1:
            return
        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.ids
        return self.env.user.dingtalk_user.id

    @api.model
    def get_site_self(self):
        '''
        自动获取当前站点的数据
        :return:
        '''
        if self.env.user.id ==1:
            return

        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.name
        return ids



