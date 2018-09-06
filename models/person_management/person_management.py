# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class MainModel(models.Model):
    _name = 'main.information'
    staff_basic_information = fields.One2many('person.management.sys','name',string='员工基础信息')
    staff_business_information = fields.One2many('employee.business.information','department',string='员工企业信息')
    staff_number = fields.Char(related='staff_basic_information.staff_number', string='工号')
    name = fields.Many2one(related='staff_basic_information.name',string='姓名')
    gender = fields.Char(related='staff_basic_information.gender',string='性别')
    nation = fields.Char(related='staff_basic_information.nation',string='民族')
    politics_status = fields.Char(related='staff_basic_information.politics_status',string='政治面貌')
    department = fields.Many2one(related='staff_business_information.department', string='分部')
    post = fields.Char(related='staff_business_information.post',strin9g='岗位')
    phone = fields.Char(related='staff_basic_information.phone',string='联系电话')
    #持证信息
    certificate_info = fields.One2many('person.certificate','name',string='持证信息')
    #转岗信息
    transfer_info = fields.One2many('persom_namagement.jobt_ranfer','site_file',string='转岗信息')
    #考评记录
    check_info = fields.One2many('person_management.check_info','relevance',string='考评记录')
    #奖励制度
    award_info = fields.One2many('person_management.award_info','relevance',string='关联字段')

class PersonManagement(models.Model):
    _name = 'person.management.sys'

    staff_number = fields.Char(string='员工工号')
    name = fields.Many2one('main.information',string='姓名')
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
    major =fields.Char(string='专业')
    second_degree_major = fields.Char(string='第二学历')
    second_degree = fields.Char(string='第二学位')
    second_school_of_graduation = fields.Char(string='毕业院校')
    second_major = fields.Char(string='专业')





