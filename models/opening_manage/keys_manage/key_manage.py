# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyManage(models.Model):
	_name = 'fuenc.station.key.manage'
	
	name = fields.Char(string='名字', required=True)
	line_id = fields.Char(string='选择线路', required=True)
	ascription_site_id = fields.Char(string='归属站点', required=True)
	key_type_id = fields.Many2one('fuenc.station.key.type', string='钥匙类型', required=True)
	key_no = fields.Text(string='钥匙编号', required=True)
	key_position = fields.Char(string='对应位置', required=True)
	is_main = fields.Selection(selection=[('yes', '主'), ('no', '备')], string='主备情况', required=True)
	
	# borrow_user_id = fields.Many2one('res.users',string='借用人')
	
	@api.model
	def create(self, vals):
		if vals.get('key_no'):
			key_nos = vals.get('key_no').split('\n')
			for key_no in key_nos:
				if key_no:
					vals['key_no'] = key_no
					super(KeyManage, self).create(vals)
		
		# 这里有问题
		return super(KeyManage, self).create(vals)
