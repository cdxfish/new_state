# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class operation_log(models.Model):
    _name = 'funenc_xa_station.operation_log'
    _description = u'操作日志'
    _order = 'id desc'


    _inherit = ['mail.thread', 'mail.activity.mixin']


class InheritMailMessage(models.Model):
    _inherit = 'mail.message'


    def detail(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_operation_log_form').id
        return {
            'name': '日志查看',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.operation_log',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
