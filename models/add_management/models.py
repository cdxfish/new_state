# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import urllib
import base64
import os


class xian_metro(models.Model):
    _name = 'xian_metro.xian_metro'
    # _inherit = 'fuenc_station.station_base'
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='线路')
    site_id = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department', 'xian_metro_site_id_rel','xian_metro_id','site_id',string='站点')
    profession_kind = fields.Many2one('xian_metro.professional', string='专业分类')
    rank_kind = fields.Many2one('add_class.add_class', string='级别分类')
    rules_id = fields.Char(string='规章编号',_sql_constraints = [ ('check_uniq_cph', 'unique(rules_id)', '编号已经存在！')])
    rules_name = fields.Char(string='规章名称')
    # load_line = fields.Selection([('one', '一号线'), ('two', '二号线'), ('three', '三号线')], string='线路', default='one')
    # station_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='站点')
    details = fields.Binary(string='内容')
    file_name = fields.Char(string="File Name")
    operation_peison = fields.Char(string='操作人',default=lambda self: self.default_person_id())
    operation_time = fields.Datetime(string='操作时间', default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    url = fields.Char(string='url')
    release_time = fields.Date(string='发布实施日期')
    rule_regulations_browse = fields.Selection([('one','内容显示'),('zero','内容不显示')],default='zero')

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
        file_binary = params['details']
        file = os.path.splitext(params.get('file_name'))
        filename,type = file
        if type != '.pdf':
            raise ValidationError('上传的文件需要时pdf文件，请重新改选择')
        file_name = params.get('file_name', self.file_name)
        if file_binary:
            url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
                'funenc_xa_station', file_name, base64.b64decode(file_binary))
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

