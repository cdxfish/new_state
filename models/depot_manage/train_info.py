# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainInfo(models.Model):
    '''
    车辆信息
    '''
    _name = 'train_info.train_info'

    motor_train_ids = fields.Many2one(comodel_name="construction.dispatch", string="ids", required=False, )
    train_line_id = fields.Many2one(comodel_name="train_line.train_line", string="线路", required=False, )
    train_type = fields.Char('车型')
    train_num = fields.Char('编号')
    train_start_location = fields.Char('出发地点')
    train_run_location = fields.Char('运行地点')
    train_return_location = fields.Char('返回地点')

    @api.model
    def create(self, vals):
        context = self._context or {}
        ids = context.get('active_ids', [])
        if len(ids) > 0:
            ids = ids[0]
            vals['line_ids'] = ids
        scrap = super(TrainInfo, self).create(vals)
        self.env['construction.dispatch'].search([('id', '=', ids)]).is_invisible = False
        return scrap
