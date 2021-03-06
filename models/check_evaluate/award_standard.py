# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class AwardStandard(models.Model):
    _name = 'funenc_xa_station.award_standard'
    _rec_name = 'award_project'
    award_standard_default = fields.Char(string='指标类型',default='奖励标准',readonly=True)
    award_standard_kind = fields.Many2one('award_standard_object',string='奖励指标类',required=True)
    award_project = fields.Many2one('award_award_project',string='奖励项目',required=True)
    check_project = fields.Many2one('award_check_project',string='考核项目',required=True)
    award_standard = fields.Char(string='奖励标准')
    support_file = fields.Char(string='支持文件')
    comment = fields.Char(string='备注')
    _sql_constraints = [('name_unique', 'unique(check_project)', "填写的考核项目必须唯一")]

    @api.model
    def create(self, vals):
        kind = vals.get('award_standard_kind')
        award = vals.get('award_project')
        check = vals.get('check_project')
        record = self.env['funenc_xa_station.award_standard'].search(
            [('award_standard_kind','=',kind),('award_project','=',award),('check_project','=',check)])
        if record:
            raise ValidationError('相同的考核指标已近存在了')
        return super(AwardStandard,self).create(vals)

    #群信server奖励指标隐藏还是显示
    @api.model
    def get_day_plan_publish_action(self):
        view_tree = self.env.ref('funenc_xa_station.award_standard_tree').id
        return {
            'name': '奖励指标',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.award_standard',
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
    def new_add_standard(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.award_standard',
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
            'res_model': 'funenc_xa_station.award_standard',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def award_delete(self):
        self.env['funenc_xa_station.award_standard'].search([('id', '=', self.id)]).unlink()

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

class AwardStandardObject(models.Model):
    _name = 'award_standard_object'

    name = fields.Char('奖励指标类')
    _sql_constraints = [('name_unique', 'unique(name)', "填写的奖励指标类必须唯一")]


class AwardProject(models.Model):
    _name = 'award_award_project'

    name = fields.Char(string='奖励项目')
    _sql_constraints = [('name_unique', 'unique(name)', "填写的奖励项目必须唯一")]


class CheckProject(models.Model):
    _name = 'award_check_project'

    name= fields.Char(string='考核项目')
    _sql_constraints = [('name_unique', 'unique(name)', "填写的考核项目必须唯一")]
