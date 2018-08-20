# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyType(models.Model):
    _name = 'fuenc.station.key.type'

    name = fields.Char(string='钥匙类型')
    remark = fields.Text(string='备注')
