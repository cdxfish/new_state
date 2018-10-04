# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
key = [('one_audit','待初核'),
       ('two_audit','待复核'),
       ('through','已通过'),
       ('rejected','已驳回')]

class GuestsHurt(models.Model):
    _name = 'fuenc_xa_station.guests_hurt'
    _inherit = 'fuenc_station.station_base'

    open_time = fields.Datetime(string='发生时间')
    write_person  = fields.Char(string='填报人')
    guests_name = fields.Char(string='乘客姓名')
    write_time = fields.Date(string='填报时间')
    claim = fields.Selection([('one','是'),('zero','否')],string='是否索赔')
    claim_money = fields.Integer(string='索赔金额')
    claim_state = fields.Selection([('one','已索赔'),('zero','未索赔')],string='索赔状态')
    audit_state = fields.Selection(key,string='审核状态')
