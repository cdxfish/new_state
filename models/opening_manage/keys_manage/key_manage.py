# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class KeyManage(models.Model):
    _name = 'fuenc.station.key.manage'

    name = fields.Char(string='名字')
