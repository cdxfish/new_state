# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
from datetime import datetime


key = [('one_audit','待初核'),
       ('two_audit','待复核'),
       ('through','已通过'),
       ('rejected','已驳回')]

class SuggestionBox(models.Model):
    _inherit = 'fuenc_station.station_base'
    _name = 'funenc_xa_station.suggestion_box'

    open_time = fields.Datetime(string='发生时间')
    open_site = fields.Char(string='发生地点')
    suggestion_title = fields.Char(string='意见标题')
    suggestion_details = fields.Text(string='意见详情')
    write_person = fields.Char(string='填报人')
    write_time = fields.Date(string='填报时间',default=datetime.now().strftime("%Y-%m-%d"))
    passengers_name = fields.Char(string='乘客姓名')
    audit_state = fields.Selection(key,string='审核状态', default='one_audit')
    event_type = fields.Char(string='事件类别')
    passengers_phone = fields.Char(string='乘客电话')
    main_parment = fields.Char(string='主办部门')
    help_parment = fields.Char(string='协办部门')
    deal_requirements = fields.Char(string='处理要求')
    access_time = fields.Date(string='回访时间')
    Satisfied = fields.Selection([('one','满意'),('zero','不满意')],string='乘客是否满意')
    load_file_test = fields.Many2many('ir.attachment','suggestion_box_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')

    def test_btn_two_audit(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'two_audit')
        self.env['funenc_xa_station.suggestion_box'].write(values)

    def test_btn_through(self):
        values = {
            'audit_state': self.audit_state,
        }
        self.audit_state = self.env.context.get('audit_state', 'through')
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
            'target': 'new',
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
        }

