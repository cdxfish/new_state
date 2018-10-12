# !user/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api,models,fields
import requests
import urllib
import base64

key = [('one_audit','待初核'),
       ('two_audit','待复核'),
       ('through','已通过'),
       ('rejected','已驳回')]

class GuestsHurt(models.Model):
    _name = 'fuenc_xa_station.guests_hurt'
    _inherit = 'fuenc_station.station_base'

    open_time = fields.Datetime(string='发生时间')
    open_site = fields.Char(string='发生地点')
    write_person  = fields.Char(string='填报人')
    guests_name = fields.Char(string='乘客姓名')
    guests_grede = fields.Selection([('man','男'),('woman','女')],string='乘客性别')
    guests_age = fields.Char(string='乘客年龄')
    write_time = fields.Date(string='填报时间',default=datetime.now().strftime("%Y-%m-%d"))
    claim = fields.Selection([('one','是'),('zero','否')],string='是否索赔')
    claim_money = fields.Integer(string='索赔金额')
    event_details = fields.Text(string='事件详情')
    claim_state = fields.Selection([('one','已赔付'),('zero','未赔付')],string='索赔状态')
    audit_state = fields.Selection(key,string='审核状态', default='one_audit')
    audit_flow = fields.Char(string='审核流程')
    load_file_test = fields.Many2many('ir.attachment','guests_hurt_ir_attachment_rel',
                                         'attachment_id','guests_hurt_id', string='图片上传')
    one_associated = fields.One2many('fuenc_xa_station.add_guests_hurt','associated',string='客人关联字段')
    mp_play = fields.Binary(string='上传视屏')
    file_name = fields.Char(string="File Name")
    url = fields.Char(string='url')
    mp_play_many = fields.One2many('video_voice_model','mp_play_one',string='视频附件')

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






    def test_btn_two_audit(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

    def test_btn_through(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'through')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

    def good_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'rejected')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

    def good_delete(self):
        self.env['fuenc_xa_station.guests_hurt'].search([('id','=',self.id)]).unlink()

    def test_btn_rejected(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'one_audit')
        self.env['fuenc_xa_station.guests_hurt'].write(values)

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
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }

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
        }

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
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }

    def add_guests_button_action(self):
        view_form = self.env.ref('funenc_xa_station.add_guests_hurt_details').id
        return {
            'name': '客伤',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'fuenc_xa_station.add_guests_hurt',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

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