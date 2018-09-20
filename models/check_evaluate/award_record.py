# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AwardRecord(models.Model):
    _name = 'funenc_xa_station.award_record'
    _inherit = 'fuenc_station.station_base'


    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    jobnumber = fields.Char(related='staff.jobnumber',string='工号')
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工')
    position = fields.Text(related='staff.position',string='职位')
    award_money = fields.Char(string='奖励金额')
    award_target_kind = fields.Char(string='奖励指标类')
    award_project = fields.Many2one('funenc_xa_station.award_standard',string='奖励项目')
    check_project = fields.Char(string='考核项目')
    award_money_kind = fields.Char(related='award_project.award_standard',string='参考奖励')
    incident_describe = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人')
    check_time = fields.Datetime(string='考评时间')
    award_record_add = fields.One2many('funenc_xa_station.award_record_add','associated',string='新增责任人员')
    award_money = fields.Float(string='奖励金额')
    award_degree = fields.Integer(string='奖励次数',default=1)

    @api.model
    def award_record_create(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.award_record',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


class AwardRecordAdd(models.Model):
    _name = 'funenc_xa_station.award_record_add'

    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工')
    jobnumber = fields.Char(related='staff.jobnumber',string='工号',readonly=True)
    award_money = fields.Char(string='奖励金额')
    incident_describe = fields.Char(string='事件描述')
    associated = fields.Many2one('funenc_xa_station.award_record',default='',readonly=True,string='')


