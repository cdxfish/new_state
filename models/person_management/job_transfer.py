# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields

class JobTransfer(models.Model):
    _name = 'persom_namagement.jobt_ranfer'
    _inherit = 'fuenc_station.station_base'


    def _default_associated(self):
        if self._context.get('active_id', False):
            return self._context['active_id']

    associated = fields.Many2one('fuenc_xa_station.guests_hurt', string='关联字段',default=_default_associated)


    # department = fields.Char(string='所属部门')
    # line_gauze = fields.Char(string='所属线网')
    station = fields.Char(string='车站')
    site_post = fields.Char(string='定岗/转岗岗位')
    site_time = fields.Date(string='定岗/转岗时间')
    site_file = fields.Char(string='定岗转岗文件号')
    relevance = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='姓名',default=_default_associated)

    #删除当前的记录
    def person_cer_delete(self):
        self.env['persom_namagement.jobt_ranfer'].search([('id','=',self.id)]).unlink()

    #修改当前的记录
    def person_cer_edit(self):
        return {
            'name': '人员管理系统',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'persom_namagement.jobt_ranfer',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target':'new'
        }
