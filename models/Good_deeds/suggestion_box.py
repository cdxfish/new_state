# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
import datetime
from ..get_domain import get_domain

key = [('one_audit','待初审'),
       ('two_audit','待复审'),
       ('through','已通过'),
       ('rejected','已驳回')]

class SuggestionBox(models.Model):
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _name = 'funenc_xa_station.suggestion_box'
    _order = 'open_time desc'
    _rec_name = 'open_site'
    _description = '乘客意见箱'

    open_time = fields.Datetime(string='发生时间', track_visibility='onchange')
    open_site = fields.Char(string='发生地点', track_visibility='onchange')
    suggestion_title = fields.Char(string='意见标题', track_visibility='onchange')
    suggestion_details = fields.Text(string='意见详情', track_visibility='onchange')
    write_person = fields.Char(string='填报人',default=lambda self: self.default_person_id(), track_visibility='onchange')
    write_time = fields.Date(string='填报时间',default=datetime.datetime.now().strftime("%Y-%m-%d"), track_visibility='onchange')
    passengers_name = fields.Char(string='乘客姓名', track_visibility='onchange')
    audit_state = fields.Selection(key,string='审核状态', default='one_audit', track_visibility='onchange')
    event_type = fields.Char(string='事件类别', track_visibility='onchange')
    passengers_phone = fields.Char(string='乘客电话', track_visibility='onchange')
    main_parment = fields.Char(string='主办部门', track_visibility='onchange')
    help_parment = fields.Char(string='协办部门', track_visibility='onchange')
    deal_requirements = fields.Char(string='处理要求', track_visibility='onchange')
    access_time = fields.Date(string='回访时间', track_visibility='onchange')
    Satisfied = fields.Selection([('one','满意'),('zero','不满意')],string='乘客是否满意', track_visibility='onchange')
    load_file_test = fields.Many2many('ir.attachment','suggestion_box_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传', track_visibility='onchange')
    video_attachment = fields.One2many('video_voice_model','suggest_box_video',string='视频附件', track_visibility='onchange')
    audio_attachment = fields.One2many('video_voice_model','suggest_box_audio',string='音频附件', track_visibility='onchange')
    recovery_time = fields.Datetime(string='回复时间', track_visibility='onchange')
    recovery_person = fields.Char(string='回复人', track_visibility='onchange')
    satisfied_person = fields.Selection([('one', '满意'), ('zero', '不满意')], string='乘客是否满意', track_visibility='onchange')#责任部门意见的乘客满意
    survey_state = fields.Char(string='调查概况', track_visibility='onchange')
    recovery_content = fields.Text(string='回复内容', track_visibility='onchange')
    rectification_method = fields.Text(string='整改方法', track_visibility='onchange')
    according_opinion = fields.Text(string='定则意见及依据', track_visibility='onchange')
    duty_general = fields.Text(string='最终定性及定责', track_visibility='onchange')
    audit_flow = fields.Char(string='审核流程', track_visibility='onchange')

    #自动获取登录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.suggestion_box_tree').id
        return {
            'name': '乘客意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.suggestion_box',
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


    def test_btn_two_audit(self):
        values = {
            'audit_state': self.audit_state,
        }
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta

        primary_audit =  '初审' + '    ' + str(self.env.user.dingtalk_user.name) + \
                        '(' + str(now_time) + ')'
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.audit_flow = self.env.context.get('audit_flow', primary_audit)
        self.env['funenc_xa_station.suggestion_box'].write(values)

    def test_btn_through(self):
        values = {
            'audit_state': self.audit_state,
        }
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta

        primary_audit = self.audit_flow + '复审' + '    ' + str(self.env.user.dingtalk_user.name) + \
                        '(' + str(now_time) + ')'
        self.audit_state = self.env.context.get('audit_state', 'through')
        self.audit_flow = self.env.context.get('audit_flow', primary_audit)
        self.env['funenc_xa_station.suggestion_box'].write(values)

    def good_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'rejected')
        self.env['funenc_xa_station.suggestion_box'].write(values)

    def test_btn_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'one_audit')
        self.env['funenc_xa_station.suggestion_box'].write(values)

    def good_delete(self):
        self.env['funenc_xa_station.suggestion_box'].search([('id', '=', self.id)]).unlink()

    def test_btn_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'one_audit')
        self.env['funenc_xa_station.suggestion_box'].write(values)

    #修改整条记录
    def onchange_button_action(self):
        view_form = self.env.ref('funenc_xa_station.suggestion_box_form').id
        return {
            'name': '意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.suggestion_box',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    #查看整条记录的详情
    def guests_details_action(self):
        view_form = self.env.ref('funenc_xa_station.suggestion_box_act_details').id
        return {
            'name': '意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.suggestion_box',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
        }

    def create_suggest(self):
        view_form = self.env.ref('funenc_xa_station.suggestion_box_form').id
        return {
            'name': '乘客意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.suggestion_box',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target':'new',
        }

    #编辑form页面的责任部门意见
    def new_create_opnion(self):
        view_form = self.env.ref('funenc_xa_station.duty_derpament_opnion_form').id
        return {
            'name': '乘客意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.suggestion_box',
            'context': self.env.context,
            'res_id':self.id,
            'flags': {'initial_mode': 'edit'},
            'target':'new'

        }

    #责任form页面的投诉定性
    def complaints_suer_button(self):
        view_form = self.env.ref('funenc_xa_station.complaints_sure').id
        return {
            'name': '乘客意见箱',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.suggestion_box',
            'context': self.env.context,
            'res_id': self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new'

        }




