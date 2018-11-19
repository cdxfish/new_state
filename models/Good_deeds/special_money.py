# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
import datetime
from ..get_domain import get_domain
import base64

key = [('one_audit','待初审'),
       ('two_audit','待复审'),
       ('through','已通过'),
       ('rejected','已驳回')]


class SpecialMoney(models.Model):
    _name = 'funenc_xa_station.special_money'
    _inherit = 'fuenc_station.station_base'

    def _default_associated(self):
        if self._context.get('active_id', False):
            return self._context['active_id']

    open_time = fields.Datetime(string='发生时间')
    open_site = fields.Char(string='发生地点')
    event_type = fields.Selection([("deal","事务处理 "),('money','非及时退款')],string='事件类型')
    event_details = fields.Text(string='事件详情',required=True)
    survey_situation = fields.Text(string='调查情况')
    involving_money = fields.Integer(string='涉及金额',required=True)
    passengers_name = fields.Char(string='乘客姓名')
    passengers_phone = fields.Char(string='乘客电话')
    passengers_ID = fields.Char(string='乘客身份证')
    deal_person = fields.Char(string='处理人员')
    webmaster = fields.Char(string='站长')
    deputy_director = fields.Char(string='分部主任')
    main_director = fields.Char(string='部门领导')
    write_time = fields.Datetime(string='填报时间',default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    write_person = fields.Char(string='填报人',default=lambda self: self.default_person_id())
    audit_flow = fields.Char(string='审核流程')
    apply_why = fields.Text(string='申请原因',required=True)
    deal_result = fields.Selection(key,string='处理结果',default='one_audit')
    # load_file_test = fields.Many2many('ir.attachment','good_special_ir_attachment_rel',
    #                                      'attachment_id','meeting_dateils_id', string='图片上传')
    load_file_test = fields.Binary(string='身份证照片')
    file_name = fields.Char(str='File Name')
    deal_list_file = fields.Binary(string='')
    special_attrchment_deal = fields.One2many('video_voice_model','special_money_act',string='附件处理结果')
    url = fields.Char(string='url')

    @api.model
    def create(self, params):
        file_binary = params['load_file_test']
        file_name = params.get('file_name', self.file_name)
        if file_binary:
            url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
                'funenc_xa_station', file_name, base64.b64decode(file_binary))
            params['url'] = url
            params['file_name'] = file_name
        return super(SpecialMoney, self).create(params)

    def image_browse_act(self):
        url = self.url
        if url:
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }



    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name

    # 创建一条新的记录
    def new_increase_record(self):
        view_form = self.env.ref('funenc_xa_station.special_money_form').id
        return {
            'name': '特殊赔偿金',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_money',
            'context': self.env.context,
            'target':'new',
        }

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.special_money_tree').id
        return {
            'name': '特殊赔偿金',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.special_money',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                        [
                            {'title': '好人好事',
                            'action':  'funenc_xa_station.good_deeds_act',
                            'group':'funenc_xa_station.table_good_actions'
                            },
                            {
                                'title': '客伤',
                                'action2' : 'funenc_xa_station.guests_hurt_act',
                                'group' : 'funenc_xa_station.table_people_wound'
                                },
                            {
                                'title': '乘客意见箱',
                                'action2':  'funenc_xa_station.suggestion_box_act',
                                'group' : 'funenc_xa_station.table_people_message'
                                },
                           {
                                'title': '特殊赔偿金',
                                'action2':  'funenc_xa_station.special_money_act',
                                'group' : 'funenc_xa_station.table_special_compensation'
                                },
                        ]
                    }''',
            'context': self.env.context,
        }

    def special_details_action(self):
        view_form = self.env.ref('funenc_xa_station.special_money_details').id
        return {
            'name': '特殊赔偿金详情',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_money',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
        }

    def test_btn_two_audit(self):
        values = {
            'deal_result': self.deal_result,
        }
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta

        primary_audit = '初审' + '    ' + str(self.env.user.dingtalk_user.name) + \
                        '(' + str(now_time) + ')'
        self.deal_result = self.env.context.get('deal_result', 'two_audit')
        self.audit_flow = self.env.context.get('audit_flow', primary_audit)
        self.env['funenc_xa_station.special_money'].write(values)

    def test_btn_through(self):
        values = {
            'deal_result': self.deal_result,
        }
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        now_time = d + delta

        primary_audit = self.audit_flow + '复审' + '    ' + str(self.env.user.dingtalk_user.name) + \
                        '(' + str(now_time) + ')'
        self.deal_result = self.env.context.get('deal_result', 'through')
        self.audit_flow = self.env.context.get('audit_flow', primary_audit)
        self.env['funenc_xa_station.special_money'].write(values)

    def good_rejected(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'rejected')
        self.env['funenc_xa_station.special_money'].write(values)

    def test_btn_rejected(self):
        values = {
            'deal_result': self.deal_result,
        }
        self.deal_result = self.env.context.get('deal_result', 'one_audit')
        self.env['funenc_xa_station.special_money'].write(values)

    def good_delete(self):
        self.env['funenc_xa_station.special_money'].search([('id', '=', self.id)]).unlink()

    def onchange_button_action(self):
        view_form = self.env.ref('funenc_xa_station.special_money_form').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.special_money',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def print_refund_form(self):
        id_id = self.id
        return {
            "type": "ir.actions.act_url",
            'res_id': self.id,
            "url": '/funenc_xa_station/special_money_word?id=%s'%(id_id),
            "target": "new",
        }

    # 上传附件文件
    def onchange_typr_action(self):
        view_form = self.env.ref('funenc_xa_station.video_voice_form').id
        return {
            'name': '附件',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'video_voice_model',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

