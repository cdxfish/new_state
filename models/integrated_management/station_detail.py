# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.exceptions as msg


class station_detail(models.Model):
    _name = 'funenc_xa_station.station_detail'
    _description = u'车站详情'
    _inherit = 'fuenc_station.station_base'

    name = fields.Char(string='车站名字')
    station_nature = fields.Text(string='车站性质')
    station_position = fields.Text(string='车站位置')
    current_location = fields.Char(string='当前位置')
    station_exit_information = fields.One2many('funenc_xa_station.station_exit_information', 'station_id',
                                               string='出口信息')
    station_map_images = fields.One2many('funenc_xa_station.station_map_images', 'station_detail_id', string='地面信息图',
                                         required=True)

    @api.model
    def init_data(self):

        if self.env.user.id == 1:
            site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([
                ('department_hierarchy', '=', 3)
            ]).ids
        else:
            ding_user = self.env.user.dingtalk_user
            department_id = ding_user.departments[0]
            if department_id.department_hierarchy == 1:
                site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([
                    ('department_hierarchy', '=', 3)
                ]).ids
            elif department_id.department_hierarchy == 1:
                site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', department_id.departmentId)]).ids
            else:
                view_form = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_form').id
                res_id = self.search([('site_id', '=', department_id.id)])
                return {
                    'name': '借用记录',
                    "type": "ir.actions.act_window",
                    "res_model": "funenc_xa_station.station_detail",
                    "views": [[view_form, "form"]],
                    'res_id': res_id
                }
        view_list = self.env.ref('funenc_xa_station.site_station_detail').id
        return {
            'name': '借用记录',
            "type": "ir.actions.act_window",
            "res_model": "cdtct_dingtalk.cdtct_dingtalk_department",
            "views": [[view_list, "tree"]],
            "domain": [('id', 'in', site_ids)],
        }

    def tab_action(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_station_detail_form').id
        res_id = self.env['funenc_xa_station.station_detail'].search([('site_id', '=', self.id)]),
        return {
            'name': '车站详情',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_id': res_id[0].id if res_id else None,
            'res_model': 'funenc_xa_station.station_detail',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                                                              [
                                                                  {
                                                                      'title': '车站详情',
                                                                      'action' : 'funenc_xa_station.station_detai_action',
                                                                      
                                                                      'context':1,
                                                                      },
                                                                  {
                                                                      'title': '耗材出库',
                                                                      'action2':  'funenc_xa_station.xa_station_consumables_delivery_storage',
                                                                      },
                                                              ]
                                                          }''',
            'context': self.env.context,
        }


class StationExitInformation(models.Model):
    _name = 'funenc_xa_station.station_exit_information'
    _description = u'出口信息'
    _rec_name = 'position'

    exit_no = fields.Char(string='出口编号')
    exit_width = fields.Char(string='宽度')
    position = fields.Char(string='位置')
    remarks = fields.Text(string='备注说明')
    station_id = fields.Many2one('funenc_xa_station.station_detail', string='车站')


class StationMapImages(models.Model):
    _name = 'funenc_xa_station.station_map_images'
    _description = u'地面信息'

    name = fields.Char(string='名称')
    image = fields.Binary(string='图片')
    station_detail_id = fields.Many2one('funenc_xa_station.station_detail', string='车站详情相关')
