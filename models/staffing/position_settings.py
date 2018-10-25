# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from collections import defaultdict

from odoo import models, fields, api

MODULE_NAME = 'funenc_xa_station'
CATEGORY_ID_LIST = ['module_category_fuenc', 'module_category_run', 'module_category_comprehensive',
                    'module_category_people', 'module_category_setting', 'module_category_jurisdiction',
                    'module_passenger_service_interface_display', 'module_files_interface_display',
                    'module_change_shifts_list_interface_display', 'module_production_daily_interface_display',
                    'module_station_detail_interface_display', 'module_rules_type_interface_display',
                    'module_scheduling_setting_interface_display', 'module_scheduling_manage_interface_display',
                    'module_attendance_interface_display', 'module_evaluation_index_setting_interface_display',
                    'module_evaluation_index_manage_interface_display']


class PositionSettings(models.Model):
    _inherit = 'res.groups'
    _description = '职位设置'

    @api.model
    def get_group_data(self, group_id):
        category_id = self.env.ref('{}.{}'.format(MODULE_NAME, 'module_category_custom_groups'))
        category_id.ensure_one()
        cats = []
        for c_id in CATEGORY_ID_LIST:
            category_record = self.env.ref('{}.{}'.format(MODULE_NAME, c_id))
            groups = self.search([('category_id', '=', category_record.id)])
            checked_groups = self.browse(group_id).implied_ids.filtered(lambda x: x.category_id.id == category_record.id)
            cats.append({
                'name': category_record.display_name,
                'groups': [{'id': i.id, 'name': i.name} for i in groups],
                'checkedGroups': [j.id for j in checked_groups],
                'isIndeterminate': False,
                'checkAll': True if set([i.id for i in groups]) & set([j.id for j in checked_groups]) == set(
                    [i.id for i in groups]) else False,
                'xml_id': category_record.xml_id
            })
        template = self.env['vue_template_manager.template_manage'].get_template_content(
            'funenc_xa_station', 'group_config')
        rst = dict(cats=cats, template=template)
        return rst

    @api.model
    def add_or_write_custom_group(self, open_type, group_id, group_name, cats):
        category_id = self.env.ref('funenc_xa_station.module_category_custom_groups')
        category_id.ensure_one()
        implied_ids = []
        for cat in cats:
            implied_ids += cat['checkedGroups']
        if open_type == 'add':
            self.create({'name': group_name, 'category_id': category_id.id, 'implied_ids': [(6, 0, implied_ids)]})
        elif open_type == 'update':
            self.browse(group_id).write({'implied_ids': [(6, 0, implied_ids)]})
            # 删除group中用户

    @api.model
    def del_group_users(self, group_id, del_groups_ids, del_users_ids):
        '''
        清除对应组的人员
        '''
        groups = self.env['res.groups'].search(
            [('id', '!=', group_id),
             ('category_id', '=', self.env.ref('{}.{}'.format(MODULE_NAME, 'module_category_custom_groups')).id)])
        del_group_user_map = defaultdict(list)
        for item in del_groups_ids:
            del_group_user_map[item] = del_users_ids
        for group in groups:
            cur_group_users = group.users.ids  # 当前分组的用户
            deal_cur_groups_ids = list(set(group.implied_ids.ids).intersection(
                set(del_groups_ids)))  # 当前分组需处理的子分组
            for del_group_id in deal_cur_groups_ids:
                del_group_user_map[del_group_id] = list(
                    set(del_group_user_map[del_group_id]).difference(set(cur_group_users)))
        for group_id in del_group_user_map:
            if del_group_user_map[group_id]:
                records = self.env['res.groups'].browse(group_id)
                users_ids = list(set(records.users.ids).difference(
                    set(del_group_user_map[group_id])))
                records.write({
                    'users': [(6, 0, users_ids)]
                })

    @api.multi
    def write(self, vals):
        '''
        重写write，避免子组变化时，对应子组的人员的人员还具体原子组权限
        '''
        if 'implied_ids' in vals:  # 模块启动时也加载了此函数处理
            del_groups_ids = self.implied_ids.ids  # 修改之前关联的分组
            # 有组被删除时，手动处理
            if not set(self.implied_ids.ids).issubset(vals['implied_ids'][0][2]):
                del_groups_ids = list(set(del_groups_ids).difference(
                    set(vals['implied_ids'][0][2])))
                self.del_group_users(self.id, del_groups_ids, self.users.ids)
        if 'users' in vals and vals['users']:  # 删除父组的人时，自动去除子组的人
            # 有人被删除时，手动处理
            if not set(self.users.ids).issubset(vals['users'][0][2]):
                del_users_ids = list(
                    set(self.users.ids).difference(set(vals['users'][0][2])))
                self.del_group_users(
                    self.id, self.implied_ids.ids, del_users_ids)
        return super().write(vals)

    @api.multi
    def unlink(self):
        '''
        当前组的子组中人的删除处理：
        若其他组的子组中包含该子组，且当前组的子组中包含的人被被包含在该子组中，则不能删除，否则，删除
        '''
        for record in self:
            del_groups_ids = record.implied_ids.ids  # 需要删除的分组的
            self.del_group_users(record.id, del_groups_ids, record.users.ids)
            super(models.Model, record).unlink()

        return True
