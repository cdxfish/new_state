# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

import xlwt

key = [('safety','安全管理')
        ,('technology','技术管理')
        ,('road','施工管理')
        ,('ticket','票务管理')
        ,('server','服务管理')
        ,('train','培训管理')
        ,('goods','物资管理')
        ,('personnel','人事绩效管理')
        ,('party','党务管理')
        ,('integrated','综合管理')]

class CheckStandard(models.Model):

    _name = 'funenc_xa_station.check_standard'
    _rec_name = 'check_standard'
    _description = '考评指标'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    check_standard = fields.Selection(key,string='考核指标',required=True, track_visibility='onchange')
    problem_kind = fields.Many2one('problem_kind_record',string='问题类型',required=True, track_visibility='onchange')
    check_project = fields.Many2one('check_project_record',string='考核项目', track_visibility='onchange')
    check_parment = fields.Char(string='考核分部（室）分值', track_visibility='onchange')
    loca_per_score = fields.Char(string='当事人考核分值', track_visibility='onchange')
    relate_per_score = fields.Char(string='相关负责人考核分数', track_visibility='onchange')
    station_per_score = fields.Char(string='车站站长考核分数', track_visibility='onchange')
    technology_score = fields.Char(string='技术职/能考核分数', track_visibility='onchange')
    technology_serve = fields.Char(string='技术服务室', track_visibility='onchange')
    duty_partment = fields.Char(string='责任部门', track_visibility='onchange')
    management_score = fields.Char(string='管理岗考核分值', track_visibility='onchange')
    technology_serve_director = fields.Char(string='技术服务室分管服务主任/副主任', track_visibility='onchange')
    duty_director = fields.Char(string='责任分部主任/副主任', track_visibility='onchange')
    comment = fields.Text(string='备注', track_visibility='onchange')
    _sql_constraints = [('name_unique', 'unique(check_project)', "填写的考核项目已经存在")]

    #用来限制同一个考核指标型下面的问题类型不能重复
    @api.onchange('problem_kind')
    def constrains_name(self):
        res = {}
        if not self.problem_kind:
            res['domain'] = {'problem_kind': [(1, '=', 1)]}

            return res
        if len(self.env['funenc_xa_station.check_standard'].search([
            ('check_standard', '=', self.check_standard),
            ('problem_kind', '=', self.problem_kind.id)
        ])) > 0:
            raise ValidationError('同一考核指标下问题类型不能重复')


    # 权限server考评指标隐藏还是显示
    @api.model
    def get_day_plan_publish_action(self):
        view_tree = self.env.ref('funenc_xa_station.check_evaluate_tree').id
        return {
            'name': '考评指标',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.check_standard',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                             [
                                 {'title': '考评指标',
                                 'action':  'funenc_xa_station.check_evaluate_act',
                                 'group':'funenc_xa_station.table_reward_index',
                                 },
                                 {
                                     'title': '奖励指标',
                                     'action2' : 'funenc_xa_station.award_standard_act',
                                     'group' : 'funenc_xa_station.table_reward_index',
                                     },
                             ]
                         }''',
            'context': self.env.context,
        }

    @api.model
    def new_add_record(self):
        a = 1
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.check_standard',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


    def check_evalulate_edit(self):
        return{
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.check_standard',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def check_evaluate_delete(self):
        self.env['funenc_xa_station.check_standard'].search([('id', '=', self.id)]).unlink()

    def check_evaluate_import(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'evaluate_import',
            'res_id': self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def impotr_evaluate_file(self):
        self.env['evaluate_import'].search([]).import_xls_bill()



class ProblemKindRecord(models.Model):
    _name = 'problem_kind_record'
    # _rec_name = 'name'

    name = fields.Char(string='问题类型')
    # check_standard = fields.Selection(key, string='考核指标类型')
    # one_manys = fields.One2many('funenc_xa_station.check_standard','problem_kind',string='关联')

class CheckProjectRecord(models.Model):
    _name = 'check_project_record'
    # _rec_name = 'name'

    name = fields.Char(string='考核项目')
    _sql_constraints = [('name_unique', 'unique(name)', "填写的考核项目必须唯一")]




