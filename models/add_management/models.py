# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import urllib
import base64
import os
from ..get_domain import get_line_ids

class xian_metro(models.Model):

    _name = 'xian_metro.xian_metro'
    _order = 'id desc'
    _rec_name = 'rules_name'
    _description = '规章制度'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # _inherit = 'fuenc_station.station_base'
    line_id = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department','line_id_site_id_ref','line_id','site_id',string='线路', track_visibility='onchange')
    site_id = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department', 'xian_metro_site_id_rel','xian_metro_id','site_id',string='站点', track_visibility='onchange')
    profession_kind = fields.Many2one('xian_metro.professional', string='专业分类', track_visibility='onchange')
    rank_kind = fields.Many2one('add_class.add_class', string='级别分类', track_visibility='onchange')
    rules_id = fields.Char(string='规章编号', track_visibility='onchange')
    rules_name = fields.Char(string='规章名称', track_visibility='onchange')
    # load_line = fields.Selection([('one', '一号线'), ('two', '二号线'), ('three', '三号线')], string='线路', default='one')
    # station_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='站点')
    details = fields.Binary(string='内容', track_visibility='onchange')
    file_name = fields.Char(string="File Name")
    operation_peison = fields.Char(string='操作人',default=lambda self: self.default_person_id(), track_visibility='onchange')
    operation_time = fields.Datetime(string='操作时间', default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_visibility='onchange')
    url = fields.Char(string='url')
    release_time = fields.Date(string='发布实施日期', track_visibility='onchange')
    rule_regulations_browse = fields.Selection([('one','内容显示'),('zero','内容不显示')],default='zero')

    # @api.onchange('line_id')
    # def change_line_id(self):
    #     lis = []
    #     if not self.line_id:
    #         self.site_id = ''
    #     else:
    #         line_id = self.line_id
    #         for i in line_id:
    #             lis.append(i.departmentId)
    #
    #         child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
    #             [('parentid', 'in', lis)]).ids
    #         site_domain = [('id', 'in', list(set(child_department_ids)))]
    #
    #         return {'domain': {'site_id': site_domain,
    #                            }
    #                 }



    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        line_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=', department_id.parentid)]).id

                line_ids.append(id)

        return line_ids
        # print(line_ids)

    # 自动获取操作人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name

    @api.model
    def xian_metro_type(self):
        return {
            'name': '新增规章',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'xian_metro.xian_metro',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def profession_kind_edit(self):
        return {
            'profession_kind': '专业分类',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'xian_metro.xian_metro',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def xian_metro_delete(self):
        self.env['xian_metro.xian_metro'].search([('id', '=', self.id)]).unlink()

    # 用来展示文件的样式
    @api.model
    def create(self, params):
        lis_line = []
        # lis_site =[]
        file_binary = params['details']
        for i in params.get('line_id'):
            for line in i[2]:
                char_line = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('id','=',line)])
                lis_line.append(char_line.name)
        # file = os.path.splitext(params.get('file_name'))
        # filename,type = file
        # if type != '.pdf':
        #     raise ValidationError('上传的文件需要时pdf文件，请重新改选择')
        file_name = params.get('file_name', self.file_name)
        if file_binary:
            url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
                'funenc_xa_station', file_name, base64.b64decode(file_binary))
            token = self.env['qiniu_service.qiniu_upload_bucket'].get_upload_token('funenc_xa_station')
            print(token)
            params['url'] = url
            params['file_name'] = file_name
            params['rule_regulations_browse'] = 'one'
        # url, key = self.env['qiniu_service.qiniu_upload_bucket'].upload_file(
        #     file_binary, 'pdf')
        # params['url'] = url
        # params['file_name'] = key
        return super(xian_metro, self).create(params)

    def view_details(self):
        url = self.url
        if url:
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }

    def file_kind_load(self):
        # view_form = self.env.ref('funenc_xa_station.add_operation_form_test').id
        # return {
        #     'name': '新增规范',
        #     'type': 'ir.actions.act_window',
        #     "views": [[view_form, "form"]],
        #     'res_model': 'xian_metro.xian_metro',
        #     'res_id': self.id,
        #     'flags': {'initial_mode': 'readonly'},
        #     'target': 'new',
        # }
        return {
            'type':'ir.actions.act_url',
            'url':'/funenc_xa_station/test_test?id=%d'%self.id,
        }

    @api.model
    def get_xian_metro_list(self):
        xian_metro = self.search_read([], ['id', 'rules_id', 'profession_kind', 'url'])
        for xian in xian_metro:
            xian['profession_kind'] =  xian['profession_kind'][1]

        return xian_metro

    def get_day_plan_publish_action(self):
        #  规章制度可见规则 admin 可见全部 站务一二分账号分别可见站务一二分部， 线路下面人员可见相关线路规章
        if self.env.user.id == 1:
            domain = []
        elif self.user_has_groups('base.group_system'):

            if self.env.user.name == '客运一部':
                parent_department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('name', '=','客运一部')])
            else:
                # 客运二部账号
                parent_department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('name', '=', '客运二部')])

            child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', parent_department.departmentId)]).ids
            domain = [('line_id', 'in', child_department_ids)]

        else:
            # 根据人物属性获取domain
            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments
            line_ids = []
            for department_id in department_ids:
                if department_id.department_hierarchy == 2:
                    line_ids.append(department_id.id)

                elif department_id.department_hierarchy == 3:
                    id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId', '=', department_id.parentid)]).id

                    line_ids.append(id)


            domain = [('line_id', 'in', list(set(line_ids)))]

        view_form = self.env.ref('funenc_xa_station.add_operation_tree').id

        return {
            'name': '规章制度',
            'type': 'ir.actions.act_window',
            'domain':domain,
            "views": [[view_form, "tree"]],
            'res_model': 'xian_metro.xian_metro',
            'context': self.env.context,
        }

