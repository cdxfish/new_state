# -*- coding: utf-8 -*-

from odoo import api, models, fields


class Add_professional(models.Model):
    _name = 'xian_metro.professional'

    _rec_name = 'professional_kind'
    professional_kind = fields.Char(string='专业类型')
    note = fields.Char(string='备注')


    @api.model
    def professional_type(self):
        return {
            'name': '新增专业类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'xian_metro.professional',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def professional_edit(self):
        return {
            'professional_kind': '专业类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'xian_metro.professional',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def management_delete(self):
        self.env['xian_metro.professional'].search([('id', '=', self.id)]).unlink()

class Add_class(models.Model):
    _name = 'add_class.add_class'
    _rec_name = 'class_kind'
    class_kind = fields.Char(string='级别类型')
    note = fields.Char(string='备注')

    @api.model
    def add_class_type(self):
        return {
            'name': '新增专业类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add_class.add_class',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def class_edit(self):
        return {
            'class_kind': '级别类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add_class.add_class',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def class_delete(self):
        self.env['add_class.add_class'].search([('id', '=', self.id)]).unlink()