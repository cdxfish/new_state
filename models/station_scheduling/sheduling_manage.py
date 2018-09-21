# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api


class ShedulingManage(models.Model):
    _name = 'funenc_xa_station.sheduling_manage'
    _description = '排班管理'
    _inherit = 'fuenc_station.station_base'

    sheduling_start_time = fields.Date(string='开始时间')
    sheduling_end_time = fields.Date(string='结束时间')
    class_group_ids = fields.Many2many('funenc_xa_station.class_group', 'sheduling_manage_class_group_2_ref',
                                       'sheduling_manage_id', 'class_group_id', string='选择班组'
                                       )
    arrange_order_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_2_ref',
                                         'sheduling_manage_id', 'arrange_order_id', string='班组班次'
                                         )
    # motorized_user_ids = fields.Many2many('')
    motorized_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_3_ref',
                                         'sheduling_manage_id', 'arrange_order_id', string='机动人员班次'
                                         )
    sheduling_arrange_order_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_4_ref',
                                         'sheduling_manage_id', 'arrange_order_id', string='班组排班规则')
    motorized_rule_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_5_ref',
                                         'sheduling_manage_id', 'arrange_order_id', string='机动人员排班规则')

    #  tree显示字段
    show_class_group_name = fields.Char(string='班组')
    show_arrange_order_name = fields.Char(string='班次')
    show_rule_name = fields.Char(string='排班规则', default= '无')
    show_sheduling_time = fields.Char(string='排班时间')



