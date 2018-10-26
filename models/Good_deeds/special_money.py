# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
from datetime import datetime
from ..get_domain import get_domain

key = [('one_audit','待初核'),
       ('two_audit','待复核'),
       ('through','已通过'),
       ('rejected','已驳回')]


class SpecialMoney(models.Model):
    _name = 'funenc_xa_station.special_money'
    _inherit = 'fuenc_station.station_base'

    open_time = fields.Datetime(string='发生时间')
    open_site = fields.Char(string='发生地点')
    event_type = fields.Selection([("deal","事务处理 "),('money','非及时退款')],string='事件类型')
    event_details = fields.Text(string='事件详情')
    survey_situation = fields.Text(string='调查情况')
    involving_money = fields.Integer(string='涉及金额')
    passengers_name = fields.Char(string='乘客姓名')
    passengers_phone = fields.Char(string='乘客电话')
    passengers_ID = fields.Char(string='乘客生份证')
    deal_person = fields.Char(string='处理人员')
    webmaster = fields.Char(string='站长')
    deputy_director = fields.Char(string='分部主任')
    main_director = fields.Char(string='部门领导')
    write_time = fields.Datetime(string='填报时间',default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    write_person = fields.Datetime(string='填报人')
    audit_flow = fields.Char(string='审核流程')
    apply_why = fields.Text(string='申请原因')
    deal_result = fields.Selection(key,string='处理结果',default='one_audit')
    # load_file_test = fields.Many2many('ir.attachment','good_special_ir_attachment_rel',
    #                                      'attachment_id','meeting_dateils_id', string='图片上传')
    load_file_test = fields.Binary(string='身份证照片')
    file_name = fields.Char(str='File Name')
    deal_list_file = fields.Binary(string='')

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.special_money_tree').id
        return {
            'name': '特殊赔偿金',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.special_money',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                        [
                            {'title': '好人好事',
                            'action':  'funenc_xa_station.good_deeds_act',
                            'group':'funenc_xa_station.table_good_actions'
                            },
                            {
                                'title': '客伤',
                                'action2' : 'funenc_xa_station.guests_hurt_act',
                                'group' : 'funenc_xa_station.table_people_wound'
                                },
                            {
                                'title': '乘客意意见箱',
                                'action2':  'funenc_xa_station.suggestion_box_act',
                                'group' : 'funenc_xa_station.table_people_message'
                                },
                           {
                                'title': '特殊赔偿金',
                                'action2':  'funenc_xa_station.special_money_act',
                                'group' : 'funenc_xa_station.table_special_compensation'
                                },
                        ]
                    }''',
            'context': self.env.context,
        }

    def special_details_action(self):
        view_form = self.env.ref('funenc_xa_station.special_money_details').id
        return {
            'name': '特殊赔偿金详情',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_money',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }

    def test_btn_two_audit(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'two_audit')
        self.env['funenc_xa_station.special_money'].write(values)

    def test_btn_through(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'through')
        self.env['funenc_xa_station.special_money'].write(values)

    def good_rejected(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'rejected')
        self.env['funenc_xa_station.special_money'].write(values)

    def test_btn_rejected(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'one_audit')
        self.env['funenc_xa_station.special_money'].write(values)

    def good_delete(self):
        self.env['funenc_xa_station.special_money'].search([('id', '=', self.id)]).unlink()

    def onchange_button_action(self):
        view_form = self.env.ref('funenc_xa_station.special_money_form').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_money',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def print_refund_form(self):
        id_id = self.id
        return {
            "type": "ir.actions.act_url",
            'res_id': self.id,
            "url": '/funenc_xa_station/special_money_xlsx?id=%s'%(id_id),

            "target": "new",
        }
