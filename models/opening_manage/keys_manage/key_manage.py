# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyManage(models.Model):
	_name = 'funenc.xa.station.key.manage'
	_description = '钥匙管理'

	# key_detail_id = fields.Many2one('funenc.xa.station.key.detail', string='钥匙详情')
	# line_id = fields.Many2one('train_line.train_line', string='线路')
	# ascription_site_id = fields.Many2one('train_station.train_station',string='归属站点')
	# key_type_id = fields.Many2one('funenc.xa.station.key.type', string='钥匙类型')
	# master_number = fields.Integer(string='主钥匙数量', compute='_compute_count')
	# copy_number = fields.Integer(string='副钥匙数量', compute='_compute_count')
	# key_total = fields.Integer(string='钥匙总量', compute='_compute_count')
	# borrow_number = fields.Integer(string='借出数量', compute='_compute_count')
	# destroy_number = fields.Integer(string='损耗数量', compute='_compute_count')


	# 创建钥匙
	@api.model
	def create_key(self):
		return {
			'name': '钥匙创建',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'funenc.xa.station.key.detail',
			'context': self.env.context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	# 借用钥匙
	@api.model
	def borrow_key(self):
		context = dict(self.env.context)
		view_form = self.env.ref('funenc_xa_station.borrow_record_form_1').id
		context['borrow_member'] = self.env.user.id
		return {
			'name': '钥匙借用',
			'type': 'ir.actions.act_window',
			"views": [[view_form, "form"]],
			'res_model': 'funenc.xa.station.borrow.record',
			'context': context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	# 归还钥匙
	@api.model
	def return_key(self):
		context = dict(self.env.context)
		view_form = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_form').id
		return {
			'name': '钥匙归还',
			'type': 'ir.actions.act_window',
			"views": [[view_form, "form"]],
			'res_model': 'funenc.xa.station.borrow.record',
			'context': context,
			# 'flags': {'initial_mode': 'edit'},
			'target': 'new',
		}
	
	# 借用记录
	@api.model
	def borrow_record(self):
		view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_list').id
		view_form = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_form').id
		return {
			'name': '借用记录',
			"type": "ir.actions.act_window",
			"res_model": "funenc.xa.station.borrow.record",
			"views": [[view_tree, "tree"], [view_form, "form"]],
			# "domain": [()],
		}


	@api.model
	def get_statistic_key_data(self):
		'''
		  根据权限获取钥匙统计数据,采用self.env['']会自动权限查询
		'''
		# user = self.env.user
		data_table = []

		key_type_list = self.env['funenc.xa.station.key.type'].search_read([(1, '=', 1)])
		# line_list = self.env['train_line.train_line'].search_read([(1, '=', 1)])
		for index, key_type in enumerate(key_type_list):
			key_total = len(self.env['funenc.xa.station.key.type'].search(
																		  [('id', '=', key_type.get('id'))])

			                                                              )
			statistic_key = {}
			statistic_key['index'] = index+1
			statistic_key['line_id'] = '一号线'
			statistic_key['site_id'] = '省体育馆'
			statistic_key['key_type'] = key_type.get('name')
			statistic_key['key_total'] =  key_total
			statistic_key['master_number'] = 1
			statistic_key['copy_number'] = 1
			statistic_key['borrow_number'] = 1
			statistic_key['destroy_number'] =  1
			data_table.append(statistic_key)
		# statistic_key_list = self.env['funenc.xa.station.borrow.record'].search_read([(1,'=',1)])


		return data_table

	@api.model
	def get_key_view_ids(self):
		borrow_record_form_1 = self.env.ref('funenc_xa_station.borrow_record_form_1').id
		borrow_record_form = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_form').id

		borrow_record_list = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_list').id

		return {'borrow_record_form_1': borrow_record_form_1,
				'borrow_record_form': borrow_record_form,
				'borrow_record_list': borrow_record_list,
				# 'context': dict(self.env.context)

		}
