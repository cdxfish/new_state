# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class production_change_shifts(models.Model):
    _name = 'funenc_xa_station.production_change_shifts'
    _inherit = 'fuenc_station.station_base'
    _description = u'生产管理交接班'

    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',stirng='交班人')
    take_over_from_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',stirng='接班人')
    on_duty_time = fields.Datetime(string='当班时间')
    change_shifts_time = fields.Datetime(string='交班时间')
    #####
    take_over_from_time = fields.Datetime(string='接班时间')
    state = fields.Selection(selection=[('draft','草稿'),('change_shifts','交班'),('take_over_from','接班')],default="draft")

    # 值班站长
    # 工作情况字段
    before_on_duty = fields.Text(string='班前情况')
    complete_task = fields.Text(stirng='工作完成情况')
    after_work = fields.Text(string='班后总结')

    focus_of_handover = fields.Text(string='交接重点')

    # 行车值班员
    in_the_rough = fields.Text(string='未完成')


    @api.model
    def create_production_change_shifts(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.production_change_shifts',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '耗材出库编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.production_change_shifts',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def production_change_shifts_save(self):
        pass

    def submit(self):
        self.state = 'change_shifts'