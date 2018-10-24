# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from .. get_domain import get_domain

class BelongToManagement(models.Model):
    _name = 'funenc_xa_station.belong_to_management'
    _inherit = 'fuenc_station.station_base'

    post_check = fields.Selection([('guard', '保安'), ('check', '安检'), ('clean', '保洁')], string='岗位检查')
    check_time = fields.Datetime(string='检测时间', requird=True)
    check_state = fields.Text(string='检测情况')
    find_problem = fields.Text(string='发现问题')
    reference_according = fields.Char(string='参考依据')
    local_image = fields.Binary(string='现场照片')
    check_score = fields.Integer(string='考核分值')
    note = fields.Char(string='备注')
    # write_person = fields.Char(string='填写人')
    write_person = fields.Char(string='填报人',
                               default=lambda self: self.default_name_id())
    job_number = fields.Char(string='工号', default=lambda self: self.default_job_number_id())
    change_state = fields.Selection([('add', '加'), ('reduce', '减')], dafault='reduce')
    summary_score = fields.Integer(string='总分值', default=100)
    check_count = fields.Integer(string='检查次数', default=1)

    @get_domain
    def create_belong_to_action(self,domain):
        return {
            'name': '属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    # 获取前端输入的姓名
    @api.model
    def default_name_id(self):
        if self.env.user.id == 1:
            return
        return self.env.user.dingtalk_user.name

    # 获取前端输入的工号
    @api.model
    def default_job_number_id(self):
        if self.env.user.id == 1:
            return
        return self.env.user.dingtalk_user.jobnumber

    # 修改当前的记录
    def belong_to_edit_action(self):
        lol = self.env.user.dingtalk_user
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

    # 删除当前的记录
    def delete_action(self):
        self.env['funenc_xa_station.belong_to_management'].search([('id', '=', self.id)]).unlink()

    # 改变参考分数的正负数
    @api.onchange('change_state')
    def change_state_negative(self):
        if self.change_state == 'add':
            self.check_score = abs(self.check_score)
        elif self.change_state == 'reduce':
            self.check_score = -abs(self.check_score)

    @api.model
    def get_belong_to_management(self):

        ding_user = self.env.user.dingtalk_user
        department = ding_user.departments[0]
        if department.department_hierarchy == 1:

            return self.search_read([], ['id', 'summary_score', 'note', 'post_check', 'check_time'])
        elif department.department_hierarchy == 2:
            ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department.departmentId)]).ids

            self.search_read([('site_id', 'in', ids)],
                             ['id', 'summary_score', 'note', 'post_check', 'check_time'])
        else:
            return self.search_read([('site_id', '=', department.id)],
                                    ['id', 'summary_score', 'note', 'post_check', 'check_time'])

    @api.model
    def get_belong_to_management_by_id(self, id):
        select_id = int(id) or -1
        return self.search_read([('id', '=', select_id)],
                                ['find_problem', 'check_state', 'note', 'post_check', 'reference_according',
                                 'summary_score', 'local_image','check_time'])
