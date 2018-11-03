# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
from ..get_domain import get_domain

class BreakLogManage(models.Model):
    _name = 'funenc_xa_station2.break_log_manage'
    _inherit = 'fuenc_station.station_base'

    position = fields.Char(string='位置')
    apply_time =fields.Date(string='申请时间')
    break_details = fields.Text(string='故障描述')
    before_break_img = fields.Binary(string='故障图片')
    state =fields.Selection([('one','已修复'),('zero','未处理')],string='状态',default='zero')
    repair_time = fields.Datetime(string='修复时间')
    repair_manufacturer = fields.Char(string='修复厂家')
    after_break_img =fields.Binary(string='修复后照片')

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station2.break_log_manage_tree').id
        return {
            'name': '故障标识管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station2.break_log_manage',
            'context': self.env.context,
        }

    def create_new_record(self):
        view_form = self.env.ref('funenc_xa_station2.break_log_manage_form').id
        return {
            'name': '标识报修',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station2.break_log_manage',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def onchange_change(self):
        values = {
            'state': self.state,
        }
        self.state = self.env.context.get('state', 'one')
        self.env['funenc_xa_station2.break_log_manage'].write(values)

        view_form = self.env.ref('funenc_xa_station2.break_log_manage_form_form').id
        return {
            'name': '标识报修',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station2.break_log_manage',
            'context': self.env.context,
            'res_id': self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def break_record_selete(self):
        self.unlink()

    def onchange_record(self):
        view_form = self.env.ref('funenc_xa_station2.break_log_manage_form').id
        return {
            'name': '标识报修',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station2.break_log_manage',
            'context': self.env.context,
            'res_id': self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }
