# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ReserverManagement(models.Model):
    _name = 'funenc_xa_station.reserver_management'
    _inherit = 'fuenc_station.station_base'

    r_date = fields.Date(string='日期')
    day_money = fields.Integer(string='日常备用金配备金额（1）')
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
    fu_subtotal = fields.Integer(string='小计(13)')
    more_money = fields.Integer(string='多币')
    return_money = fields.Integer(string='返还金额(14)')
    return_money_date = fields.Datetime(string='返还所属日期')
    bank_return_money = fields.Integer(string='返还金额')
    bank_return_date = fields.Datetime(string='返还所属日期')
    day_day_standby = fields.Integer(string='当日备用金额(15)')
    fu_day_day_standby = fields.Integer(string='当日备用金额(15)')
    day_day_standby_subtraction = fields.Integer(string='当日备用金差额(16)')
    fu_day_day_standby_subtraction = fields.Integer(string='当日备用金差额(16)')
    note = fields.Text(string='备注')
    Person_charge_account = fields.Char(string='记账人')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts',string='交接班')

    @api.model
    def reserver_money_method(self):
        ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].get_default_sheduling_data()
        lol = self.env['funenc_xa_station.reserver_management'].search_read([('site_id','=',ids.get('default_site'))])
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

    @api.onchange('machine_money','counterfeit','imperfect_money','Foreign_currency','less_money')
    def add_count_01(self):
        for data in self:
            data.subtotal = data.machine_money + data.counterfeit + data.imperfect_money + data.Foreign_currency \
                            + data.less_money


    @api.constrains('machine_money','counterfeit','imperfect_money','Foreign_currency','less_money')
    def add_count_011(self):
        for data in self:
            data.fu_subtotal = data.machine_money + data.counterfeit + data.imperfect_money + data.Foreign_currency \
                           + data.less_money

    @api.onchange('day_money','traffic_money','bank_Paper','bank_COINS','day_standby_money','temporary_standby_money',
                  'financial_temporary_money','subtotal','return_money',)
    def add_count_02(self):
        for data in self:
            data.day_day_standby = data.day_money - data.traffic_money + data.bank_Paper + data.bank_COINS \
                                   + data.day_standby_money + data.temporary_standby_money \
                                   - data.financial_temporary_money - data.subtotal + data.return_money

    @api.constrains('day_money','traffic_money','bank_Paper','bank_COINS','day_standby_money','temporary_standby_money',
                  'financial_temporary_money','subtotal','return_money',)
    def add_count_022(self):
        for data in self:
            data.fu_day_day_standby = data.day_money - data.traffic_money + data.bank_Paper + data.bank_COINS \
                                   + data.day_standby_money + data.temporary_standby_money \
                                   - data.financial_temporary_money - data.subtotal + data.return_money

    @api.onchange('traffic_money','bank_Paper','bank_COINS','subtotal','return_money')
    def add_count_03(self):
        for data in self:
            data.day_day_standby_subtraction = data.traffic_money - data.bank_Paper - data.bank_COINS + data.subtotal \
                                               - data.return_money

    @api.constrains('traffic_money','bank_Paper','bank_COINS','subtotal','return_money')
    def add_count_033(self):
        for data in self:
            data.fu_day_day_standby_subtraction = data.traffic_money - data.bank_Paper - data.bank_COINS + data.subtotal \
                                               - data.return_money

    @api.model
    def add_count_line(self):
        lol = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy','=',2)],['id','name'])
        return lol

    @api.model
    def add_count_site(self):
        lol = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy','=',3)],['id','name'])
        return lol

    @api.model
    def search_site(self,date):
        site_parent = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id','=',date)],['departmentId'])
        site_son = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('parentid','=',site_parent[0]['departmentId'])],['name'])
        # site = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('parentid','=',site_son[1]['departmentId'])],['name'])


        return site_son

    @api.model
    def search_record(self,date):

        production_change_shifts = self.env['funenc_xa_station.production_change_shifts'].search([('site_id','=',date)])
        data = []
        for production_change_shift in production_change_shifts:
            data = data +  production_change_shift.reserver_management_ids.read()


        return data

    @api.model
    def get_line_self_data(self):
        '''
        自动获取当前线路的数据
        :return:
        '''
        if self.env.user.id ==1:
            return
        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.ids
        return self.env.user.dingtalk_user.id

    @api.model
    def get_site_self_data(self):
        '''
        自动获取当前站点的数据
        :return:
        '''
        if self.env.user.id ==1:
            return

        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.id
        return ids