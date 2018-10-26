# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import json

from ..get_domain import get_domain

class BreakSubmit(models.Model):
    _name = 'funenc_xa_station.break_submit'

    _inherit = 'fuenc_station.station_base'

    break_describe = fields.Char(string='故障描述')
    local_image = fields.Binary(string='现场图片')
    equipment_name = fields.Char(string='设备名称')
    equipment_number = fields.Char(string='设备编码`')
    equipment_post = fields.Char(string='设备位置')
    break_type = fields.Many2one('funenc_xa_staion.break_type_increase', string='故障类型')
    submit_time = fields.Datetime(string='提报时间')
    deal_situation = fields.Selection([('one', '提交'), ('zero', '未处理')], string='处理情况')
    deal_results = fields.Char(string='处理结果')
    deal_time = fields.Datetime(string='处理时间')
    load_file_test = fields.Many2many('ir.attachment', 'funenc_xa_station_break_dateils_ir_attachment_rel',
                                      'attachment_id', 'meeting_dateils_id', string='图片上传')
    url = fields.Char(string='七牛路径')  # app 上传路径 自己转换

    def break_delete_action(self):
        self.env['funenc_xa_station.break_submit'].search([('id', '=', self.id)]).unlink()

    @api.model
    def get_break_submit_list(self):
        if self.env.user.id == 1:
            data = self.search_read([], ['id', 'break_describe', 'break_type', 'submit_time', 'deal_results'])
        else:
            ding_user = self.env.user.dingtalk_user
            department = ding_user.departments[0]
            if department.department_hierarchy == 1:
                data = self.search_read([], ['id', 'break_describe', 'break_type', 'submit_time', 'deal_results'])
            elif department.department_hierarchy == 2:
                ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', department.departmentId)]).ids
                data = self.search_read([('site_id', 'in', ids)],
                                        ['id', 'break_describe', 'break_type', 'submit_time', 'deal_results'])
            else:
                data = self.search_read([('site_id', '=', department.id)],
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
            else:
                data = []

        except Exception:
            return []
        return data

    @api.model
    def save_break_submit(self, vals):

        try:
            self.create(vals)

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
