# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api

'''
交接班设置
'''


#################


class preparedness(models.Model):

    _name = 'funenc_xa_station.preparedness'
    _description = u'备品'
    _rec_name = 'preparedness_name'

    KEY = [('station_master', '站长'),
           ('train_working', '行车'),
           ('station_service', '站务'),
           ('ticket_booth', '票亭'),
           ('passenger_transport', '客运'),
           ]

    preparedness_name = fields.Char(string='备品名称', required=True)
    unit = fields.Char(string='单位')
    remarks = fields.Text(string='备注')
    type = fields.Selection(selection=KEY, string='备品类型')

    station_master_id = fields.Many2one('funenc_xa_station.station_master', string='')
    car_line_id = fields.Many2one('funenc_xa_station.car_line', string='')
    station_service_id = fields.Many2one('funenc_xa_station.station_service', string='')
    ticket_booth_id = fields.Many2one('funenc_xa_station.ticket_booth_id', string='')
    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')


class preparedness_1(models.Model):
    _name = 'funenc_xa_station.preparedness_1'
    _description = u'票务和站务备品'
    _rec_name = 'preparedness_name'

    state = fields.Selection(selection=[('正常','正常'),('异常','异常')],default="正常")
    preparedness_name = fields.Char(string='备品名称')
    unit = fields.Char(string='单位')
    list_situation = fields.Char(string='清单情况')
    error_name = fields.Char(string='异常情况')
    explain = fields.Char(string='说明')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts',srting='交接班')



class train_working(models.Model):
    _name = 'funenc_xa_station.check_project'
    _description = u'运营前检查项目'

    context = fields.Text(string='工作中填写内容')
    remarks = fields.Char(string='备注')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')

    car_line_id = fields.Many2one('funenc_xa_station.car_line', string='')
    check_project_to_production_change_shifts_ids = fields.One2many(
        'funenc_xa_station.check_project_to_production_change_shifts', 'check_project_id', string='交接班中间表')



class train_working_2(models.Model):
    _name = 'funenc_xa_station.train_working_2'
    _description = u'运营前检查交接班中间表'

    production_change_shifts1_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    context = fields.Text(string='工作中填写内容')
    check_situation = fields.Char(string='检查情况')
    check_time = fields.Datetime(string='检查时间')


class train_working_1(models.Model):
    _name = 'funenc_xa_station.train_working_1'
    _description = u'运营前检查项目'

    context = fields.Text(string='运营前检查项目')
    remarks = fields.Char(string='备注')
    check_situation = fields.Text(string='检查情况')
    check_time = fields.Datetime(string='检查时间')
    tvm = fields.Char(srting='tvm')
    bom = fields.Char(srting='bom')
    agm = fields.Char(srting='tvm')
    tcm = fields.Char(srting='tcm')
    plane_ticket = fields.Char(srting='互联网机票')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')


class prefabricate_ticket_type(models.Model):
    _name = 'funenc_xa_station.prefabricate_ticket_type'
    _description = u'预制票类型'

    name = fields.Char(string='预制票名称')
    remarks = fields.Char(string='备注')

    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')


class prefabricate_ticket_type_2(models.Model):
    _name = 'funenc_xa_station.prefabricate_ticket_type_2'
    _description = u'预制票类型'

    name = fields.Char(string='票种')
    settlement = fields.Char(string='上班结存')
    call_out = fields.Char(string='调出本站')
    turn_over = fields.Char(string='上交车票')
    press_ticket = fields.Char(string='售票员配票/票箱压票')
    add_up = fields.Char(string='增配数量')
    recovery = fields.Char(string='销售员结账/人工回收')
    this_lass = fields.Char(string='本班结存')
    remarks = fields.Char(string='备注')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')

class preparedness_2(models.Model):
    _name = 'funenc_xa_station.preparedness_2'
    _description = u'预制票类型'

    name = fields.Char(string='备品名称')
    remarks = fields.Char(string='备注')
    increase = fields.Char(string='本班增加/减少数')
    balance = fields.Char(string='本班结存')
    damage = fields.Char(string='损坏数量')
    scrap = fields.Char(string='报废数量')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts',string='交接班')


class ticketing_key_type(models.Model):
    _name = 'funenc_xa_station.ticketing_key_type'
    _description = u'票务钥匙类型'

    name = fields.Char(string='钥匙名称')
    remarks = fields.Char(string='备注')

    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')

class ticketing_key_type_2(models.Model):
    _name = 'funenc_xa_station.ticketing_key_type_2'
    _description = u'票务钥匙类型'

    name = fields.Char(string='钥匙名称')
    number = fields.Char(string='随身携带数量')
    cabinet = fields.Char(string='票柜存放数量')
    spare = fields.Char(string='备用数量')
    remarks = fields.Char(string='备注')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')


#################


class station_master(models.Model):

    _name = 'funenc_xa_station.station_master'
    _description = u'预设值班站长'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'station_master_id', string='备品交接')

    # station_master_to_shifts_ids = fields.One2many('funenc_xa_station.station_master_to_production_change_shifts',
    #                                                'station_master_id', string='交接班')

    @api.model
    def create(self, vals):
        station_master_id = super(station_master, self).create(vals)

        station_master_id.preparedness_ids.write({'type': 'station_master'})

        return station_master_id

    @api.multi
    def write(self, vals):
        self.preparedness_ids.write({'type': 'station_master'})

        return super(station_master, self).write(vals)

    @api.model
    def init_data(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_station_master_form').id

        dic = {
            'name': '预设值班站长',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.station_master',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
        ids = self.search([]).ids
        if ids:
            dic['res_id'] = ids[0]

        return dic


class car_line(models.Model):
    _name = 'funenc_xa_station.car_line'
    _description = u'预设行车值班员'

    check_project_ids = fields.One2many('funenc_xa_station.check_project', 'car_line_id', string='运营前检查')
    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'car_line_id', string='备品交接')

    def init_data(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_car_line_form').id

        dic = {
            'name': '预设',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.car_line',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
        ids = self.search([]).ids
        if ids:
            dic['res_id'] = ids[0]

        return dic


class station_service(models.Model):
    _name = 'funenc_xa_station.station_service'
    _description = u'预设站务'

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'station_service_id', string='')

    def init_data(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_station_service_form').id

        dic = {
            'name': '预设',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.station_service',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
        ids = self.search([]).ids
        if ids:
            dic['res_id'] = ids[0]

        return dic


class ticket_booth(models.Model):
    _name = 'funenc_xa_station.ticket_booth'
    _description = u'预设票务'

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'ticket_booth_id', string='')

    def init_data(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_ticket_booth_form').id

        dic = {
            'name': '预设',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.ticket_booth',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
        ids = self.search([]).ids
        if ids:
            dic['res_id'] = ids[0]

        return dic


class passenger_transport(models.Model):
    _name = 'funenc_xa_station.passenger_transport'
    _description = u'预设值客运值班员'

    check_project_ids = fields.One2many('funenc_xa_station.train_working_1', 'passenger_transport_id', string='运营前检查')
    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'passenger_transport_id', string='备品')
    prefabricate_ticket_type_ids = fields.One2many('funenc_xa_station.prefabricate_ticket_type',
                                                   'passenger_transport_id', string='预制票类型')
    ticketing_key_type_ids = fields.One2many('funenc_xa_station.ticketing_key_type', 'passenger_transport_id',
                                             string='钥匙类型')

    def init_data(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_passenger_transport_form').id

        dic = {
            'name': '预设',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.passenger_transport',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
        ids = self.search([]).ids
        if ids:
            dic['res_id'] = ids[0]

        return dic


class special_card_preset(models.Model):
    _name = 'funenc_xa_station.special_card_preset'
    _description = u'特殊卡预设'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'card_number'

    card_number = fields.Char(string='特殊卡号', required=True, track_visibility='onchange')
    remarks = fields.Char(string='备注', track_visibility='onchange')

    #
    user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='借用人', track_visibility='onchange')
    borrow_time = fields.Datetime('借用时间', track_visibility='onchange')
    return_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='归还人', track_visibility='onchange')
    return_time = fields.Datetime(string='归还时间', track_visibility='onchange')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班', track_visibility='onchange')

    def change_shifts_edit(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_special_card_preset_form').id
        return {
            'name': '交接班-车站特殊卡预设',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_card_preset',
            'context': self.env.context,
            'res_id':self.id,
            'flags': {'initial_mode': 'edit'},
            'target':'new',
        }

    def change_shifts_delete(self):
        self.unlink()


