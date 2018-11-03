# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api
import datetime
import odoo.exceptions as msg


class BorrowRecord(models.Model):
    _name = 'funenc.xa.station.borrow.record'
    _inherit = 'fuenc_station.station_base'

    key_no = fields.Many2one('funenc.xa.station.key.detail',string='钥匙编号')
    # line = fields.Many2one(related='key_no.line_id',string='线路')
    type = fields.Many2one('funenc.xa.station.key.type', string='钥匙类型',related='key_no.key_type_id')
    # station = fields.Many2one(related='key_no.site_id',string='归属站点')
    name = fields.Char(related='key_no.name',string='钥匙名称')
    position = fields.Char(related='key_no.key_position',string='对应位置')
    borrow_time = fields.Datetime(string='借用时间')
    borrow_operate_member = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='借用操作人')
    borrow_member = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='借用人')
    return_time = fields.Datetime(string='归还时间')
    return_operate_member = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='归还操作人')
    return_member = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',
                                     string='归还人')
    state = fields.Selection(selection=[('yes','借出'),('no','归还')],default='yes',string='状态')
    del_ids = fields.Integer(string='删除id')


    @api.model
    def create(self, vals):
        if self.env.user.id == 1:
            return_operate_member = 1
        else:
            return_operate_member = self.env.user.dingtalk_user[0].id
        if vals.get('key_no') and ( not vals.get('return_member') ):

            key_no = vals.get('key_no')
            key = self.env['funenc.xa.station.key.detail'].search([('id','=',key_no)])
            if key.is_borrow == 1:
                raise msg.Warning('钥匙正在借用')
            else:
                key.write({'is_borrow':1})
                key.write({'state_now': 'borrow'})

        vals['borrow_time'] = datetime.datetime.now()
        vals['state'] = 'yes'
        vals['borrow_operate_member'] = return_operate_member
        if vals.get('return_member'):
            vals['del_ids']= 1
        return super(BorrowRecord, self).create(vals)

    @api.onchange('key_no')
    def change_key_no(self):
        res = {}
        if not self.key_no:
            return

        borrow_record = self.env['funenc.xa.station.borrow.record'].search(
            [('key_no', '=',self.key_no.key_no), ('state', '=','yes')])
        res['value'] = {'borrow_member': borrow_record.borrow_member.id,
                          'borrow_time':borrow_record.borrow_time
                          }

        return  res

    @api.multi
    def write(self, vals):
        if not self:
            return

        return super(BorrowRecord, self).write(vals)
    def submit(self):
        if self.env.user.id ==1 :
            return_operate_member = 1
        else:
            return_operate_member =self.env.user.dingtalk_user[0].id

        borrow_record = self.env['funenc.xa.station.borrow.record'].search(
            [('key_no', '=',self.key_no.id), ('state', '=','yes'), ('del_ids', '=', False)])

        borrow_record.write({'state': 'no','return_member':self.return_member.id,
                             'return_time':datetime.datetime.now(),
                             'return_operate_member': return_operate_member

                             })
        borrow_record.key_no.write({'is_borrow':2,'state_now': 'normal'})
        self.env['funenc.xa.station.borrow.record'].search([('del_ids', '=', 1)]).unlink()
        return {
            'name': '钥匙',
            "type": "ir.actions.client",
            "tag": "key_statistic",
            "target": "current",

        }

    def _compute_count(self):
        '''
         统计钥匙数量
        :return:
        '''
        pass

        # 创建钥匙
        @api.model
        def create_key(self):
            return {
                'name': '钥匙创建',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'funenc.xa.station.key.detail',
                'context': self.env.context,
                # 'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }

        # 借用钥匙
        @api.model
        def borrow_key(self):
            context = dict(self.env.context)
            view_form = self.env.ref('funenc_xa_station2.borrow_record_form_1').id
            context['borrow_member'] = self.env.user.id
            return {
                'name': '钥匙借用',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc.xa.station.borrow.record',
                'context': context,
                # 'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }

        # 归还钥匙
        @api.model
        def return_key(self):
            context = dict(self.env.context)
            view_form = self.env.ref('funenc_xa_station2.funenc_xa_station_borrow_record_form').id
            return {
                'name': '钥匙归还',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc.xa.station.borrow.record',
                'context': context,
                # 'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }

        # 借用记录
        @api.model
        def borrow_record(self):
            view_tree = self.env.ref('funenc_xa_station2.funenc_xa_station_borrow_record_list').id
            view_form = self.env.ref('funenc_xa_station2.funenc_xa_station_borrow_record_form').id
            return {
                'name': '借用记录',
                "type": "ir.actions.act_window",
                "res_model": "funenc.xa.station.borrow.record",
                "views": [[view_tree, "tree"], [view_form, "form"]],
                # "domain": [()],
            }

    def save(self):

        return {
            'name': '钥匙',
            "type": "ir.actions.client",
            "tag": "key_statistic",
            "target": "current",

        }

