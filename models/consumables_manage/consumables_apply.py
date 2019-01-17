import odoo.exceptions as msg
from odoo import models, fields, api
from ..get_domain import get_domain

import json

class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_apply'
    _description = u'耗材申请'
    _order = 'id desc'

    to_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标部门',
        #                                default=lambda
        # self: self.default_to_department_id()
                                       )
    to_parent_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标父部门')
    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='申请部门',
        #                             default=lambda
        # self: self.default_department_id()
                                    )
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type',string='耗材名称', required=True)
    consumables_count = fields.Integer(string='申请数量')
    is_apply = fields.Selection(string='是否已开始申请', selection=[('yes', '是'), ('no', '否')],default="no")
    apply_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='申请人')
    state = fields.Selection(selection=[('已处理','已处理'),('未处理','未处理')],default="未处理")
    manage_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='处理人')
    manage_time = fields.Datetime('处理时间')

    storage_id = fields.Integer(string='耗材出库id')

    product_departments_domain = fields.Char(
        compute="_compute_product_departments_domain",
        readonly=True,
        store=False,
    )

    @api.multi
    @api.depends('department_id')
    def _compute_product_departments_domain(self):
        if self.env.user.id == 1:
            domain = []
        else:
            departments_ids = self.env.user.dingtalk_user.user_property_departments.ids
            domain = [('id', 'in', departments_ids)]

        for rec in self:
            rec.product_departments_domain = json.dumps(
                domain
            )

    @api.onchange('department_id')
    def onchange_department_id(self):
        if not self.department_id:
            return

        department_id = self.department_id
        parent_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('departmentId', '=', department_id.parentid)]).id
        return {
            'domain': {
                'to_department_id': [('id','=',parent_id)]
            }
            ,
            'value': {
                'to_department_id': parent_id
            }
        }

    @api.model
    def init_data(self):
        if self.env.user.id == 1:
            domain = [('state','=','未处理')]
        else:
            ding_user = self.env.user.dingtalk_user
            ids = ding_user.user_property_departments.ids
            domain = [('state','=','未处理'),('to_department_id','in',ids)]


        context = dict(self.env.context or {})
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_apply_list').id
        return {
            'name': '耗材申请列表',
            'type': 'ir.actions.act_window',
            'res_model': 'funenc_xa_station.consumables_apply',
            'context': context,
            'target': 'current',
            "views": [[view_tree, "tree"]],
            'domain':domain,
        }


    @api.model
    def create_consumables_apply(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材申请创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_apply',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材申请编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_apply',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def apply(self):
        context = dict(self.env.context or {})
        context['apply_id'] = self.id
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_delivery_storage_form_2').id
        return {
            'name': '耗材出库',
            'type': 'ir.actions.act_window',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
            "views": [[view_form, "form"]],
            'res_id':self.storage_id
        }

    def delete(self):
        self.unlink()

    def default_to_department_id(self):
        if self.env.user.id != 1:

            department_id = self.env.user.dingtalk_user.departments[0]
            parent_department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('departmentId', '=', department_id.parentid)])
            return parent_department.id or None
        else:
            return

    def default_department_id(self):
        if self.env.user.id != 1:
            return self.env.user.dingtalk_user.departments[0].id
        else:
            return

    def consumables_apply_save(self):
        if self.consumables_count == 0:
            raise msg.Warning('申请数量不能为0')
        values = {'department_id':self.to_department_id.id,
                  'delivery_storage_department': self.department_id.id,
                  'consumables_type': self.consumables_type.id,
                  'consumables_count': self.consumables_count,
                  'is_delivery': 'no',
                  'consumables_apply_id': self.id,

                  }
        obj = self.env['funenc_xa_station.delivery_storage'].create(values)
        self.storage_id = obj.id
        self.is_apply = 'yes'
        self.apply_user_id = self.env.user.dingtalk_user.id  if self.env.user.id!=1 else None


    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_inventory_list').id
        return {
            'name': '耗材入库',
            'type': 'ir.actions.act_window',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.consumables_inventory',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                               [
                                   {'title': '耗材入库',
                                   'action':  'funenc_xa_station.xa_station_consumables_inventory_action',
                                   'group':'funenc_xa_station.consumables_management_consumables_storage',
                                   },
                                   {
                                       'title': '耗材申请',
                                       'action2' : 'funenc_xa_station.xa_station_consumables_apply_action',
                                       'group' : 'funenc_xa_station.consumables_management_consumables_apply',
                                       },
                                   {
                                       'title': '出入库记录',
                                       'action2':  'funenc_xa_station.award_record_act',
                                       'group' : 'funenc_xa_station.consumables_management_consumables_record',
                                       },
                               ]
                           }''',
            'context': self.env.context,
        }
