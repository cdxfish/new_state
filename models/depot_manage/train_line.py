# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class TrainLine(models.Model):
    '''
    线路
    '''
    _name = 'train_line.train_line'

    name = fields.Char(string='线别', required=True)
    train_ids_rel = fields.Integer('ids')
    c_time = fields.Date(
        string="创建日期", default=datetime.now().strftime("%Y-%m-%d"))
    remark = fields.Char(string='备注', help='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "线别唯一")]

    station_ids = fields.One2many(
        comodel_name='train_station.train_station', inverse_name='line_id', string='')

    line_json = fields.Text(string='正线图json')

    @api.multi
    def edit_click(self):
        return {
            "type": "ir.actions.client",
            "tag": 'chart_view',
        }
