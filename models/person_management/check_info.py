# !user/bin/env python3
# -*- coding: utf-8 -*

from odoo import api,models,fields


class CheckInfo(models.Model):
    _name = 'person_management.check_info'

    grade = fields.Integer(string='评分')
    grade_standard = fields.Char(string='考评标准')
    problem_kind = fields.Char(string='考核类型')
    check_kind = fields.Char(string='考核类别')
    check_project = fields.Char(string='考核项目')
    incident_desfcription = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人')
    check_time = fields.Datetime(string='考评时间')
    # relevance = fields.Many2one('main.information',string='关联字段没有实际意义')