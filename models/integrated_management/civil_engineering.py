# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ..get_domain import get_domain

class CivilEngineering(models.Model):
    _name = 'funenc_xa_station.civil_engineering'
    _description = u'土建结构'
    _inherit = 'fuenc_station.station_base'
    # _rec_name = ''

    essential_information_ids = fields.One2many('funenc_xa_station.essential_information','civil_engineering_id',string='基本信息')
    private_channel_ids = fields.One2many('funenc_xa_station.private_channel','civil_engineering_id',string='专用通道信息')
    contact_re = fields.Many2one('funenc_xa_station.station_summary',string='关联车站详情')

    #用来筛选当前站点
    def search_record_local(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_civil_engineering_list').id
        return {
            'name': '土建结构',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.civil_engineering',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
        }


class EssentialInformation(models.Model):
    _name = 'funenc_xa_station.essential_information'
    _description = u'基本信息'
    _rec_name = 'type'

    type = fields.Char(string= '类别')
    content = fields.Text(string= '内容')

    civil_engineering_id = fields.Many2one('funenc_xa_station.civil_engineering',string='出口信息')


class PrivateChannel(models.Model):
    _name = 'funenc_xa_station.private_channel'
    _description = u'专用通道信息'
    _rec_name = 'name'

    name = fields.Char(string='通道名称')
    channel_width = fields.Char(string='宽度(m)')
    remarks = fields.Text(string='说明')

    civil_engineering_id = fields.Many2one('funenc_xa_station.civil_engineering', string='出口信息')

