# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api


class ConflictRule(models.Model):
    _name = 'funenc_xa_station.conflict_rule'
    _description = '冲突规则'
    _order = 'conflict_rule_index asc'
    _inherit = 'fuenc_station.station_base'

    conflict_rule_index = fields.Integer(string='序号', default =1)
    conflict_rule_content = fields.Char(string='内容')
    conflict_rule = fields.Char(string='条件')  #用于tree 显示
    save_conflict_rule = fields.Integer(string='保存条件')   #用于form保存条件
    conflict_rule_state = fields.Selection(selection=[('enable','启用'), ('discontinuation', '停用')])

    is_certificate = fields.Integer(string='证书', default =1)  #用来判断该记录是否是证书具备
    conflict_rule_to_station_certificate = fields.One2many('conflict_rule_station_certificate_ref', 'conflict_rule_id', string='')



    @api.model
    def init_data(self):
        # 其他权限组进来还没有判断
        if self.env.user.id == 1:
            return {
                'name': '冲突规则',
                'type': 'ir.actions.act_window',
                "views": [[False, 'tree']],
                'res_model': 'funenc_xa_station.conflict_rule',
                'context': self.env.context,
                'target': 'current',
            }
        #
        department_id = self.env.user.dingtalk_user.departments[0]
        site_id = department_id.id
        line_id = self.env.user.dingtalk_user.line_id.id
        if department_id.department_hierarchy == 3:
            # 形如
            # values ={
            #     'line_id':
            #     'site_id':
            #     'conflict_rule_index': 1,
            #     'conflict_rule_content': '班与班之间的时间间隔≤',
            #     'conflict_rule': '12h',
            #     'save_conflict_rule': 12
            #     'conflict_rule_state': 'enable',
            #     'is_certificate': 2
            # }
            site_conflict_rule = self.search([('site_id', '=', site_id)])
            if not site_conflict_rule:

                sel_sql = "insert into funenc_xa_station_conflict_rule(line_id,site_id,conflict_rule_index,conflict_rule_content," \
                          "conflict_rule,save_conflict_rule,conflict_rule_state,is_certificate) " \
                          "values({},{},1, '班与班之间的时间间隔≤', '12h',12, 'enable', 2),({},{},2, '每人纯休的连续时间≤', '2d',2, 'enable', 2)," \
                          "({},{},3, '夜班第2天必须排休', '2d',2, 'enable', 2),({},{},4, '每个班组必须具备证书', null, 0, 'enable', 1)".format(
                          line_id,site_id,line_id,site_id,line_id,site_id,line_id,site_id
                )
                self.env.cr.execute(sel_sql)

            return {
                'name': '冲突规则',
                'type': 'ir.actions.act_window',
                "views": [[False, 'tree']],
                'res_model': 'funenc_xa_station.conflict_rule',
                'context': self.env.context,
                'target': 'current',
                'domain': [('site_id','=', site_id)]
            }


    def conflict_rule_enable(self):
        self.conflict_rule_state = 'discontinuation'

    def conflict_rule_discontinuation(self):
        self.conflict_rule_state = 'enable'

    def conflict_rule_edit(self):
        context = dict(self.env.context or {})

        if self.is_certificate == 1:

            view_form = self.env.ref('funenc_xa_station.funenc_xa_station_conflict_rule_form_4').id
            return {
                'name': '证书设置',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.conflict_rule',
                'context': context,
                'flags': {'initial_mode': 'edit'},
                'target': 'new',
                'res_id': self.id,
            }

        else:
            if self.conflict_rule_index ==1:
                view_form = self.env.ref('funenc_xa_station.funenc_xa_station_conflict_rule_form_1').id
            else:
                view_form = self.env.ref('funenc_xa_station.funenc_xa_station_conflict_rule_form_2').id

            return {
                'name': '条件修改',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.conflict_rule',
                'context': context,
                'flags': {'initial_mode': 'edit'},
                'target': 'new',
                'res_id': self.id,
            }

    @api.constrains('save_conflict_rule')
    def constrains_save_conflict_rule(self):
        if self.conflict_rule_index ==1 :
            self.conflict_rule = str(self.save_conflict_rule) + 'h'
        else:
            self.conflict_rule = str(self.save_conflict_rule) + 'd'


class conflict_rule_station_certificate(models.Model):
    _name = 'conflict_rule_station_certificate_ref'
    _description = '冲突规则人员证件中间表'

    conflict_rule_id = fields.Many2one('funenc_xa_station.conflict_rule', string='冲突规则关联')
    station_certificate_id = fields.Many2one('person.certificate', string='人员证件关联')





