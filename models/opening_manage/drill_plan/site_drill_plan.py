# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class site_drill_plan(models.Model):
    _name = 'funenc_xa_station.site_drill_plan'
    _description = u'站点演练详情'


    @api.model
    def create_site_drill_plan(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.site_drill_plan',
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
            'res_model': 'funenc_xa_station.site_drill_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def site_drill_plan_save(self):
        pass