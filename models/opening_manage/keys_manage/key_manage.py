# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api
from ...get_domain import get_site_ids

class KeyManage(models.Model):
    _name = 'funenc.xa.station.key.manage'
    _description = '钥匙管理'
    _inherit = 'fuenc_station.station_base'

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

    @get_site_ids
    @api.model
    def get_statistic_key_data(self,site_ids):
        '''
          根据权限获取钥匙统计数据,采用self.env['']会自动权限查询
        '''
        res_user = self.env.user
        data_table = []
        # 先暂时统计 站点钥匙
        if res_user.id == 1:
            return


        key_type_list = self.env['funenc.xa.station.key.type'].search_read([('site_id', 'in', site_ids)])
        # line_list = self.env['train_line.train_line'].search_read([(1, '=', 1)])
        for index, key_type in enumerate(key_type_list):
            key_total = len(self.env['funenc.xa.station.key.detail'].search(
                [('key_type_id', '=', key_type.get('id'))]).ids
                            )
            master_number = len(
                self.env['funenc.xa.station.key.detail'].search(
                    [('key_type_id', '=', key_type.get('id', 0)), ('is_main', '=', 'yes')
                     ]).ids
            )

            copy_number = len(
                self.env['funenc.xa.station.key.detail'].search([('key_type_id', '=', key_type.get('id', 0))
                                                                  ,('is_main','!=','yes')
                                                                  ]).ids)
            borrow_number = len(
                self.env['funenc.xa.station.key.detail'].search([('key_type_id', '=', key_type.get('id', 0))
                                                                  ,('state_now','=','borrow')
                                                                  ]).ids)
            destroy_number = len(
                self.env['funenc.xa.station.key.detail'].search([('key_type_id', '=', key_type.get('id', 0))
                                                                  ,('state_now','=','destroyed')
                                                                  ]).ids)
            statistic_key = {}
            statistic_key['index'] = index + 1
            statistic_key['line_id'] = key_type.get('line_id')[1] if key_type.get('line_id') else ''
            statistic_key['site_id'] = key_type.get('site_id')[1] if key_type.get('site_id') else ''
            statistic_key['key_type'] = key_type.get('name')
            statistic_key['key_total'] = key_total
            statistic_key['master_number'] = master_number
            statistic_key['copy_number'] = copy_number
            statistic_key['borrow_number'] = borrow_number
            statistic_key['destroy_number'] = destroy_number
            data_table.append(statistic_key)

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
