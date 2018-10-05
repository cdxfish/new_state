# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ReserverManagement(models.Model):
    _name = 'funenc_xa_station.reserver_management'
    _inherit = 'fuenc_station.station_base'

    r_date = fields.Date(string='日期')
    day_money = fields.Char(string='日常备用金配备金额（1）')
    traffic_money = fields.Integer(string='交银行兑零纸币(2)')
    bank_Paper = fields.Integer(string='银行返兑零纸币(3)')
    bank_COINS = fields.Integer(string='银行返兑零硬币(4)')
    day_standby_money = fields.Integer(string='日常备用金(5)')
    temporary_standby_money = fields.Integer(string='临时备用金(6)')
    financial_temporary_money = fields.Integer(string='返还财务部备用金金额(7)')
    machine_money = fields.Integer(string='机币(8)')
    counterfeit = fields.Integer(string='假币(9)')
    imperfect_money = fields.Integer(string='残币(10)')
    Foreign_currency = fields.Integer(string='外币(11)')
    less_money = fields.Integer(string='少币(12)')
    subtotal = fields.Integer(string='小计(13)')
    more_money = fields.Integer(string='多币')
    return_money = fields.Integer(string='返还金额(14)')
    return_money_date = fields.Integer(string='返还所属日期')
    bank_return_money = fields.Integer(string='返还金额')
    bank_return_date = fields.Datetime(string='返还所属日期')
    day_day_standby = fields.Integer(string='当日备用金额(15)')
    day_day_standby_subtraction = fields.Integer(string='当日备用金差额(16)')
    note = fields.Text(string='备注')
    Person_charge_account = fields.Char(string='记账人')

    @api.model
    def reserver_money_method(self):
        lol = self.env['funenc_xa_station.reserver_management'].search_read([])
        for i in lol:
            print(i)
        print(lol)
        return lol


    def test_btn_start(self):
        return {
            ''
            'name': '储备金管理',
            'type': 'ir.actions.act_window',
            'res_model': 'funenc_xa_station.reserver_management',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
        }

    @api.depends('','','','','','')
    def add_count(self):
        pass

    @api.model
    def add_count_line(self):
        lol = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy','=',2)],['id','name'])
        print(lol)
        return lol

    @api.model
    def add_count_site(self):
        lis = []
        lol = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy','=',3)],['id','name'])
        print(lol)
        return lol

    @api.model
    def search_site(self,date):
        print("ooooooooooooooooooooooooooo",date)
        return  [{
            'id':'123'
        },{'name':'1234'}]