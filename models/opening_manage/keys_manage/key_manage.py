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
	
	# 借用钥匙
	@api.model
	def borrow_key(self):
		return {
			'name': '钥匙借用',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'fuenc.station.borrow.record',
			'context': self.env.context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	# 归还钥匙
	@api.model
	def return_key(self):
		return {
			'name': '钥匙归还',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'fuenc.station.borrow.record',
			'context': self.env.context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	# 借用记录
	@api.model
	def borrow_record(self):
		view_tree = self.env.ref('fuenc_station.fuenc_station_borrow_record_list').id
		view_form = self.env.ref('fuenc_station.fuenc_station_borrow_record_form').id
		return {
			'name': '借用记录',
			"type": "ir.actions.act_window",
			"res_model": "fuenc.station.borrow.record",
			"views": [[view_tree, "tree"], [view_form, "form"]],
			# "domain": [()],
		}
