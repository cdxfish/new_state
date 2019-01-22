# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyType(models.Model):
	_name = 'funenc.xa.station.key.type'
	_rec_name = "name"
	_inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
	_description = '钥匙管理钥匙类型'
	
	name = fields.Char(string='钥匙类型', required=True, track_visibility='onchange')
	prent_id = fields.Many2one('funenc.xa.station.key.type', string='父钥匙分类', track_visibility='onchange')
	child_ids = fields.One2many('funenc.xa.station.key.type', 'prent_id', string='子钥匙分类')
	remarks = fields.Text(string='备注', track_visibility='onchange')

	
	# 创建钥匙类型
	@api.model
	def create_key_type(self):
		return {
			'name': '钥匙类型创建',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'funenc.xa.station.key.type',
			'context': self.env.context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	def key_type_edit(self):
		return {
			'name': '钥匙类型编辑',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'funenc.xa.station.key.type',
			'context': self.env.context,
			'flags': {'initial_mode': 'edit'},
			'res_id': self.id,
			'target': 'new',
		}
	
	def key_type_delete(self):
		self.env['funenc.xa.station.key.type'].search([('id', '=', self.id)]).unlink()

	# 用来测试层级选择
	@api.model
	def get_equipment_class(self, id=False):
		'''
        获取分组
        :return:
        '''
		rst = []
		class_a = self.env['funenc.xa.station.key.type'].search_read([('prent_id', '=', id)],
																			 fields=['child_ids', 'name'])
		for record in class_a:
			vals = {
				'value': record['id'],
				'label': record['name'],
			}
			children = self.get_equipment_class(record['id'])
			if children:
				vals['children'] = children
			rst.append(vals)
		return rst
