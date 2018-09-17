# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields

class CheckRecord(models.Model):
    _name = 'funenc_xa_station.check_record'
    _inherit = 'fuenc_station.station_base'

    key = [('1','考核分部（室）分值')
        ,('2','相关负责人考核分值')
        ,('3','车站站长考核分值')
        ,('4','技术/职能岗考核分值')
        ,('5','管理岗考核分值')
        ,('6','当事人考核分值')
        ]

    line_id = fields.Char(string='线路')
    site_id = fields.Char(string='站点')
    job_number = fields.Char(related='staff.jobnumber',string='工号',readonly=True)
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工')
    position = fields.Char(string='职位')
    grade = fields.Integer(string='评分',readonly=True)
    chose_grade = fields.Selection([('add','加'),('subtraction','减')],string='评分',store=True)
    check_target = fields.Char(string='考评指标')
    problem_kind =fields.Char(string='问题类型')
    check_kind = fields.Selection(key,string='考核类别',default='subtraction',\
                                   compute='parment_score')
    check_project = fields.Many2one('funenc_xa_station.check_standard',string='考核项目')
    incident_describe = fields.Text(string='事件描述')
    check_person = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='考评人')
    check_number = fields.Char(related='check_person.jobnumber', string='工号', readonly=True)
    check_time = fields.Datetime(string='考评时间')
    associated_add = fields.One2many('funenc_xa_station.check_record_add','associated',string='新增考评人员')
    # check_person_add = fields.Char(related='associated_add.check_person',string='责任人员')
    # check_kind_add = fields.Char(related='associated_add.check_kind',string='考核类别')

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

    @api.constrains('grade')
    def chose_grade_grade(self):
        for this in self:
            if this.grade:
                  if  this.chose_grade == 'subtraction':
                      this.grade = -abs(this.grade)

                  elif this.chose_grade == 'add':
                      this.grade = abs(this.grade)
    def create_(self):

        self.associated_add = [(0, 0, {'check_person':''},)]

    @api.constrains('grade','check_kind')
    def parment_score(self):
        for this in self:
            if this.check_kind == 1:
                this.grade = self.env['funenc_xa_station.check_standard'].search({}).check_parment
            elif this.check_kind == 2:
                this.grade = self.env['funenc_xa_station.check_standard'].search({}).relate_per_score
            elif this.check_kind == 3:
                this.grade = self.env['funenc_xa_station.check_standard'].search({}).station_per_score



class AddResponsibility(models.Model):
    _name = 'funenc_xa_station.check_record_add'
    check_person = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='责任人员')
    check_number = fields.Char(related='check_person.jobnumber', string='工号', readonly=True)
    check_kind = fields.Char(string='考核类别')
    grade = fields.Integer(string='评分', readonly=True)
    chose_grade = fields.Selection([('add', '加'), ('subtraction', '减')], string='评分', default='subtraction')
    incident_describe = fields.Text(string='事件描述')
    associated = fields.Many2one('funenc_xa_station.check_record',string='关联字段没有实际意义')

