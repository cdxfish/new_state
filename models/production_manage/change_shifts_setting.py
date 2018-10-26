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

    KEY=[('station_master','站长'),
         ('train_working','行车'),
         ('station_service','站务'),
         ('ticket_booth', '票亭'),
         ('passenger_transport','客运'),
         ]

    preparedness_name = fields.Char(string='备品名称',required=True)
    unit = fields.Char(string='单位',required=True)
    remarks = fields.Text(string='备注')
    type = fields.Selection(selection=KEY,string='备品类型')

    station_master_id = fields.Many2one('funenc_xa_station.station_master',string='')
    car_line_id = fields.Many2one('funenc_xa_station.car_line', string='')
    station_service_id = fields.Many2one('funenc_xa_station.station_service', string='')
    ticket_booth_id = fields.Many2one('funenc_xa_station.ticket_booth_id', string='')
    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')


class train_working(models.Model):
    _name = 'funenc_xa_station.check_project'
    _description = u'运营前检查项目'

    context = fields.Text(string='工作中填写内容')
    remarks = fields.Char(string='备注')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    car_line_id = fields.Many2one('funenc_xa_station.car_line',string='')


class train_working_1(models.Model):
    _name = 'funenc_xa_station.train_working_1'
    _description = u'运营前检查项目'

    context = fields.Text(string='运营前检查项目')
    remarks = fields.Char(string='备注')
    check_situation = fields.Text(string='检查情况')
    check_time = fields.Datetime(string='检查时间')
    tvm = fields.Char(srting='tvm')
    bom= fields.Char(srting='bom')
    agm = fields.Char(srting='tvm')
    tcm = fields.Char(srting='tcm')
    plane_ticket= fields.Char(srting='互联网机票')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts',string='交接班')
    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport',string='')



class prefabricate_ticket_type(models.Model):
    _name = 'funenc_xa_station.prefabricate_ticket_type'
    _description = u'预制票类型'

    name = fields.Char(string='预制票名称')
    remarks = fields.Char(string='备注')

    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport', string='')

class ticketing_key_type(models.Model):
    _name = 'funenc_xa_station.ticketing_key_type'
    _description = u'票务钥匙类型'

    name = fields.Char(string='钥匙名称')
    remarks = fields.Char(string='备注')

    passenger_transport_id = fields.Many2one('funenc_xa_station.passenger_transport',string='')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')

#################


class station_master(models.Model):
    _name = 'funenc_xa_station.station_master'
    _description = u'预设值班站长'

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness','station_master_id',string='备品交接')

    station_master_to_shifts_ids = fields.One2many('funenc_xa_station.station_master_to_production_change_shifts','station_master_id',string='交接班')

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
    def init(self):
        if self.env.user.id == 1:

            pass

        else:
            return




class car_line(models.Model):
    _name = 'funenc_xa_station.car_line'
    _description = u'预设行车值班员'

    check_project_ids = fields.One2many('funenc_xa_station.check_project','car_line_id',string='运营前检查')
    preparedness_ids = fields.One2many('funenc_xa_station.preparedness','car_line_id',string='备品交接')

class station_service(models.Model):
    _name = 'funenc_xa_station.station_service'
    _description = u'预设站务'

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness','station_service_id',string='')


class ticket_booth(models.Model):
    _name = 'funenc_xa_station.ticket_booth'
    _description = u'预设票务'

    preparedness_ids = fields.One2many('funenc_xa_station.preparedness','ticket_booth_id',string='')


class passenger_transport(models.Model):
    _name = 'funenc_xa_station.passenger_transport'
    _description = u'预设值客运值班员'

    check_project_ids = fields.One2many('funenc_xa_station.train_working_1', 'passenger_transport_id', string='运营前检查')
    preparedness_ids = fields.One2many('funenc_xa_station.preparedness', 'passenger_transport_id', string='备品')
    prefabricate_ticket_type_ids = fields.One2many('funenc_xa_station.prefabricate_ticket_type', 'passenger_transport_id', string='预制票类型')
    ticketing_key_type_ids = fields.One2many('funenc_xa_station.ticketing_key_type', 'passenger_transport_id', string='钥匙类型')

class special_card_preset(models.Model):
    _name = 'funenc_xa_station.special_card_preset'
    _description = u'特殊卡预设'
    _inherit = 'fuenc_station.station_base'
    _rec_name = 'card_number'

    card_number = fields.Char(string='特殊卡号', required=True)
    remarks = fields.Char(string='备注')



