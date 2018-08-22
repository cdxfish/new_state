# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyDetail(models.Model):
	_name = 'fuenc.station.key.detail'
	_rec_name = 'key_no'
	
	name = fields.Char(string='钥匙名称')
	line_id = fields.Char(string='选择线路')
	ascription_site_id = fields.Char(string='归属站点')
	key_type_id = fields.Many2one('fuenc.station.key.type', string='钥匙类型')
	key_no = fields.Text(string='钥匙编号')
	key_position = fields.Char(string='对应位置')
	state_now = fields.Char(string='当前状态')
	is_main = fields.Selection(selection=[('yes', '主'), ('no', '备')], string='主备情况')
	
	# borrow_user_id = fields.Many2one('res.users',string='借用人')
	
	@api.model
	def create(self, vals):
		key_nos = vals.get('key_no', '').split('\n')
		if vals.get('key_no'):

			for i, key_no in enumerate(key_nos):
				vals['key_no'] = key_no
				if i != 0:
					self.env['fuenc.station.key.detail'].create(vals)
		vals['key_no'] = key_nos[0]

		return super(KeyDetail, self).create(vals)
	
	@api.model
	def get_data_test(self):
		print('ok')
