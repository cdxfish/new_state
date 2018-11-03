# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime

class CheckCollect(models.Model):
    _name = 'funenc_xa_station2.check_collect'
    _inherit = 'funenc_xa_station2.check_record'


    @api.model
    def get_action(self):
        user_id = self.env.user.dingtalk_user.id
        print(user_id)
        return {
            'name': '考评汇总',
            'type': 'ir.actions.client',
            'tag':'funenc_xa_check',
            'res_model': 'funenc_xa_station2.award_record',
            'context': self.env.context,
        }

    @api.model
    def get_group_2(self):
        if self.user_has_groups('funenc_xa_station2.table_evaluation_total'):
            return self.user_has_groups('funenc_xa_station2.table_evaluation_total')
        else:
            return

    @api.model
    def get_group_1(self):
        if self.user_has_groups('funenc_xa_station2.table_evaluation_record'):
            return self.user_has_groups('funenc_xa_station2.table_evaluation_record')
        else:
            return

    @api.model
    def get_group_3(self):
        if self.user_has_groups('funenc_xa_station2.table_reward_record'):
            return self.user_has_groups('funenc_xa_station2.table_reward_record')
        else:
            return

    @api.model
    def get_group_4(self):
        if self.user_has_groups('funenc_xa_station2.table_reward_total'):
            return self.user_has_groups('funenc_xa_station2.table_reward_total')
        else:
            return



    @api.model
    def check_record_method(self):
        # data = self.env['funenc_xa_station2.check_record'].search([]).mapped('job_number')
        # data1 = set(data)
        # data2 = list(data1)
        # list_temp = []
        #
        # for i, item in enumerate(data2):
        #
        #     count = self.env['funenc_xa_station2.check_record'].search_count([('job_number','=',item)])
        #     record = self.env['funenc_xa_station2.check_record'].search_read([('job_number','=',item)])[0]
        #     grade = self.env['funenc_xa_station2.check_record'].search_read([('job_number', '=', item)])
        #     sure_grede = sum(record1.get('sure_grede') for record1 in grade)
        #     record['comment_count'] = count
        #     record['mouth_grade'] = 100 + sure_grede
        #     list_temp.append(record)
        #
        # return list_temp

            return

    @api.model
    def search_record_method(self, date):

        startTime = datetime.datetime.strptime(date[:10], '%Y-%m-%d')
        date_one = (startTime + datetime.timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')
        record = {}

        date_time = self.env['funenc_xa_station2.check_record'].search_read([])
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







                # check_record_no = set(check_record. get('job_number') for check_record in date_list)
                #
                # data2 = list(check_record_no)
                #
                # for i, item in enumerate(data2):
                #
                #     count = self.env['funenc_xa_station2.check_record'].search_count([('job_number','=',item)])[0]

        return [record.get(key) for key in record]

