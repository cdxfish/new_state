# -*- coding: utf-8 -*-
from odoo import models, fields, api


class arrange_order(models.Model):
    '''
     班次管理
    '''

    _name = 'funenc_xa_station.arrange_order'
    _description = u'班次管理'

    name = fields.Char(string='班次名称', required= True)
    time = fields.Char(string='班次时间')
    work_time = fields.Char(string='工作时长')
    start_work_time = fields.Datetime(string='上班时间', required= True)
    end_work_time = fields.Datetime(string='下班时间', required= True)
    end_time_select = fields.Selection(string='下班日期',selection=[('same_day','当日'),('next_day','次日')],default='same_day')


    @api.constrains('start_work_time','end_work_time')
    def compute_work_time(self):

        return self