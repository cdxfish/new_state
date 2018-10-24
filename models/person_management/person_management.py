# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class MainModel(models.Model):
    # _name = 'main.information'
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_users'


    gender = fields.Char(string='性别')
    # nation = fields.Char(string='民族')
    # politics_status = fields.Char(string='政治面貌')
    # department = fields.Char(string='分部')
    # position = fields.Text(string='岗位')
    phone = fields.Char(string='联系电话')
    certificate_info = fields.One2many('person.certificate','relevance',string='持证信息')
    #转岗信息
    transfer_info = fields.One2many('persom_namagement.jobt_ranfer','relevance',string='转岗信息')
    #考评记录
    check_info = fields.One2many('funenc_xa_station.check_record','relevance',string='考评记录')
    #奖励制度
    award_info = fields.One2many('funenc_xa_station.award_record','relevance',string='奖励记录')

    # staff_number = fields.Char(string='员工工号',compute='onchange_name_sta',readonly=True)
    # name_name = fields.Char(string='姓名',compute='onchange_name_sta',readonly=True)
    gender = fields.Char(string='性别')
    nation = fields.Char(string='民族')
    birth = fields.Date(string='出生日期')
    idcar = fields.Char(string='生份证号码')
    phone = fields.Char(string='联系电话')
    politics_status = fields.Char(string='政治面貌')
    shoe_size = fields.Char(string='鞋码')
    native_place = fields.Char(string='籍贯')
    native_sition = fields.Char(string='户籍地址')
    new_site = fields.Char(string='现住址')
    emergency_contact = fields.Char(string='紧急联系人')
    emergency_contact_phone = fields.Integer(string='联系人电话')
    First_degree_major = fields.Char(string='第一学历')
    first_degree = fields.Char(string='第一学位')
    school_of_graduation = fields.Char(string='毕业学校')
    major = fields.Char(string='专业')
    second_degree_major = fields.Char(string='第二学历')
    second_degree = fields.Char(string='第二学位')
    second_school_of_graduation = fields.Char(string='毕业院校')
    second_major = fields.Char(string='专业')
    certificate_status = fields.Selection([('one','正常'),('zero','缺失')],string='证书状态',default='one')
    email = fields.Char(string='邮箱')
    department = fields.Char(string='所属部门')
    department_load = fields.Char(string='所属线网')
    team_or_group_station = fields.Char(string='班主车站')
    # post = fields.Char(string='岗位')
    begin_time = fields.Date(string='入司时间')
    become_a_regular_worker_time = fields.Date(string='转正时间')
    join_work_time = fields.Date(string='参加工作时间')
    staff_source = fields.Char(string='员工来源')
    # load_line = fields.Char(string='线路')
    station_site = fields.Char(string='车站')

    # @api.constrains('jobnumber','name')
    # def onchange_name_sta(self):
    #     self.staff_number = self.jobnumber
    #     self.name_name = self.name

    def person_info(self):
        return {
            'name': '人员管理系统',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cdtct_dingtalk.cdtct_dingtalk_users',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
        }

    def person_cer_edit(self):
        form_edit = self.env.ref('funenc_xa_station.person_information_increase').id
        return {
            'name': '新增证件',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[form_edit, "form"]],
            'res_model': 'person.certificate',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def import_file_management(self):
        return {
            'name': '新增证件',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.management',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def synchronization_information(self):
       self.env['cdtct_dingtalk.cdtct_dingtalk_account'].search([])[0].sync_dingtalk()

    def import_xls_bill(self):
        self.env['import.management'].search([])[0].import_xls_bill()






