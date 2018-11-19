import odoo.exceptions as msg
from odoo import models, fields, api
import datetime


class delivery_storage(models.Model):
    _name = 'funenc_xa_station.delivery_storage'
    _description = u'耗材出库'

    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='部门',
                                    # default=lambda
                                    # self: self.default_department_id()
                                    )
    delivery_storage_department = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='出库申请部门')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材名称')
    consumables_count = fields.Integer(string='出库数量')
    store_house_id = fields.Many2one('funenc_xa_station.consumables_inventory', string='库房名称')
    store_house_ids = fields.One2many('funenc_xa_station.delivery_storage_to_consumables_inventory',
                                      'delivery_storage_id', string='出库仓库')
    is_delivery = fields.Selection(selection=[('yes', '已出库'), ('no', '未出库')], default="no")
    consumables_apply_id = fields.Many2one('funenc_xa_station.consumables_apply', string='申请出库关联')
    outgoing_way = fields.Selection(string='出库方式', selection=[('组织', '组织'), ('个人', ('个人'))], default="组织")
    delivery_storage_date = fields.Date(string='出库时间')
    outgoing_user_name = fields.Char(string='个人姓名')
    department_name = fields.Char(string='部门名')


    # @api.constrains
    # def consumables_count(self):
    #     self.consumables_count = sum(store_house_id.sel_inventory_count for store_house_id in self.store_house_ids)

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
            return self.env.user.dingtalk_user.departments[0].id
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
        self.is_delivery = 'yes'
        self.delivery_storage_date = datetime.datetime.now()

        # for store_house_id in self.store_house_ids:
        #     store_house_id.consumables_inventory_id.write({
        #         'inventory_export': store_house_id.consumables_inventory_id - store_house_id.sel_inventory_count
        #     })

        for store_house_id in self.store_house_ids:
            store_house_id.inventory_count = store_house_id.inventory_count - store_house_id.sel_inventory_count

    def delivery_storage_save1(self):

        apply_id = self.env.context.get('apply_id')
        consumables_inventory =self.env['funenc_xa_station.consumables_inventory'].search(
            [('inventory_department_id', '=', self.department_id.id),
             ('consumables_type', '=', self.consumables_type.id)])
        if consumables_inventory:
            count = consumables_inventory.inventory_count - self.consumables_count
            if count>=0:
                consumables_inventory.inventory_count = count
                consumables_apply = self.env['funenc_xa_station.consumables_apply'].browse(apply_id)
                consumables_apply.state = '已处理'
            else:
                raise msg.Warning('库存不够')


        else:
            raise msg.Warning('未找到相应库存')

        self.is_delivery = 'yes'
        self.delivery_storage_date = datetime.datetime.now()



class delivery_storage_to_consumables_inventory(models.Model):
    '''
     出库库存中间表
    '''

    _name = 'funenc_xa_station.delivery_storage_to_consumables_inventory'
    delivery_storage_id = fields.Many2one('funenc_xa_station.delivery_storage', string='出库关联')
    consumables_inventory_id = fields.Many2one('funenc_xa_station.consumables_inventory', string='库存关联'
                                               )
    inventory_count = fields.Integer(string='库存数量', related='consumables_inventory_id.inventory_count')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材名称',
                                       related='consumables_inventory_id.consumables_type')
    sel_inventory_count = fields.Integer(string='选择出库数量')

    # @api.onchange('consumables_inventory_id')
    # def get_doamin(self):
    #     if self.env.user.id == 1:
    #         return []
    #     else:
    #         return {'domain': {'consumables_inventory_id': [
    #             ('inventory_department_id', '=', self.env.user.dingtalk_user.departments[0].id)]}}
