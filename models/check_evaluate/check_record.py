# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime

class CheckRecord(models.Model):
    _name = 'funenc_xa_station.check_record'
    _inherit = 'fuenc_station.station_base'

    key = [('check_parment','考核分部（室）分值')
        ,('relate_per_score','相关负责人考核分值')
        ,('station_per_score','车站站长考核分值')
        ,('technology_score','技术/职能岗考核分值')
        ,('management_score','管理岗考核分值')
        ,('loca_per_score','当事人考核分值')
        ]

    job_number = fields.Char(related='staff.jobnumber',string='工号',readonly=True)
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='考核人员')
    position = fields.Text(related='staff.position',string='职位')
    grade = fields.Float(string='参考分值',readonly=True)
    chose_grade = fields.Selection([('add','加'),('subtraction','减')],string='评分',default='subtraction')
    sure_grede = fields.Float(string='评分分值')
    check_target = fields.Selection(related='check_project.check_standard',string='考评指标')
    problem_kind =fields.Char(related='check_project.problem_kind',string='问题类型')
    check_kind = fields.Selection(key,string='考核类别')
    check_project = fields.Many2one('funenc_xa_station.check_standard',string='考核项目')
    incident_describe = fields.Text(string='事件描述')
    check_person = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='考评人')
    check_number = fields.Char(related='check_person.jobnumber', string='工号', readonly=True)
    check_time = fields.Datetime(string='考评时间',default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    associated_add = fields.One2many('funenc_xa_station.check_record_add','associated',string='新增考评人员')
    all_score = fields.Float(string='总分值', default=100)
    mouth_grade = fields.Float(string='本月评分')
    grade_degree = fields.Float(string='考评次数',default=1)


    @api.model
    def new_add_record(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.check_record',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    @api.constrains('chose_grade')
    def chose_grade_grade(self):
          if  self.chose_grade == 'subtraction':
              a = -self.sure_grede
              self.sure_grede = a
          elif self.chose_grade == 'add':
            self.sure_grede = self.sure_grede


    @api.onchange('check_kind')
    def parment_score(self):
        if self.check_kind == 'check_parment':
            check_kind1 = self.check_project.check_parment
            return {'value':{'grade':check_kind1}}

        elif self.check_kind == 'relate_per_score':
            check_kind1 = self.check_project.relate_per_score
            return {'value': {'grade': check_kind1}}

        elif self.check_kind == 'station_per_score':
            check_kind1 = self.check_project.station_per_score
            return {'value': {'grade': check_kind1}}

        elif self.check_kind == 'technology_score':
            check_kind1 = self.check_project.technology_score
            return {'value': {'grade': check_kind1}}

        elif self.check_kind == 'management_score':
            check_kind1 = self.check_project.management_score
            return {'value': {'grade': check_kind1}}

        elif self.check_kind == 'loca_per_score':
            check_kind1 = self.check_project.loca_per_score
            return {'value': {'grade': check_kind1}}
        else:
            return {'value': {'grade': 0}}

    @api.onchange('check_kind')
    def parment_sure_grede(self):
        if self.check_kind == 'check_parment':
            check_kind1 = self.check_project.check_parment
            return {'value':{'sure_grede':check_kind1}}

        elif self.check_kind == 'relate_per_score':
            check_kind1 = self.check_project.relate_per_score
            return {'value': {'sure_grede': check_kind1}}

        elif self.check_kind == 'station_per_score':
            check_kind1 = self.check_project.station_per_score
            return {'value': {'sure_grede': check_kind1}}

        elif self.check_kind == 'technology_score':
            check_kind1 = self.check_project.technology_score
            return {'value': {'sure_grede': check_kind1}}

        elif self.check_kind == 'management_score':
            check_kind1 = self.check_project.management_score
            return {'value': {'sure_grede': check_kind1}}

        elif self.check_kind == 'loca_per_score':
            check_kind1 = self.check_project.loca_per_score
            return {'value': {'sure_grede': check_kind1}}
        else:
            return {'value': {'sure_grede': 0}}


class AddResponsibility(models.Model):
    _name = 'funenc_xa_station.check_record_add'
    check_person = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='责任人员')
    check_number = fields.Char(related='check_person.jobnumber', string='工号', readonly=True)
    check_kind = fields.Char(string='考核类别')
    grade = fields.Integer(string='评分', readonly=True)
    chose_grade = fields.Selection([('add', '加'), ('subtraction', '减')], string='评分', default='subtraction')
    incident_describe = fields.Text(string='事件描述')
    associated = fields.Many2one('funenc_xa_station.check_record',string='关联字段没有实际意义')
