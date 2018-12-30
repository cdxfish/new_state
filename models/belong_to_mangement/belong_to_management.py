# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from .. get_domain import get_domain
from ast import literal_eval
from ..python_util import get_add_8th_str_time
import datetime
class BelongToManagement(models.Model):
    _name = 'funenc_xa_station.belong_to_management'
    _inherit = 'fuenc_station.station_base'

    post_check = fields.Selection([('guard', '保安'), ('check', '安检'), ('clean', '保洁')], string='岗位检查')
    check_time = fields.Datetime(string='检测时间')
    check_state = fields.Text(string='检测情况')
    find_problem = fields.Text(string='发现问题')
    reference_according = fields.Char(string='参考依据')
    local_image = fields.Binary(string='现场照片')
    check_score = fields.Float(string='考核分值',)
    note = fields.Char(string='备注')
    # write_person = fields.Char(string='填写人')
    write_person = fields.Char(string='填报人',
                               default=lambda self: self.default_name_id())
    job_number = fields.Char(string='工号', default=lambda self: self.default_job_number_id())
    change_state = fields.Selection([('add', '加'), ('reduce', '减')], default='reduce')
    summary_score = fields.Integer(string='总分值', default=100)
    check_count = fields.Integer(string='检查次数', default=1)
    load_file_test = fields.One2many('video_voice_model','belong_management_imange',string='图片上传')
    imgs = fields.Char('照片路径')  # 存的字典  自己转
    browse_image_invisible = fields.Selection([('one','有图片'),('zero','没有图片')],string='显示还是隐藏图片',default='zero')

    #在创建的时候改变分数的正负数
    @api.model
    def create(self, vals):
        if vals.get('change_state') == 'add':
            vals['check_score'] = abs(vals.get('check_score'))
        elif vals.get('change_state') == 'reduce':
            vals['check_score'] = -abs(vals.get('check_score'))
            
        if vals.get('load_file_test') or vals.get('imgs') :

                vals['browse_image_invisible'] = 'one'
        create_vals = super(BelongToManagement, self).create(vals)
        if create_vals.imgs:
            imgs = literal_eval(create_vals.imgs)
            for img in imgs:
                self.env['video_voice_model'].create({
                    'belong_management_imange':create_vals.id,
                    'url': img['url']
                })
        return create_vals

    def create_button(self):
        print(self)

    @get_domain
    @api.model
    def get_day_plan_publish_action(self,domain):
        view_form = self.env.ref('funenc_xa_station.belong_to_management_tree').id
        return {
            'name': '属地管理属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_form, "tree"]],
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
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

    #创建新记录
    @api.model
    def create_belong_to_action(self):
        # view_form = self.env.ref('funenc_xa_station.belong_to_management_form').id
        return {
            'name': '属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            # "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
            'target':'new',
        }

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

    @get_domain
    @api.model
    def get_belong_to_management(self,domain):

        temps = self.search_read(domain,
                                     ['id', 'summary_score', 'note', 'post_check', 'check_time'])
        for temp in temps:
            if temp.get('post_check') == 'guard':
                temp['post_check'] = '保安'
            elif temp.get('post_check') == 'check':
                temp['post_check'] = '安检'
            elif temp.get('post_check') == 'clean':
                temp['post_check'] = '保洁'
            else:
                temp['post_check'] = ''
            if temp.get('check_time'):
                temp['check_time'] = get_add_8th_str_time(temp.get('check_time'))
            else:
                temp['check_time'] = ''

        return temps

    @api.model
    def get_belong_to_management_by_id(self, id):
        select_id = int(id) or -1
        belong_to_management = self.search_read([('id', '=', select_id)],
                                                ['find_problem', 'check_state', 'note', 'post_check',
                                                 'reference_according','imgs',
                                                 'summary_score', 'local_image', 'check_time', 'line_id', 'site_id'])[0]
        if belong_to_management.get('line_id') and belong_to_management.get('site_id'):
            belong_to_management['devicePosition'] = belong_to_management.get('line_id')[1] + '-' + \
                                                     belong_to_management.get('site_id')[1]
        else:
            belong_to_management['devicePosition'] = ''
        temp = belong_to_management.get('post_check')
        if temp:
            if temp == 'guard':
                belong_to_management['post_check'] = '保安'
            elif temp == 'check':
                belong_to_management['post_check'] = '安检'
            elif temp == 'clean':
                belong_to_management['post_check'] = '保洁'
            else:
                belong_to_management['post_check'] = ''

        if belong_to_management.get('check_time'):
            belong_to_management['check_time'] = get_add_8th_str_time(belong_to_management.get('check_time'))
        else:
            belong_to_management['check_time'] = ''

        return belong_to_management

    @api.model
    def save_belong_to_management(self, vals):

        try:
            vals['check_time'] = datetime.datetime.now()
            vals['summary_score'] = 100 + vals.get('check_score',0)
            self.create(vals)
        except Exception:
            raise False
        return True

    #查看现场图片
    def browse_image_button_act(self):
        view_form = self.env.ref('funenc_xa_station.browse_iamge_form').id
        return {
            'name': '属地管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }


