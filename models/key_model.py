# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.exceptions as msg

class key_manage(models.Model):
    _name = 'fuenc_station.key_manage'

class key_type(models.Model):
    _name = 'fuenc_station.key_type'
    _rec_name = "key_type_name"

    key_type_name = fields.Char(string=u'钥匙类型')
    remarks = fields.Text(string=u'备注')
