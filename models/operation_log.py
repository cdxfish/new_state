# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class operation_log(models.Model):
    _name = 'funenc_xa_station.operation_log'
    _description = u'操作日志'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='名称')

    @api.model
    def get_log_ids(self, **kw):
        '''
        获取日志记录ids
        :param message_id: 创建message_id日志的id
        :return: 日志ids
        '''
        try:
            message_id = kw.get('message_id')

            mail_message = self.env['mail.message'].browse(message_id)

            return [message_id] + mail_message.child_ids.ids
        except:
            return []


class InheritMailMessage(models.Model):
    _inherit = 'mail.message'

    def detail(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_operation_log_form').id
        operation_log = self.env['funenc_xa_station.operation_log'].search([])
        if operation_log:
            res_id = operation_log[0].id
        else:
            res_id = self.env['funenc_xa_station.operation_log'].create(
                {'name': '操作人日志'}
            ).id
        return {
            'name': '日志查看',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.operation_log',
            'context': self.env.context,
            'target': 'current',
            'res_id': res_id
        }

    @api.multi
    def unlink(self):
        # lens = len(self)
        # this = self[lens - 1]  # 日志为创建的记录
        # model = this.model
        # del_ir_model = self.env['ir.model'].search([('model', '=', model)])
        #
        # self.sudo(this.create_uid).create(
        #     {
        #         'body': '删除模型({})'.format(del_ir_model.name),
        #         'record_name': this.record_name
        #     }
        # )

        return super(InheritMailMessage, self).unlink()
