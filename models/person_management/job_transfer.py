# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields

class JobTransfer(models.Model):
    _name = 'persom_namagement.jobt_ranfer'

    department = fields.Char(string='所属部门')
    line_gauze = fields.Char(string='所属线网')
    station = fields.Char(string='车站')
    site_post = fields.Char(string='定岗/转岗岗位')
    site_time = fields.Date(string='定岗/转岗时间')
    site_file = fields.Many2one('main.information',string='定岗转岗文件号')

