# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class BelongToManagement(models.Model):
    _name = 'funenc_xa_station.belong_to_management'
    _inherit = 'fuenc_station.station_base'

    post_check = fields.Selection([('guard','保安'),('check','安检'),('clean','保洁')],string='岗位检查')
    check_time = fields.Datetime(string='检测时间')
    check_state = fields.Text(string='检测情况')
    find_problem = fields.Text(string='发现问题')
    reference_according = fields.Char(string='参考依据')
    local_image = fields.Binary(string='现场照片')
    check_score = fields.Integer(string='参考分值')
    note = fields.Char(string='备注')
    write_person = fields.Char(string='填写人')
    change_state = fields.Selection([('add','加'),('reduce','减')],dafault='reduce')
    summary_score = fields.Integer(string='总分值', default=100)
    check_count = fields.Integer(string='检查次数',default=1)

    def create_belong_to_action(self):
        return {
            'name': '属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def belong_to_edit_action(self):
        return {
            'name': '属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete_action(self):
        self.env['funenc_xa_station.belong_to_management'].search([('id','=',self.id)]).unlink()



