# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import  datetime
from ..get_domain import get_domain

key = [('one_audit','待初核'),
       ('two_audit','待复核'),
       ('through','通过'),
       ('rejected','驳回')]

class GoodDeeds(models.Model):
    _name = 'fuenc_station.good_deeds'
    _inherit = 'fuenc_station.station_base'


    type = fields.Many2one('funenc_xa_station.good_deeds_type',string='类型')
    open_time = fields.Datetime(string='发生时间')
    open_site =fields.Char(string='发生地点')
    related_person =fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users','good_deeds_cdtct_ding_rel',string='相关人员')
    # related_person =fields.One2many('fuenc_station.good_deeds','fu_related_person',string='相关人员')
    write_person = fields.Char(string='填报人',default=lambda self: self.default_person_id())
    write_time = fields.Date(string='填报时间',default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    audit_state = fields.Selection(key,string='审核状态',default='one_audit')
    event_state = fields.Text(string='事件详情')
    load_file_test = fields.Many2many('ir.attachment','good_deeds_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')
    audit_flow = fields.Char(string='审核流程')
    mp_play_many = fields.One2many('video_voice_model' ,'good_deeds_play' ,string='视频附件')

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.good_deeds_tree').id
        return {
            'name': '好人好事',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'fuenc_station.good_deeds',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                        [
                            {'title': '好人好事',
                            'action':  'funenc_xa_station.good_deeds_act',
                            # 'group':'funenc_xa_station.table_good_actions',
                            },
                            {
                                'title': '客伤',
                                'action2' : 'funenc_xa_station.guests_hurt_act',
                                'group' : 'funenc_xa_station.table_people_wound',
                                },
                            {
                                'title': '乘客意意见箱',
                                'action2':  'funenc_xa_station.suggestion_box_act',
                                'group' : 'funenc_xa_station.table_people_message',
                                },
                           {
                                'title': '特殊赔偿金',
                                'action2':  'funenc_xa_station.special_money_act',
                                'group' : 'funenc_xa_station.table_special_compensation',
                                },
                        ]
                    }''',
            'context': self.env.context,
        }

    #自动获取登录人的填报姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name



    def test_btn_two_audit(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.env['fuenc_station.good_deeds'].write(values)

    def test_btn_through(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'through')
        self.env['fuenc_station.good_deeds'].write(values)

    def good_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'rejected')
        self.env['fuenc_station.good_deeds'].write(values)

    def test_btn_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'one_audit')
        self.env['fuenc_station.good_deeds'].write(values)

    def good_delete(self):
        self.env['fuenc_station.good_deeds'].search([('id','=',self.id)]).unlink()

    #修改按钮
    def onchange_button_action(self):
        view_form = self.env.ref('funenc_xa_station.good_deeds_from').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_station.good_deeds',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    #详情页面
    def good_details_button(self):
        view_form = self.env.ref('funenc_xa_station.good_deeds_state').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_station.good_deeds',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
        }