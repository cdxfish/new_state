# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api
import odoo.exceptions as msg

KEY_STATES = [
    ('normal', '正常'),
    ('borrow', '借出'),
    ('fixed', '锁定'),
    ('destroyed', '报废'),
    ('error', '破损'),
]


class KeyDetail(models.Model):
    _name = 'funenc.xa.station.key.detail'
    _rec_name = 'key_no'
    _description = '钥匙详情'
    _inherit = 'fuenc_station.station_base'

    name = fields.Char(string='钥匙名称', required=True)
    remark = fields.Text(string='操作说明')
    # line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='选择线路', required=True)
    # ascription_site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='归属站点', required=True)
    key_type_id = fields.Many2one('funenc.xa.station.key.type', string='钥匙类型', required=True)
    key_no = fields.Text(string='钥匙编号', required=True)
    only_key_no = fields.Char(string='钥匙唯一编号')  # 自动生成 线路id+站点id+钥匙编号   用来验证钥匙是否重复
    key_position = fields.Char(string='对应位置')
    state_now = fields.Selection(selection=KEY_STATES, string='当前状态', default='normal')
    is_main = fields.Selection(selection=[('yes', '主'), ('no', '备')], string='主备情况', default='yes')
    is_borrow = fields.Integer(string='是否在借用', default=2)

    # borrow_user_id = fields.Many2one('res.users',string='借用人')

    @api.model
    def create(self, vals):
        line_id = vals.get('line_id')
        site_id = vals.get('site_id')
        is_main = vals.get('is_main')
        key_type_id = vals.get('key_type_id')
        key_position = vals.get('key_position') or ''
        only_key_no = 'line_site_'.format(line_id,site_id)
        name = vals.get('name')
        key_nos = vals.get('key_no', '').split('\n')
        new_key_nos = []
        k = -1
        [new_key_nos.append(key_no) for key_no in key_nos if key_no not in new_key_nos]  # 去重并保持排序不变
        for i, new_key_no in enumerate(new_key_nos):
            existence = self.search([('only_key_no', '=', only_key_no + new_key_no)])

            if not existence:
                if k == -1:
                    k = i
                else:
                    inset_sql = "insert into  funenc_xa_station_key_detail(line_id,site_id,key_no,only_key_no,name," \
                                "is_borrow,is_main,state_now,key_type_id,key_position) " \
                                "values({},{},{},'{}','{}',{},'{}','{}',{},'{}')".format(line_id, site_id, new_key_no,
                                                                                    (only_key_no + new_key_no),
                                                                                    name, 2, is_main, 'normal',
                                                                                    key_type_id,key_position)
                    self.env.cr.execute(inset_sql)
        if k == -1:
            raise msg.Warning('此编号已存在')

        vals['key_no'] = new_key_nos[k]
        vals['only_key_no'] = only_key_no + new_key_nos[k]

        return super(KeyDetail, self).create(vals)

    @api.multi
    def write(self, vals):
        # if self.self.env.context.get('state_now'):
        # 	vals['state_now'] = self.env.context.get('state_now')
        return super(KeyDetail, self).write(vals)

    @api.model
    def get_data_test(self):
        print('ok')

    def key_detail_edit(self):
        return {
            'name': '钥匙详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc.xa.station.key.detail',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def key_detail_delete(self):
        self.env['funenc.xa.station.key.detail'].search([('id', '=', self.id)]).unlink()

    # 启用
    @api.multi
    def key_detail_state_change_start(self):
        context = {}
        context['state_now'] = 'normal'
        # view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_borrow_record_list').id
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_key_detail_operate_remark_form_start').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc.xa.station.key.detail",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': context,
            'value': {'state_now': 'normal'}
        }

    @api.multi
    def key_detail_state_change_fixed(self):
        context = {}
        context['search_default_state_now'] = 'fixed'
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_key_detail_operate_remark_form_fixed').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc.xa.station.key.detail",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': context
        }

    @api.multi
    def key_detail_state_change_destroyed(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_key_detail_operate_remark_form_destroyed').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc.xa.station.key.detail",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': {'state_now': 'destroyed'},
            'value': {'state_now': 'destroyed'}
        }

    @api.multi
    def key_detail_state_change_recovery(self):
        context = {}
        context['state_now'] = 'normal'
        view_form = self.env.ref(
            'funenc_xa_station.funenc_xa_station_key_detail_operate_remark_form_recovery').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc.xa.station.key.detail",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': context
        }

    @api.multi
    def key_detail_state_change_error(self):
        context = {}
        context['state_now'] = 'error'
        view_form = self.env.ref(
            'funenc_xa_station.funenc_xa_station_key_detail_operate_remark_form_error').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc.xa.station.key.detail",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': context
        }

    def test_btn_start(self):
        values = {
            'key_no': self.key_no,
            'type': self.key_type_id.name,
            'station': self.site.id,
            'name': self.name,
            'position': self.key_position,
            'is_main': self.is_main,
            'operate_type': 'start',
            'operate_member': self._uid,
            'remarks': self.remark,
        }
        self.state_now = self.env.context.get('state_now', 'normal')
        self.env['funenc.xa.station.change.record'].create(values)

    def test_btn_fixed(self):
        values = {
            'key_no': self.key_no,
            'type': self.key_type_id.name,
            'station': self.site.id,
            'name': self.name,
            'position': self.key_position,
            'is_main': self.is_main,
            'operate_type': 'fixed',
            'operate_member': self._uid,
            'remarks': self.remark,
        }
        self.state_now = self.env.context.get('state_now', 'normal')
        self.env['funenc.xa.station.change.record'].create(values)

    def test_btn_error(self):
        values = {
            'key_no': self.key_no,
            'type': self.key_type_id.name,
            'station': self.site_id.id,
            'name': self.name,
            'position': self.key_position,
            'is_main': self.is_main,
            'operate_type': 'error',
            'operate_member': self._uid,
            'remarks': self.remark,
        }
        self.state_now = self.env.context.get('state_now', 'normal')
        self.env['funenc.xa.station.change.record'].create(values)

    def test_btn_destroyed(self):
        values = {
            'key_no': self.key_no,
            'type': self.key_type_id.name,
            'station': self.site_id.id,
            'name': self.name,
            'position': self.key_position,
            'is_main': self.is_main,
            'operate_type': 'start',
            'operate_member': self._uid,
            'remarks': self.remark,
        }
        self.state_now = self.env.context.get('state_now', 'normal')
        self.env['funenc.xa.station.change.record'].create(values)

    def test_btn_recovery(self):
        values = {
            'key_no': self.key_no,
            'type': self.key_type_id.name,
            'station': self.site_id.id,
            'name': self.name,
            'position': self.key_position,
            'is_main': self.is_main,
            'operate_type': 'recovery',
            'operate_member': self._uid,
            'remarks': self.remark,
        }
        self.state_now = self.env.context.get('state_now', 'normal')
        self.env['funenc.xa.station.change.record'].create(values)

    def key_detail_save(self):

        # values = {
        # 	'key_no': self.key_no,
        # 	'key_type_id': self.key_type_id.id,
        # 	'ascription_site_id': self.ascription_site_id.id,
        # 	'name': self.name,
        # 	'key_position': self.key_position,
        # 	'is_main': self.is_main,
        # 	'remarks': self.remark,
        # 	'line_id': self.line_id.id
        # }
        #
        # self.create(values)

        return {
            'name': '钥匙',
            "type": "ir.actions.client",
            "tag": "key_statistic",
            "target": "current",

        }
