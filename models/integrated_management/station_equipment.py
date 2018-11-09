# -*- coding: utf-8 -*-
from odoo import models, fields, api


class station_equipment(models.Model):
    _name = 'funenc_xa_station.station_equipment'
    _description = u'车站设备'

    name = fields.Char(string='设备名称')
    count = fields.Integer(string='设备数量')
    position = fields.Char(string='设备位置')
    remarks = fields.Text(string='备注')

    station_summary_id = fields.Many2one('funenc_xa_station.station_summary',string='车站详情')


    @api.model
    def create_station_equipment(self):
        context = dict(self.env.context or {})
        return {
            'name': '创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.station_equipment',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.station_equipment',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def station_equipment_save(self):
        pass