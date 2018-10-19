# -*- coding: utf-8 -*-
import odoo.exceptions as msg

from odoo import models, fields, api


class position_settiings(models.Model):
    _inherit = 'res.groups'
    _description = '职位设置'

    button_line_ids = fields.Many2many('funenc_xa_station.button_line', 'res_user_button_line_rel_1', 'group_id',
                                       'button_id', string='页面按钮设置')

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


def create_position_settings(self):
    self.env['ir.ui.view'].search(
        [('model', '=', 'res.groups'), ('name', '=', 'funenc_xa_station_res_groups_list')])
    return


class button_line(models.Model):
    _name = 'funenc_xa_station.button_line'
    _rec_name = 'button_name'

    button_name = fields.Char(string='按钮名字')
    model_id = fields.Char(string='模型名称')
    visible_button_name = fields.Char(string='可见的按钮名称')  # 准确匹配

    def create_data(self):
        self.env['ir.ui.view'].search(
            [('model', '=', 'res.groups'), ('name', '=', 'funenc_xa_station_res_groups_list')])
        return
