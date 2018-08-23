# -*- coding: utf-8 -*-
# Created by yong at 2018/8/22
from odoo import models, fields, api

OPERATE_TYPE = [
	('create', '创建'),
	('write', '修改'),
	('delete', '删除'),
	('destroyed', '报废'),
	('error', '破损'),
	('recovery', '恢复'),
	('start', '启用'),
	('fixed', '锁定'),
]


class ChangeRecord(models.Model):
	_name = 'funenc.xa.station.change.record'
	
	key_no = fields.Char(string='钥匙编号')
	type = fields.Char(string='钥匙类型')
	station = fields.Char(string='归属站点')
	name = fields.Char(string='钥匙名称')
	position = fields.Char(string='对应位置')
	is_main = fields.Selection(selection=[('yes', '主'), ('no', '备')], string='主备情况')
	operate_type = fields.Selection(selection=OPERATE_TYPE, string='操作类型')
	operate_member = fields.Char(string='操作人')
	remarks = fields.Char(string='备注')
