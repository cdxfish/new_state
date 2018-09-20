# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime

class CheckCollect(models.Model):
    _name = 'funenc_xa_station.check_collect'
    _inherit = 'funenc_xa_station.check_record'

    @api.model
    def check_record_method(self):
        # data = self.env['funenc_xa_station.check_record'].search([]).mapped('job_number')
        # data1 = set(data)
        # data2 = list(data1)
        # list_temp = []
        #
        # for i, item in enumerate(data2):
        #
        #     count = self.env['funenc_xa_station.check_record'].search_count([('job_number','=',item)])
        #     record = self.env['funenc_xa_station.check_record'].search_read([('job_number','=',item)])[0]
        #     grade = self.env['funenc_xa_station.check_record'].search_read([('job_number', '=', item)])
        #     sure_grede = sum(record1.get('sure_grede') for record1 in grade)
        #     record['comment_count'] = count
        #     record['mouth_grade'] = 100 + sure_grede
        #     list_temp.append(record)
        #
        # return list_temp
            return [{'line_id':'0'}]

    @api.model
    def search_record_method(self, date):
        judge = self.env['funenc_xa_station.check_record'].search([]).mapped('check_time')
        list_temp = []
        for i in judge:
            if str(i)[:7] == date[:7]:
                date_time = self.env['funenc_xa_station.check_record'].search_read([])
                date_list = [check_record for check_record in date_time if check_record.get('check_time')[:7] == date[:7]]
                check_record_no = set(check_record. get('job_number') for check_record in date_list)

                data2 = list(check_record_no)

                for i, item in enumerate(data2):

                    count = self.env['funenc_xa_station.check_record'].search_count([('job_number','=',item)])
                    record = self.env['funenc_xa_station.check_record'].search_read([('job_number','=',item)])[0]
                    grade = self.env['funenc_xa_station.check_record'].search_read([('job_number', '=', item)])
                    sure_grede = sum(record1.get('sure_grede') for record1 in grade)
                    record['comment_count'] = count
                    record['mouth_grade'] = 100 + sure_grede
                    list_temp.append(record)

        return list_temp


