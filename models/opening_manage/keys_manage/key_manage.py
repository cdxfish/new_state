# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyManage(models.Model):
	_name = 'fuenc.station.key.manage'
	
	line_id = fields.Char(string='线路')
	ascription_site_id = fields.Char(string='归属站点')
	key_type_id = fields.Char(string='钥匙类型')
	master_number = fields.Integer(string='主钥匙数量')
	copy_number = fields.Integer(string='副钥匙数量')
	key_total = fields.Integer(string='钥匙总量')
	borrow_number = fields.Integer(string='借出数量')
	destroy_number = fields.Integer(string='损耗数量')
	
	# 创建钥匙
	@api.model
	def create_key(self):
		return {
			'name': '钥匙创建',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'fuenc.station.key.detail',
			'context': self.env.context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
