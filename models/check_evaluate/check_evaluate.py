# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CheckStandard(models.Model):
    _name = 'funenc_xa_station.check_standard'

    key = [('safety','安全管理')
        ,('technology','技术管理')
        ,('road','施工管理')
        ,('ticket','票务管理')
        ,('server','服务管理')
        ,('train','培训管理')
        ,('goods','物资管理')
        ,('personnel','人事绩效管理')
        ,('party','党务管理')
        ,('integrated','综合管理')]



    check_standard = fields.Selection(key,string='考核标准')
    problem_kind = fields.Char(string='问题类型',required=True)
    check_project = fields.Text(string='考核项目',required=True)
    check_parment = fields.Integer(string='考核分部（室）分值')
    loca_per_score = fields.Integer(string='当事人考核分值')
    relate_per_score = fields.Integer(string='相关负责人考核分数')
    station_per_score = fields.Integer(string='车站站长考核分数')
    technology_score = fields.Integer(string='技术职/能考核分数')
    technology_serve = fields.Char(string='技术服务室')
    duty_partment = fields.Char(string='责任部门')
    management_score = fields.Integer(string='管理岗考核分值')
    technology_serve_director = fields.Char(string='技术服务室分管服务主任/副主任')
    duty_director = fields.Char(string='责任分部主任/副主任')
    comment = fields.Text(string='备注')

    @api.model
    def new_add_record(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.check_standard',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def check_evalulate_edit(self):
        return{
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.check_standard',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def check_evaluate_delete(self):
        self.env['funenc_xa_station.check_standard'].search([('id', '=', self.id)]).unlink()