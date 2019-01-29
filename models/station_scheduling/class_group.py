# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

from ..get_domain import get_domain


class ClassGroup(models.Model):
    '''
        班组管理
    '''

    _name = 'funenc_xa_station.class_group'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _description = u'班组管理'

    name = fields.Char(string='班组名称', required=True)
    group_user_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'class_group_dingtalk_user_1_ref',
                                      'class_group_id', 'ding_talk_user_id', string='班组人员')

    # arrange_class_manage_ids =  fields.One2many('funenc_xa_station.arrange_class_manage', 'arrange_class_obj', string='排班规则对应')

    @get_domain
    @api.model
    def init_data(self, domain):
        context = {}
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_class_group_list').id
        return {
            'name': '班组管理',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.class_group",
            "views": [[view_tree, "tree"]],
            "domain": domain,
            'target': 'current',
            'context': context,
        }

    def create_class_group(self):
        context = dict(self.env.context or {})
        return {
            'name': '新增班组',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.class_group',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def class_group_edit(self):
        context = dict(self.env.context or {})
        unselected_user_ids = self.unselected_user_ids(self.site_id.id)
        return {
            'name': '班组详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.class_group',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
            'domain': {'group_user_ids': [('id', 'in', unselected_user_ids)]}
        }

    @api.onchange('site_id')
    def onchange_site_id(self):
        if not self.site_id:
            domain = [('id', '<', 0)]
        else:
            unselected_user_ids = self.unselected_user_ids(self.site_id.id)
            domain = [('id', 'in', unselected_user_ids)]

        return {
            'domain': {'group_user_ids': domain}
        }

    def class_group_delete(self):
        self.unlink()

    def unselected_user_ids(self, site_id):
        # 班组可选人员过滤
        department_property_users = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(site_id).department_property_users
        pop_user_ids = []
        tmp_department_user_ids = department_property_users.ids
        for department_property_user in department_property_users:  # 用户的部门属性
            self_departments = department_property_user.user_property_departments
            for self_department in self_departments:
                if self_department.department_hierarchy != 3:
                    pop_user_ids.append(department_property_user.id)
                    break
        department_user_ids = list(set(tmp_department_user_ids) - set(pop_user_ids))
        select_user_ids_list = []
        for obj in self.search([('site_id', '=', site_id)]):
            select_user_ids_list = select_user_ids_list + obj.group_user_ids.ids

        return list(set(department_user_ids) - set(select_user_ids_list))
