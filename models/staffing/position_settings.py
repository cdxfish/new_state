# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import models, fields, api

MODULE_NAME = 'funenc_xa_station'
CATEGORY_ID_LIST = ['module_category_fuenc', 'module_category_run', 'module_category_comprehensive','module_position11',
                    'module_category_people', 'module_category_setting', 'module_category_jurisdiction']
CACHE_LIST = []


class PositionSettings(models.Model):
    _inherit = 'res.groups'
    _description = '职位设置'
    _parent_store = True  # set to True to compute MPTT (parent_left, parent_right)
    parent_id = fields.Many2one('res.groups', ondelete='cascade')
    child_ids = fields.One2many('res.groups', 'parent_id')
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    sequence = fields.Integer(index=True, default=0)

    def recursion_tree_data(self, cats):
        '''
        递归添加group树
        :param cats: 根节点的list
        :return:
        '''
        for cat in cats:
            if len(cat['child_ids']) == 0:
                cat['children'] = []
            else:
                cat['children'] = self.search_read([
                    ('id', 'in', cat['child_ids'])], fields=['name', 'child_ids', 'parent_left', 'parent_right'],
                    order='sequence')
                self.recursion_tree_data(cat['children'])
        return

    @api.model
    def get_group_data(self, group_id):
        '''
        获取group树和template模板
        :param group_id: 当前group的id，如果是新建，则此值为None
        :return:
        '''
        global CACHE_LIST
        category_id = self.env.ref('{}.{}'.format(MODULE_NAME, 'module_category_custom_groups'))
        category_id.ensure_one()
        # 获取父节点
        # 组装子节点
        if len(CACHE_LIST) == 0:
            category_record_ids = [self.env.ref('{}.{}'.format(MODULE_NAME, i)).id for i in CATEGORY_ID_LIST]
            cats = self.search_read([('category_id', 'in', category_record_ids), ('parent_id', '=', None)], fields=[
                'name', 'parent_id', 'child_ids', 'parent_left', 'parent_right', 'category_id'], order='sequence')
            self.recursion_tree_data(cats)
            CACHE_LIST = cats
        # 获取已选择节点
        checked_groups_ids = self.browse(group_id).implied_ids.filtered(lambda x: len(x.child_ids) == 0).ids
        template = self.env['vue_template_manager.template_manage'].get_template_content(
            'funenc_xa_station', 'group_config')
        rst = dict(cats=CACHE_LIST, template=template, checked_groups_ids=checked_groups_ids)
        return rst

    @api.model
    def add_or_write_custom_group(self, open_type, group_id, group_name, implied_ids):
        '''
        添加或更改依赖组
        :param open_type: 'add' or 'update'
        :param group_id: 当前组id
        :param group_name: 当前组name
        :param implied_ids: 选中的group_id
        :return:
        '''
        category_id = self.env.ref('funenc_xa_station.module_category_custom_groups')
        category_id.ensure_one()
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

    @api.model
    def import_position_user_button(self):
            # context = dict(self.env.context or {})
            view_form = self.env.ref('funenc_xa_station.import_position_user_form').id
            return {
                'name': '导入角色组成员',
                "type": "ir.actions.act_window",
                "res_model": "import_group_user",
                "views": [[view_form, "form"]],
                'target': 'new',
                'context': {},
            }

    def act_group_users(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_group_form').id
        return {
            'name': '角色组成员',
            "type": "ir.actions.act_window",
            "res_model": "res.groups",
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': {},
            'res_id': self.id
        }

