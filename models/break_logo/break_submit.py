# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class BreakSubmit(models.Model):
    _name = 'funenc_xa_station.break_submit'

    _inherit = 'fuenc_station.station_base'

    break_describe = fields.Char(string='故障描述')
    local_image = fields.Binary(string='现场图片')
    equipment_name = fields.Char(string='设备名称')
    equipment_number = fields.Char(string='设备编码')
    equipment_post = fields.Char(string='设备位置')
    break_type = fields.Many2one('funenc_xa_staion.break_type_increase',string='故障类型')
    submit_time = fields.Datetime(string='提报时间')
    deal_situation = fields.Selection([('one','提交'),('zero','未处理')],string='处理情况')
    deal_results = fields.Char(string='处理结果')
    deal_time = fields.Datetime(string='处理时间')
    load_file_test = fields.Many2many('ir.attachment', 'funenc_xa_station_break_dateils_ir_attachment_rel',
                                     'attachment_id', 'meeting_dateils_id', string='图片上传')

    def break_delete_action(self):
        self.env['funenc_xa_station.break_submit'].search([('id','=',self.id)]).unlink()