# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyDetail(models.Model):
	_name = 'fuenc.station.key.detail'
	
	name = fields.Char(string='钥匙名称')
	line_id = fields.Char(string='选择线路')
	ascription_site_id = fields.Char(string='归属站点')
	key_type_id = fields.Many2one('fuenc.station.key.type', string='钥匙类型')
	key_no = fields.Text(string='钥匙编号')
	key_position = fields.Char(string='对应位置')
	is_main = fields.Selection(selection=[('yes', '主'), ('no', '备')], string='主备情况')
	
	# borrow_user_id = fields.Many2one('res.users',string='借用人')
	
	@api.model
	def create(self, vals):
		if vals.get('key_no'):
			key_nos = vals.get('key_no').split('\n')
			for key_no in key_nos:
				if key_no:
					vals['key_no'] = key_no
					record = super(KeyDetail, self).create(vals)
		return record
	
	@api.model
	def get_data_test(self):
		print('ok')
