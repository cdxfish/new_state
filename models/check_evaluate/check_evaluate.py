# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, fields, models

import xlwt

class CheckStandard(models.Model):
    _name = 'funenc_xa_station.check_standard'
    _rec_name = 'check_project'

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



    check_standard = fields.Selection(key,string='考核指标')
    problem_kind = fields.Char(string='问题类型',required=True)
    check_project = fields.Text(string='考核项目',required=True)
    check_parment = fields.Integer(string='考核分部（室）分值')
    loca_per_score = fields.Integer(string='当事人考核分值')
    relate_per_score = fields.Integer(string='相关负责人考核分数')
    station_per_score = fields.Integer(string='车站站长考核分数')
    technology_score = fields.Integer(string='技术职/能考核分数')
    technology_serve = fields.Char(string='技术服务室')
    duty_partment = fields.Char(string='责任部门')
    management_score = fields.Integer(string='管理岗考核分值')
    technology_serve_director = fields.Char(string='技术服务室分管服务主任/副主任')
    duty_director = fields.Char(string='责任分部主任/副主任')
    comment = fields.Text(string='备注')

    # 群信server考评指标隐藏还是显示
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
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.check_standard',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            # 'target': 'new',
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




