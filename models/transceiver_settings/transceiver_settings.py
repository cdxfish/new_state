# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
from odoo.exceptions import ValidationError

class TransceiverSettings(models.Model):
    _name = 'funenc_xa_station.transceiver_settings'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'transient_type'

    transient_type = fields.Many2one('funenc_xa_station.consumables_type',string='工器具类型', track_visibility='onchange')
    transient_name = fields.Char(string='工器具名称' , track_visibility='onchange')
    transient_number = fields.Char(string='工器具编号', track_visibility='onchange')
    post = fields.Char(string='位置', track_visibility='onchange')
    state = fields.Selection([('one','正常'),('zero','故障')],string='状态',default='one')
    break_descrip = fields.Text(string='故障描述', track_visibility='onchange')
    load_file_test = fields.Many2many('ir.attachment', 'funenc_xa_transceiver_attachment_rel',
                                     'attachment_id', 'meeting_dateils_id', string='图片上传', track_visibility='onchange')

    @api.model
    def create(self, vals):
        number = vals.get('transient_number')
        record = self.env['funenc_xa_station.transceiver_settings'].search([('transient_number','=',number)])
        if record:
            raise ValidationError('当前站点已经存在改工器具编号，请从新输入')
        return super(TransceiverSettings,self).create(vals)



    # 用来获取工器具类型的值和id
    # def get_value(self):
    #     global lis
    #     lis = []
    #     res_id = self.transient_type.consumables_type
    #     lis.append(res_id)
    #     parent_id = self.transient_type.prent_id.id
    #     return self.get_parent(res_id,parent_id)

    # #用来获取工器具类型所有的值和id
    # def get_parent(self,res_id,parent_id):
    #     record = self.env['funenc_xa_station.consumables_type'].search_read(
    #       [('id', '=', parent_id)], ['consumables_type', 'prent_id'])
    #     if record[0]['consumables_type']:
    #       lis.append(record[0]['consumables_type'])
    #     if record[0]['prent_id']:
    #         res_id = record[0]['consumables_type']
    #         parent_id = record[0]['prent_id'][0]
    #         return self.get_parent(res_id,parent_id)
    #     else:
    #         print(lis)
    #         lis.reverse()
    #         liss = lis
    #         print(liss)
    #         print('/'.join(liss))
    #         self.transient_name = '/'.join(liss)









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