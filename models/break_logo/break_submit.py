# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import json
from datetime import datetime

from ..get_domain import get_domain
from ..python_util import get_add_8th_str_time
from ast import literal_eval

class BreakSubmit(models.Model):
    _name = 'funenc_xa_station.break_submit'

    _inherit = 'fuenc_station.station_base'

    break_describe = fields.Char(string='故障描述')
    local_image = fields.Binary(string='现场图片')
    equipment_name = fields.Char(string='设备名称')
    equipment_number = fields.Char(string='设备编码')
    equipment_post = fields.Char(string='设备位置')
    break_type = fields.Many2one('funenc_xa_staion.break_type_increase', string='故障类型')
    submit_time = fields.Datetime(string='提报时间')
    deal_situation = fields.Selection([('one', '已处理'), ('zero', '未处理')], string='处理情况',default='zero')
    deal_results = fields.Char(string='处理结果')
    deal_time = fields.Datetime(string='处理时间')
    load_file_test_1 = fields.One2many('video_voice_model','break_submit_image',string='图片')
    url = fields.Char(string='七牛路径')  # app 上传路径 自己转换
    browse_image_invisible = fields.Selection([('one', '有图片'), ('zero', '没有图片')], string='显示还是隐藏图片', default='zero')

    #在创建的时候改变分数的正负数
    @api.model
    def create(self, vals):
        # if vals['load_file_test'][0][2]:
        #     vals['browse_image_invisible'] = 'one'
        vals['submit_time'] = datetime.now()

        return super(BreakSubmit, self).create(vals)

    # 创建一条新的记录
    def new_increase_record(self):
        view_form = self.env.ref('funenc_xa_station.break_submit_form').id
        return {
            'name': '故障列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.break_submit',
            'context': self.env.context,
            'target':'new',
        }

    # 处理操作
    def deal_button_action(self):

        self.write({'deal_situation':'one'})
        view_form = self.env.ref('funenc_xa_station.break_submit_deal_form').id
        return {
            'name': '故障列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.break_submit',
            'context': self.env.context,
            'res_id':self.id,
            'target':'new',
        }

    # 修改当前的一条记录
    def onchange_record_button_act(self):
        view_form = self.env.ref('funenc_xa_station.break_submit_form').id
        return {
            'name': '故障列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.break_submit',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id':self.id,
            'target':'new',
        }

    # 编辑当前的一条记录
    def edit_button_subit_act(self):
        view_form = self.env.ref('funenc_xa_station.break_submit_edit_form').id
        return {
            'name': '故障列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.break_submit',
            'flags': {'initial_mode': 'edit'},
            'context': self.env.context,
            'res_id':self.id,
            'target':'new',
        }


    # 删除当前的一条记录
    def break_delete_action(self):
        self.env['funenc_xa_station.break_submit'].search([('id', '=', self.id)]).unlink()

    @get_domain
    @api.model
    def get_break_submit_list(self,domain):
        if self.env.user.id == 1:
            data = self.search_read([], ['id', 'break_describe', 'break_type', 'submit_time', 'deal_results'])
        else:
            data = self.search_read(domain,
                                    ['id', 'break_describe', 'break_type', 'submit_time', 'deal_results'])
        for obj in data:
            if obj['break_type']:
                obj['break_type'] = obj['break_type'][1]
            else:
                obj['break_type'] = ''
            if obj.get('deal_results'):
                obj['deal_results'] = '已处理'
            else:
                obj['deal_results'] = '未处理'
            if obj.get('submit_time'):
                obj['submit_time'] = get_add_8th_str_time(obj.get('submit_time'))

        return data

    @api.model
    def get_break_submit_by_id(self, id):
        try:
            sel_data = self.search_read([('id', '=', int(id))
                                         ], ['break_describe', 'url', 'equipment_name', 'equipment_number', 'line_id',
                                             'site_id', 'submit_time', 'deal_results', 'deal_time', 'break_type'])
            if sel_data:
                data = sel_data[0]
                data['position'] = data['line_id'][1] + data['site_id'][1]
                if data['url']:
                    data['url'] = json.loads(data['url'])
                else:
                    data['url'] = []
                if data.get('break_type'):
                    data['break_type'] = data['break_type'][1]
                else:
                    data['break_type'] = ''
                if data.get('deal_results'):

                    data['deal_results'] = '已处理'
                else:
                    data['deal_results'] = '未处理'
                if data.get('submit_time'):
                    data['submit_time'] = get_add_8th_str_time(data.get('submit_time'))

            else:
                data = []

        except Exception:
            return []
        return data

    @api.model
    def save_break_submit(self, vals):

        try:
            obj = self.create(vals)
            if vals.get('url'):
                imgs = literal_eval(vals.get('url'))
                for im in imgs:
                    self.env['video_voice_model'].create({
                        'break_submit_image':obj.id,
                        'url':im['url']
                    })

        except Exception:

            return  False

        return True

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.break_submit_tree').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.break_submit',
            'context': self.env.context,
        }

    #浏览当前记录的图片
    def browse_image_button_act(self):
        view_form = self.env.ref('funenc_xa_station.browse_image_button_submit_act').id
        return {
            'name': '查看图片',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.break_submit',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }
