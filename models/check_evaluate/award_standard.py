# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AwardStandard(models.Model):
    _name = 'funenc_xa_station2.award_standard'
    _rec_name = 'award_project'
    award_standard_default = fields.Char(string='指标类型',default='奖励标准',readonly=True)
    award_standard_kind = fields.Char(string='奖励指标类')
    award_project = fields.Char(string='奖励项目')
    check_project = fields.Char(string='考核项目')
    award_standard = fields.Char(string='奖励标准')
    support_file = fields.Char(string='支持文件')
    comment = fields.Char(string='备注')

    #群信server奖励指标隐藏还是显示
    @api.model
    def get_day_plan_publish_action(self):
        view_tree = self.env.ref('funenc_xa_station2.award_standard_tree').id
        return {
            'name': '奖励指标',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station2.award_standard',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                             [
                                 {'title': '考评指标',
                                 'action':  'funenc_xa_station2.check_evaluate_act',
                                 'group':'funenc_xa_station2.table_reward_index',
                                 },
                                 {
                                     'title': '奖励指标',
                                     'action2' : 'funenc_xa_station2.award_standard_act',
                                     'group' : 'funenc_xa_station2.table_reward_index',
                                     },
                             ]
                         }''',
            'context': self.env.context,
        }

    @api.model
    def new_add_standard(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station2.award_standard',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


    def award_edit(self):
        return{
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station2.award_standard',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def award_delete(self):
        self.env['funenc_xa_station2.award_standard'].search([('id', '=', self.id)]).unlink()

    def award_standard_import(self):
        return{
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'award_import',
            'res_id': self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def import_award_file(self):
        self.env['award_import'].search([]).import_xls_bill()