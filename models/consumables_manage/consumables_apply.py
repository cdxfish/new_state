import odoo.exceptions as msg
from odoo import models, fields, api
from ..get_domain import get_domain

class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_apply'
    _description = u'耗材申请'

    to_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标部门', default=lambda
        self: self.default_to_department_id())
    to_parent_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标父部门')
    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='申请部门', default=lambda
        self: self.default_department_id())
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type',string='耗材类型', required=True)
    consumables_count = fields.Integer(string='申请数量')
    is_apply = fields.Selection(string='是否已开始申请', selection=[('yes', '是'), ('no', '否')],default="no")

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
        context['self_id'] = self.id
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
        values = {'delivery_storage_department': self.to_department_id.id,
                  # 'consumables_type': self.consumables_type.id,
                  'consumables_count': self.consumables_count,
                  'is_delivery': 'no',
                  'consumables_apply_id': self.id,

                  }
        self.env['funenc_xa_station.delivery_storage'].create(values)

        self.is_apply = 'yes'

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
