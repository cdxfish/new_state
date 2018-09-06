# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models,fields


class AwardInfo(models.Model):
    _name = 'person_management.award_info'

    award_money = fields.Char(string='奖励金额')
    award_standard_kind = fields.Char(string='奖励指标类')
    examination_item = fields.Char(string='考核项目')
    incident_description = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人')
    check_time = fields.Datetime(string='考评时间')
    relevance = fields.Many2one('main.information',string='关联字段没有实际意义')
