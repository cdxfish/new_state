# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyType(models.Model):
	_name = 'funenc.xa.station.key.type'
	_rec_name = "name"
	
	name = fields.Char(string='钥匙类型', required=True)
	remarks = fields.Text(string='备注')

	@api.multi
	def write(self, vals):

		return
	
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
