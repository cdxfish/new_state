# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AwardCollect(models.Model):
    _name = 'funenc_xa_station.award_collect'
    # _inherit = 'funenc_xa_station.award_record'

    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    jobnumber = fields.Char(string='工号')
    staff = fields.Char(string='员工')
    position = fields.Char(string='职位')


    @api.model
    def award_record_method(self):
        data = self.env['funenc_xa_station.award_record'].search([]).mapped('jobnumber')
        data1 = set(data)
        data2 = list(data1)
        list_temp = []

        for i, item in enumerate(data2):

            count = self.env['funenc_xa_station.award_record'].search_count([('jobnumber','=',item)])
            record = self.env['funenc_xa_station.award_record'].search_read([('jobnumber','=',item)])[0]
            grade = self.env['funenc_xa_station.award_record'].search_read([('jobnumber', '=', item)])
            sure_grede = sum(record1.get('award_money') for record1 in grade)
            record['comment_count'] = count
            record['award_money'] = sure_grede
            list_temp.append(record)

        return list_temp