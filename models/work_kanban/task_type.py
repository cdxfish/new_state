# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class task_type(models.Model):
    _name = 'funenc_xa_station.task_type'
    _description = u'任务类型'

    name = fields.Char(string='任务事件名称',required=True)
    remarks = fields.Char(string='备注')



    @api.model
    def create_task_type(self):
        context = dict(self.env.context or {})
        return {
            'name': '任务类型创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.task_type',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '任务类型编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.task_type',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def task_type_save(self):
        pass