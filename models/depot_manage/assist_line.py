# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AssistLine(models.Model):
    '''
    辅助线路
    '''
    _name = 'assist_line.assist_line'

    train_block_ids = fields.Many2one(
        'train_block.train_block', string='ids_train_block', ondelete='cascade')
    area_ids = fields.Many2one(
        comodel_name='train_station.train_station', string='', ondelete='cascade')

    name = fields.Char(string='辅助线名称')
    assist_type = fields.Selection(string="辅助线供电分区", selection=[
        ('qt', '其他'),
        ('sx', '上行'),
        ('xx', '下行'),
        ('fz_down', '辅助线下行'),
        ('fz_up', '辅助线上行'),
        ('none', '无')], required=True)
    electric_block = fields.Many2one(
        'electric_block.electric_block', string='供电区域编号',)  # 待删除..
    electric_zone_code = fields.Many2one(
        'electric_block.electric_block', string='供电区域编号', domain="[('line_id', '=', area_ids.line_id)]")

    @api.onchange('electric_block')
    def onchange_electric_block(self):
        '''
        辅助线线别筛选
        :return: domain赛选器
        '''
        line_id = self.train_block_ids.train_line_more_id.line_id.id
        electric_block = self.env['electric_block.electric_block'].search([
            ('line_id', '=', line_id)
        ]).mapped('id')
        return {'domain': {
            'electric_block': [('id', 'in', electric_block)],
        }
        }
