# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
from ..get_domain import get_domain

class AwardRecord(models.Model):
    _name = 'funenc_xa_station.award_record'
    _inherit = 'fuenc_station.station_base'


    # line_road = fields.Char(string='线路')
    # station_site = fields.Char(string='站点')
    jobnumber = fields.Char(related='staff.jobnumber',string='工号', readonly=True)
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='员工')
    position = fields.Text(related='staff.position',string='职位')
    award_money = fields.Char(string='奖励金额')
    award_target_kind = fields.Char(string='奖励指标类')
    award_project = fields.Many2one('funenc_xa_station.award_standard',string='奖励项目')
    check_project = fields.Char(string='考核项目')
    award_money_kind = fields.Char(related='award_project.award_standard',string='参考奖励')
    incident_describe = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人', default=lambda self: self.default_person_id())
    check_time = fields.Datetime(string='考评时间',default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    award_record_add = fields.One2many('funenc_xa_station.award_record_add','associated',string='新增责任人员')
    award_money = fields.Float(string='奖励金额')
    award_degree = fields.Integer(string='奖励次数',default=1)
    relevance = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='关联字段')

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
    def create(self, vals):
        record = vals['award_record_add']
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
        vals['relevance'] = vals['staff']
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

    def check_record_change(self):
        view_form = self.env.ref('funenc_xa_station.award_record_form').id
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




