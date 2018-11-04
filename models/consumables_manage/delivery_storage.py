import odoo.exceptions as msg
from odoo import models, fields, api

class delivery_storage(models.Model):
    _name = 'funenc_xa_station.delivery_storage'
    _description = u'耗材出库'

    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='部门',default=lambda
        self: self.default_department_id())
    delivery_storage_department = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='出库申请部门')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材类型')
    consumables_count = fields.Integer(string='出库数量')
    store_house_ids = fields.One2many('funenc_xa_station.delivery_storage_to_consumables_inventory','delivery_storage_id',string='出库仓库')
    is_delivery = fields.Selection(selection=[('yes','已出库'),('no','未出库')],default="no")
    consumables_apply_id = fields.Many2one('funenc_xa_station.consumables_apply',string='申请出库关联')

    @api.multi
    def get_day_plan_publish_action(self):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_delivery_storage_list').id
        return {
            'name': '耗材入库',
            'type': 'ir.actions.act_window',
            # 'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.delivery_storage',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                                          [
                                              {
                                                  'title': '耗材入库',
                                                  'action' : 'funenc_xa_station.xa_station_consumables_delivery_storage',
                                                  'group' : 'funenc_xa_station.consumables_management_consumables_storage',
                                                  },
                                              {
                                                  'title': '耗材出库',
                                                  'action2':  'funenc_xa_station.xa_station_consumables_delivery_storage',
                                                  },
                                          ]
                                      }''',
            'context': self.env.context,
        }

    def default_department_id(self):
        if self.env.user.id != 1:
            return  self.env.user.dingtalk_user.departments[0].id
        else:
            return

    @api.model
    def create_delivery_storage(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def is_delivery_button(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def consumables_export_search_button(self):
        pass

    def delivery_storage_save(self):
        sel_inventory_count = sum(store_house_id.sel_inventory_count for store_house_id in self.store_house_ids)  # 出库数量
        if self.consumables_count == sel_inventory_count:
            values ={'consumables_department_id': self.delivery_storage_department.id,
                     'consumables_type_id': self.consumables_type.id,
                     'warehousing_count': sel_inventory_count

            }

            self.env['funenc_xa_station.consumables_warehousing'].create(values)
            self.is_delivery = 'yes'
            for store_house_id in self.store_house_ids:
                store_house_id.inventory_count = store_house_id.inventory_count - sel_inventory_count
        else:
            raise msg.Warning('出库数量必须和选择的出库数量相等')

class delivery_storage_to_consumables_inventory(models.Model):

    '''
     出库库存中间表
    '''

    _name = 'funenc_xa_station.delivery_storage_to_consumables_inventory'
    delivery_storage_id = fields.Many2one('funenc_xa_station.delivery_storage',string='出库关联')
    consumables_inventory_id = fields.Many2one('funenc_xa_station.consumables_inventory',string='库存关联')
    inventory_count = fields.Integer(string='库存数量', related='consumables_inventory_id.inventory_count')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材类型',related='consumables_inventory_id.consumables_type')
    sel_inventory_count = fields.Integer(string='选择出库数量')