# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime

class TransceiverSettings(models.Model):
    _name = 'funenc_xa_station.transceiver_settings'
    _inherit = 'fuenc_station.station_base'

    transient_type = fields.Many2one('funenc_xa_station.consumables_type',string='工器具类型')
    transient_name = fields.Char(string='工器具名称' )
    transient_number = fields.Char(string='工器具编号',_sql_constraints = [ ('check_uniq_cph', 'unique(transient_number)', '编号已经存在！')])
    post = fields.Char(string='位置')
    state = fields.Selection([('one','正常'),('zero','故障')],string='状态',default='one')
    break_descrip = fields.Text(string='故障描述')
    load_file_test = fields.Many2many('ir.attachment', 'funenc_xa_transceiver_attachment_rel',
                                     'attachment_id', 'meeting_dateils_id', string='图片上传')


    # @api.model
    # def create(self, vals):
    #     re_id = vals.get('transient_type')
    #     lis = []
    #     record = self.env['funenc_xa_station.consumables_type'].search_read(
    #         [('id', '=', re_id)], ['consumables_type', 'prent_id'])
    #     if record[0]['consumables_type']:
    #         lis.append(record[0]['consumables_type'])
    #         re_id = record[0]['prent_id']
    #         return self.create()
    #     else:
    #         print(lis)


    # 创建一条新的记录
    def new_increase_record(self):
        view_form = self.env.ref('funenc_xa_station.transceiver_settings_form').id
        return {
            'name': '新增工器具',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transceiver_settings',
            'context': self.env.context,
            'target':'new',
        }

    #报修按钮
    def warranty_action(self):
        dic={
            'id_id':self.id,
            'transceiver_type':self.transient_type.id,
            'transceive_name':self.transient_name,
            'transceive_number':self.transient_number,
            'line_id':self.line_id.id,
            'site_id':self.site_id.id,
            'post':self.post,
            'apply_time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'break_describe':self.break_descrip
        }
        self.write({'state':'zero'})
        self.env['funenc_xa_station.transient_break_management'].sudo().create(dic)
        view_form = self.env.ref('funenc_xa_station.transceiver_settings_form_warranty').id
        return {
            'name': '工器具使用列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transceiver_settings',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    #修改按钮
    def professional_edit(self):
        view_form = self.env.ref('funenc_xa_station.transceiver_settings_form_warranty').id
        return {
            'name': '工器具使用列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transceiver_settings',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    #删除记录
    def management_delete(self):
        self.env['funenc_xa_station.transceiver_settings'].search([('id','=',self.id)]).unlink()