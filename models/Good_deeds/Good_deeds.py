# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import  datetime
from ..get_domain import get_domain

key = [('one_audit','待初审'),
       ('two_audit','待复审'),
       ('through','已通过'),
       ('rejected','已驳回')]


class GoodDeeds(models.Model):

    _name = 'fuenc_station.good_deeds'
    _order = 'open_time desc'
    _description = '好人好事'
    _rec_name = 'open_site'
    _inherit = ['fuenc_station.station_base','mail.thread', 'mail.activity.mixin']

    type = fields.Many2one('funenc_xa_station.good_deeds_type',string='类型',required=True, track_visibility='onchange')
    open_time = fields.Datetime(string='发生时间', track_visibility='onchange')
    open_site =fields.Char(string='发生地点', track_visibility='onchange')
    related_person =fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users','good_deeds_cdtct_ding_rel',string='相关人员', track_visibility='onchange')
    # related_person =fields.One2many('fuenc_station.good_deeds','fu_related_person',string='相关人员')
    write_person = fields.Char(string='填报人',default=lambda self: self.default_person_id(), track_visibility='onchange')
    write_time = fields.Date(string='填报时间',default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), track_visibility='onchange')
    audit_state = fields.Selection(key,string='审核状态',default='one_audit', track_visibility='onchange')
    event_state = fields.Text(string='事件详情', track_visibility='onchange')
    load_file_test = fields.Many2many('ir.attachment','good_deeds_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传', track_visibility='onchange')
    audit_flow = fields.Char(string='审核流程')
    mp_play_many = fields.One2many('video_voice_model' ,'good_deeds_play' ,string='视频附件', track_visibility='onchange')

    # 创建一条新的记录
    def new_increase_record(self):
        view_form = self.env.ref('funenc_xa_station.good_deeds_from').id
        return {
            'name': '好人好事',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_station.good_deeds',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target':'new',
        }

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.good_deeds_tree').id
        return {
            'name': '好人好事',
            'type': 'ir.actions.act_window',
            'clear_breadcrumbs': True,
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
                            'group':'funenc_xa_station.table_good_actions',
                            },
                            {
                                'title': '客伤',
                                'action2' : 'funenc_xa_station.guests_hurt_act',
                                'group' : 'funenc_xa_station.table_people_wound',
                                },
                            {
                                'title': '乘客意见箱',
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
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta

        primary_audit = '初审'+'    '+str(self.env.user.dingtalk_user.name) + \
                        '(' + str(now_time) + ')'
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.audit_flow = self.env.context.get('audit_flow', primary_audit)
        self.env['fuenc_station.good_deeds'].write(values)

    def test_btn_through(self):
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta
        values = {
            'audit_state': self.audit_state,
        }
        two_audit = self.audit_flow +'    '+ '复审'+'    '+str(self.env.user.dingtalk_user.name) + \
                    '(' + str(now_time.strftime('%Y-%m-%d %H:%M:%S')) + ')'
        self.audit_state = self.env.context.get('audit_state', 'through')
        self.audit_flow = self.env.context.get('audit_flow', two_audit)
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