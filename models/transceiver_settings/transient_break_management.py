# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class TransientBreakManagement(models.Model):
    _name = 'funenc_xa_station.transient_break_management'
    # _inherit = 'fuenc_station.station_base'

    transceiver_type = fields.Char(string='工器具类型')
    transceive_name = fields.Char(string='工器具名称')
    transceive_number = fields.Char(string='工器具编号',_sql_constraints = [ ('check_uniq_cph', 'unique(transceive_number)', '编号已经存在！')])
    line_id = fields.Char(string='线路')
    site_id = fields.Char(string='站点')
    post = fields.Char(string='位置')
    apply_time = fields.Datetime(string='申报时间')
    break_describe = fields.Char(string='故障描述')
    load_file_test = fields.Many2many('ir.attachment','good_break_transient_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')
    state = fields.Selection([('one','已修复'),('zero','未处理')],string='状态',default='zero')
    repair_time = fields.Datetime(string='修复时间')
    repair_manufacturer = fields.Char(string='修复厂家')
    many2many_image = fields.Many2many('ir.attachment','good_break_ir_before_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')
    id_id = fields.Char(string='id引用') #用来接收工器具使用列表的ID

    #修复
    def repair_image(self):
        self.env['funenc_xa_station.transceiver_settings'].search([('id','=',int(self.id_id))]).write({
          'state':'one'
        })
        self.write({'state': 'one'})
        view_form = self.env.ref('funenc_xa_station.transient_break_management_form').id
        return {
            'name': '工器具使用列表',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transient_break_management',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    #修改
    def change_onchange(self):
        view_form = self.env.ref('funenc_xa_station.transient_break_management_form_button').id
        return {
            'name': '工器具故障',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transient_break_management',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    #删除
    def management_delete(self):
        self.env['funenc_xa_station.transient_break_management'].search([('id','=',self.id)]).unlink()

    #查看故障前的图片
    def before_action(self):
        view_form = self.env.ref('funenc_xa_station.transceiver_settings_before_button').id
        return {
            'name': '工器具故障',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transceiver_settings',
            'res_id':int(self.id_id),
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }

    #查看修复后的图片
    def after_action(self):
        view_form = self.env.ref('funenc_xa_station.transient_break_management_before_image').id
        return {
            'name': '工器具故障',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.transient_break_management',
            'res_id':self.id,
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }




