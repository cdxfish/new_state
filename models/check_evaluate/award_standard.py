# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AwardStandard(models.Model):
    _name = 'funenc_xa_station.award_standard'
    _rec_name = 'award_project'
    award_standard_default = fields.Char(string='指标类型',default='奖励标准',readonly=True)
    award_standard_kind = fields.Char(string='奖励指标类')
    award_project = fields.Char(string='奖励项目')
    check_project = fields.Char(string='考核项目')
    award_standard = fields.Char(string='奖励标准')
    support_file = fields.Char(string='支持文件')
    comment = fields.Char(string='备注')

    @api.model
    def new_add_standard(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.award_standard',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


    def award_edit(self):
        return{
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.award_standard',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def award_delete(self):
        self.env['funenc_xa_station.award_standard'].search([('id', '=', self.id)]).unlink()