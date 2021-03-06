# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
from ..get_domain import get_domain

class AwardRecord(models.Model):
    _name = 'funenc_xa_station.award_record'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _order = 'check_time desc'
    _rec_name = 'staff'
    _description = '奖励记录'


    # line_road = fields.Char(string='线路')
    # station_site = fields.Char(string='站点')
    jobnumber = fields.Char(related='staff.jobnumber',string='工号', readonly=True, track_visibility='onchange')
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工', track_visibility='onchange')
    position = fields.Text(related='staff.position',string='职位', track_visibility='onchange')
    award_target_kind = fields.Many2one('award_standard_object',string='奖励指标类',required=True, track_visibility='onchange')
    award_project = fields.Many2one('award_award_project',string='奖励项目',required=True, track_visibility='onchange')
    check_project = fields.Many2one('award_check_project',string='考核项目',required=True, track_visibility='onchange')
    award_money_kind = fields.Char(string='参考奖励', track_visibility='onchange')
    incident_describe = fields.Char(string='事件描述', track_visibility='onchange')
    check_person = fields.Char(string='考评人', default=lambda self: self.default_person_id(), track_visibility='onchange')
    check_time = fields.Datetime(string='考评时间',default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_visibility='onchange')
    award_record_add = fields.One2many('funenc_xa_station.award_record_add','associated',string='新增责任人员', track_visibility='onchange')
    award_money = fields.Float(string='奖励金额', track_visibility='onchange')
    award_degree = fields.Integer(string='奖励次数',default=1, track_visibility='onchange')
    relevance_award = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='关联字段')

    #在修改奖励指标类的时候返回奖励项目
    @api.onchange('award_target_kind')
    def get_award_project(self):
        res = {}
        if self.award_target_kind and self.award_project and self.check_project:
            record = self.env['funenc_xa_station.award_standard'].search([
                ('award_standard_kind','=',self.award_target_kind.id),
                ('award_project','=',self.award_project.id),
                ('check_project','=',self.check_project.id)
            ])
            if not record:
                res['value'] = {'award_project': None, 'check_project': None}
                return res
        if not self.award_target_kind:
            res['domain'] = {'award_project': [(1, '=', 1)]}

            return res
        elif not self.check_project:
            record = self.env['funenc_xa_station.award_standard'].search(
                [('award_standard_kind', '=', self.award_target_kind.id)])

            ids = [i['award_project'][0].id for i in record]

            res['domain'] = {'award_project': [('id', 'in', ids)]}
            res['value'] = {'award_project': None}

            return res
    #在修改奖励项目返回考核项目的值
    @api.onchange('award_project')
    def get_check_project(self):
        res = {}
        if self.award_target_kind and self.award_project and self.check_project:
            record = self.env['funenc_xa_station.award_standard'].search([
                ('award_standard_kind','=',self.award_target_kind.id),
                ('award_project','=',self.award_project.id),
                ('check_project','=',self.check_project.id)
            ])
            if not record:
                res['value'] = {'award_target_kind': None, 'award_project': None, 'check_project': None}
                return res

        if not self.award_target_kind:
            res['domain'] = {'award_project': [(1, '=', 1)]}

            return res
        elif not self.check_project:
            record = self.env['funenc_xa_station.award_standard'].search(
                [('award_project','=',self.award_project.id),('award_standard_kind', '=', self.award_target_kind.id)])

            ids = [i['check_project'][0].id for i in record]

            res['domain'] = {'check_project': [('id', 'in', ids)]}
            res['value'] = {'check_project': None}

            return res

    #在修改考核项目的时候返回参考奖励的值
    @api.onchange('check_project')
    def get_refer_check_value(self):
        res = {}
        if self.award_target_kind and self.award_project and self.check_project:
            record = self.env['funenc_xa_station.award_standard'].search([
                ('award_standard_kind','=',self.award_target_kind.id),
                ('award_project','=',self.award_project.id),
                ('check_project','=',self.check_project.id)
            ])
            if not record:
                res['value'] = {'award_target_kind': None, 'award_project': None,}
                return res
        if not self.check_project:
            res['domain'] = {'check_project': [(1, '=', 1)]}

            return res
        elif not self.award_target_kind or self.award_project:
            record = self.env['funenc_xa_station.award_standard'].search_read(
                [('check_project','=',self.check_project.id)])
            if record:
                self.award_money_kind = record[0].get('award_standard')
                self.award_target_kind = record[0]['award_standard_kind'][0]
                self.award_project = record[0]['award_project'][0]



    #自动获取登录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return
        return self.env.user.dingtalk_user.name

    #用来对照前端的tab页面
    @api.model
    @get_domain
    def get_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.award_record_tree').id
        return {
            'name': '奖励记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "list"]],
            'res_model': 'funenc_xa_station.award_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                                  [
                                      {'title': '考评记录',
                                      'action':  'funenc_xa_station.check_record_act',
                                      'group':'funenc_xa_station.table_evaluation_record',
                                      },
                                      {
                                          'title': '考评汇总',
                                          'action2' : 'funenc_xa_station.funenc_xa_check',
                                          'group' : 'funenc_xa_station.table_evaluation_total',
                                          },
                                      {
                                          'title': '奖励记录',
                                          'action2':  'funenc_xa_station.award_record_act',
                                          'group' : 'funenc_xa_station.table_reward_record',
                                          },
                                     {
                                          'title': '奖励汇总',
                                          'action2':  'funenc_xa_station.funenc_xa_award',
                                          'group' : 'funenc_xa_station.table_reward_total',
                                          },
                                  ]
                              }''',
            'context': self.env.context,
        }

    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.award_record_tree').id
        return {
            'name': '奖励记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.award_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                              [
                                  {'title': '考评记录',
                                  'action':  'funenc_xa_station.check_record_act',
                                  'group':'funenc_xa_station.table_evaluation_record',
                                  },
                                  {
                                      'title': '奖励记录',
                                      'action2':  'funenc_xa_station.award_record_act',
                                      'group' : 'funenc_xa_station.table_reward_record',
                                      },
                              ]
                          }''',
            'context': self.env.context,
        }

    @api.model
    def create(self, vals):
        record = vals.get('award_record_add')
        if record:
            for i in record:
                key = {
                    'line_id':vals['line_id'],
                    'site_id':vals['site_id'],
                    'award_target_kind':vals['award_target_kind'],
                    'award_project':vals['award_project'],
                    'check_project':vals['check_project'],
                    'award_money_kind':vals['award_money_kind'],
                    'award_money':i[2]['award_money'],
                    'incident_describe':i[2]['incident_describe'],
                    'staff':i[2]['staff'],
                }
                super(AwardRecord, self).create(key)

        #用来和人员信息表关联
        vals['relevance_award'] = vals['staff']
        return super(AwardRecord, self).create(vals)

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

    def check_record_delete(self):
        self.env['funenc_xa_station.award_record'].search([('id', '=', self.id)]).unlink()

    #修改当前的一条记录
    def check_record_change(self):
        view_form = self.env.ref('funenc_xa_station.award_record_form_modify').id
        return {
            'name': '奖励记录',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.award_record',
            'res_id': self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


class AwardRecordAdd(models.Model):
    _name = 'funenc_xa_station.award_record_add'

    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工')
    jobnumber = fields.Char(related='staff.jobnumber',string='工号',readonly=True)
    award_money = fields.Char(string='奖励金额')
    incident_describe = fields.Char(string='事件描述')
    associated = fields.Many2one('funenc_xa_station.award_record')




