# -*- coding: utf-8 -*-
import datetime

import odoo.exceptions as msg
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
        start_work_time = datetime.datetime.strptime(self.start_work_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)
        end_work_time = datetime.datetime.strptime(self.end_work_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)

        # seconds
        if (end_work_time- start_work_time).days < 0:
            end_time_select = '次日'
        else:
            end_time_select = '当日'
        # format(float((end_work_time - start_work_time).seconds) / float((60 * 60)), '.2f')
        work_time = round( (end_work_time - start_work_time).seconds / (60 * 60), 2)
        self.work_time = str(work_time) + 'h'
        self.time = '{}-{} ({})'.format(self.start_work_time[11:-3], self.end_work_time[11:-3], end_time_select)

    def create_arrange_order(self):
        return {
            'name': '新增班次',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.arrange_order',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def arrange_order_edit(self):
        return {
            'name': '班次详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.arrange_order',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def arrange_order_delete(self):

        self.env['funenc_xa_station.arrange_order'].search([('id', '=', self.id)]).unlink()


