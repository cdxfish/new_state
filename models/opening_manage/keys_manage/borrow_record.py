# -*- coding: utf-8 -*-
# Created by yong at 2018/8/20
from odoo import models, fields, api
import datetime
import odoo.exceptions as msg


class BorrowRecord(models.Model):
    _name = 'funenc.xa.station.borrow.record'

    key_no = fields.Many2one('funenc.xa.station.key.detail',string='钥匙编号')
    line = fields.Char(related='key_no.line_id',string='线路')
    type = fields.Many2one('funenc.xa.station.key.type', string='钥匙类型',related='key_no.key_type_id')
    station = fields.Char(related='key_no.ascription_site_id',string='归属站点')
    name = fields.Char(related='key_no.name',string='钥匙名称')
    position = fields.Char(related='key_no.key_position',string='对应位置')
    borrow_time = fields.Datetime(string='借用时间')
    borrow_operate_member = fields.Many2one('res.users',string='借用操作人')
    borrow_member = fields.Many2one('res.users',
                                     string='借用人')
    return_time = fields.Datetime(string='归还时间')
    return_operate_member = fields.Many2one('res.users',string='归还操作人')
    return_member = fields.Many2one('res.users',
                                     string='归还人')
    state = fields.Selection(selection=[('yes','借出'),('no','归还')],default='yes',string='状态')
    del_ids = fields.Integer(string='删除id')
    @api.model
    def create(self, vals):
        if vals.get('key_no'):
            key_no = vals.get('key_no')
            key = self.env['funenc.xa.station.key.detail'].search([('key_no','=',key_no)])
            if key.is_borrow == 1:
                raise msg.Warning('钥匙正在借用')
            else:
                key.write({'is_borrow':1})

        vals['borrow_time'] = datetime.datetime.now()
        vals['state'] = 'yes'
        vals['borrow_operate_member'] = self.env.user.id
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

        borrow_record = self.env['funenc.xa.station.borrow.record'].search(
            [('key_no', '=',self.key_no.key_no), ('state', '=','yes')])

        borrow_record.write({'state': 'no','return_member':self.return_member.id,
                             'return_time':datetime.datetime.now(),
                             'return_operate_member':self.env.user.id

                             })

        self.env['funenc.xa.station.borrow.record'].search([('del_ids', '=', 1)]).unlink()



