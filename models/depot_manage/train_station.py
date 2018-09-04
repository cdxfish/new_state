# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainStation(models.Model):
    '''
    站点/站间区域
    '''
    _name = 'train_station.train_station'
    _rec_name = 'name'

    train_line_more_id = fields.Many2one(
        'train_line_more.train_line_more', string="id", ondelete='cascade')
    line_id = fields.Many2one(comodel_name='train_line.train_line', string='')
    name = fields.Char(string="站点", required=False)
    station_type = fields.Selection([
        ('cz', '车站'), ('cc', '出入段线'), ('qy', '站间区域')
    ], '类型', default='cz')
    up_link = fields.Many2one('electric_block.electric_block', string='上行供电分区编号',
                              domain="[('line_id', '=', line_id),('direction','=','sx')]"
                              )
    down_link = fields.Many2one('electric_block.electric_block', string='下行供电分区编号',
                                domain="[('line_id', '=', line_id),('direction','=','xx')]"
                                )
    assist_lines = fields.One2many(comodel_name="assist_line.assist_line",
                                   inverse_name="area_ids",
                                   string="辅助线",
                                   required=False)
    deparment_id = fields.Many2one(
        comodel_name='cdtct_dingtalk.cdtct_dingtalk_department',
        relation="station_deparment_rel",
        string='维护部门', ondelete='cascade')
    index = fields.Integer(string='顺序index')

    # @api.model
    # def create(self, vals):
    #
    #     train_id = super(TrainStation, self).create(vals)
    #     key_manage_values = {}
    #     key_manage_values['line_id'] = train_id.line_id.id
    #     key_manage_values['ascription_site_id'] = train_id.id
    #     self.env['funenc.xa.station.key.manage'].create(key_manage_values)
    #
    #     return train_id

