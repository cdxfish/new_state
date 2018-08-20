# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyType(models.Model):
	_name = 'fuenc.station.key.type'
	_rec_name = "name"
	
	name = fields.Char(string='名字')
	remarks = fields.Text(string='备注')
	operation = fields.Char(string='操作', default='操作')
	
	def delete(self):
		pass
	
	def operation(self):
		pass
