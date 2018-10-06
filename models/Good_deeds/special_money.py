# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
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
    involving_money = fields.Char(string='涉及金额')
    passengers_name = fields.Char(string='乘客姓名')
    passengers_phone = fields.Char(string='乘客电话')
    passengers_ID = fields.Char(string='乘客生份证')
    deal_person = fields.Char(string='处理人员')
    webmaster = fields.Char(string='站长')
    deputy_director = fields.Char(string='分部主任')
    main_director = fields.Char(string='部门领导')
    write_time = fields.Datetime(string='填报时间')
    write_person = fields.Datetime(string='填报人')
    audit_flow = fields.Char(string='审核流程')
    deal_result = fields.Selection(key,string='处理结果',default='one_audit')
    load_file_test = fields.Many2many('ir.attachment','good_deeds_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')

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