# -*- coding: utf-8 -*-
import odoo.exceptions as msg

from odoo import models, fields, api

MODULE_NAME = 'funenc_xa_station'
CATEGORY_ID_LIST = ['module_category_fuenc']


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
            checked_groups = self.browse(group_id).implied_ids
            cats.append({
                'name': category_record.display_name,
                'groups': [{'id': i.id, 'name': i.name} for i in groups],
                'checkedGroups': [j.id for j in checked_groups],
                'isIndeterminate': False,
                'checkAll': False if len(checked_groups) != len(groups) else True,
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

    def create_position_settings_button(self):
        return {
            'name': '职位创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.groups',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }
