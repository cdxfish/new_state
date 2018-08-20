# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api


class BorrowRecord(models.Model):
    _name = 'fuenc.station.borrow.record'

    key_no = fields.Char(string='钥匙编号')
    line = fields.Char(string='线路')
    type = fields.Char(string='钥匙类型')
    station = fields.Char(string='归属站点')
    name = fields.Char(string='钥匙名称')
    position = fields.Char(string='对应位置')
    state = fields.Char(string='归还状态')
    borrow_time = fields.Datetime(string='借用时间')
    borrow_operate_member = fields.Char(string='借用操作人')
    borrow_member = fields.Char(string='借用人')
    return_time = fields.Datetime(string='归还时间')
    return_operate_member = fields.Char(string='归还操作人')
    return_member = fields.Char(string='归还人')
