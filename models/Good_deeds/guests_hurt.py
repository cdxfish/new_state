# !user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api,models,fields
import requests
import urllib
import base64
from ..get_domain import get_domain


key = [('one_audit','待初审'),
       ('two_audit','待复审'),
       ('through','已通过'),
       ('rejected','已驳回')]

class GuestsHurt(models.Model):
    _name = 'fuenc_xa_station.guests_hurt'
    _inherit = 'fuenc_station.station_base'

    open_time = fields.Datetime(string='发生时间')
    open_site = fields.Char(string='发生地点')
    write_person  = fields.Char(string='填报人',default=lambda self: self.default_person_id())
    guests_name = fields.Char(string='乘客姓名')
    guests_grede = fields.Selection([('man','男'),('woman','女')],string='乘客性别')
    guests_age = fields.Char(string='乘客年龄')
    write_time = fields.Date(string='填报时间',default=datetime.now().strftime("%Y-%m-%d"))
    claim = fields.Selection([('one','是'),('zero','否')],string='是否索赔')
    claim_money = fields.Integer(string='索赔金额')
    event_details = fields.Text(string='事件详情')
    equiment_details = fields.Text(string='设备状态')
    claim_state = fields.Selection([('one','已赔付'),('zero','未赔付')],string='索赔状态',default='zero')
    audit_state = fields.Selection(key,string='审核状态', default='one_audit')
    audit_flow = fields.Char(string='审核流程')
    guests_phone = fields.Char(string='乘客联系方式')
    responsibility_identification = fields.Selection([('self','乘客自身的原因'),
                                                      ('subway','地铁原因'),('three_method','第三方原因')],string='责任方认定(初审)')
    load_file_test = fields.Many2many('ir.attachment','guests_hurt_ir_attachment_rel',
                                         'attachment_id','guests_hurt_id', string='图片上传')
    one_associated = fields.One2many('fuenc_xa_station.add_guests_hurt','associated',string='客人关联字段')
    mp_play = fields.Binary(string='上传视屏')
    file_name = fields.Char(string="File Name")
    url = fields.Char(string='url')
    mp_play_many = fields.One2many('video_voice_model','guests_mp_play_one',string='视频附件')
    mp3_play_many = fields.One2many('video_voice_model','guests_mp3_play',string='视频附件')

    # 自动获取记录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return
        return self.env.user.dingtalk_user.name
    # @api.model
    # def create(self, params):
    #     file_binary = params['mp_play_many.']
    #     file_name = params.get('file_name', self.file_name)
    #     if file_binary:
    #         url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
    #             'funenc_xa_station', file_name, base64.b64decode(file_binary.mp_play))
    #         params['url'] = url
    #         params['file_name'] = file_name
    #     return super(GuestsHurt, self).create(params)
    #
    # def view_details(self):
    #     url = self.url
    #     if url:
    #         return {
    #             "type": "ir.actions.act_url",
    #             "url": url,
    #             "target": "new"
    #         }

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.guests_hurt_tree').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'fuenc_xa_station.guests_hurt',
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
                                'title': '乘客意见箱',
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

    #通过初审按钮
    def test_btn_two_audit(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

    #通过复审按钮
    @api.multi
    def test_btn_through(self):
        for i in self:
            values = {
                'audit_state': i.audit_state,
            }
            i.audit_state = self.env.context.get('audit_state', 'through')
            self.env['fuenc_xa_station.guests_hurt'].write(values)

    #驳回按钮
    def good_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'rejected')
        self.env['fuenc_xa_station.guests_hurt'].write(values)
        return False

    #删除按钮
    def good_delete(self):
        self.env['fuenc_xa_station.guests_hurt'].search([('id','=',self.id)]).unlink()

    #继续提交按钮
    def test_btn_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'one_audit')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

    #查看详情

    def good_details_button(self):
        view_form = self.env.ref('funenc_xa_station.guests_hurt_details').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            # 'target': 'new',
        }

    #新建一条记录
    def create_guests_action(self):
        view_form = self.env.ref('funenc_xa_station.guests_hurt_form').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target':'new',
        }

    #查看详情
    def guests_details_action(self):
        view_form = self.env.ref('funenc_xa_station.guests_hurt_details').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    #form表格中的新增
    def add_guests_button_action(self):
        view_form = self.env.ref('funenc_xa_station.add_guests_hurt_form').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.add_guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    #tree视图中的修改按钮
    def onchange_button_action(self):
        view_form = self.env.ref('funenc_xa_station.guests_hurt_form').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }
    # 修改索赔的状态
    def change_state(self):
        if self.claim_state == 'zero':
            self.write({'claim_state':'one'})
        elif self.claim_state == 'one':
            self.write({'claim_state': 'zero'})

    # 新增一条跟进记录
    def complaints_suer_button(self):
        view_form = self.env.ref('funenc_xa_station.add_aguests_hurt_form').id
        return {
            'name': '跟进记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.add_guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }
