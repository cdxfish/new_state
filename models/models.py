# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.exceptions as msg
import qrcode
from PIL import Image
import os
import base64
from odoo import http
import socket,datetime

class fuenc_station(models.Model):
    _name = 'fuenc_station.station_base'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点', default=lambda self: self.default_site_id())
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路', default=lambda self: self.default_line_id())


    @api.model
    def default_line_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.line_id.id

    @api.model
    def default_site_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.departments[0].id

    @api.constrains('site_id', 'line_id')
    def compute_site_and_line(self):
        if self.env.user.id == 1:
            if not self.line_id:
                raise msg.Warning('线路不能为空')

            if not self.site_id:
                raise msg.Warning('车站不能为空')
        else:
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            if department.department_hierarchy == 3:
                model = self._table

                site_id = self.env.user.dingtalk_user.departments[0].id
                line_id = self.env.user.dingtalk_user.line_id.id
                #   不用orm  因为会递归回调
                sql = 'update {} set site_id = {}, line_id = {} where id = {}'.format(model,site_id,line_id,self.id)
                self.env.cr.execute(sql)


    @api.onchange('line_id')
    def change_line_id(self):
        if not self.line_id:
            return

        department_id = self.line_id.departmentId
        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department_id)]).ids

        return {'domain': {'site_id': [('id', 'in', child_department_ids)]}
                # 'value': {'site_id': None}
                }


class StationIndex(models.Model):
    '''
    打卡记录
    '''
    _name = 'fuenc_station.clock_record'
    _description = '打卡记录'
    _inherit = 'fuenc_station.station_base'

    time = fields.Date(string='日期')
    user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='员工', required=True)
    jobnumber = fields.Char(related='user_id.jobnumber', string="工号")
    position = fields.Text(related='user_id.position', string="职位")
    arrange_order_id = fields.Many2one('funenc_xa_station.arrange_order',string='班次')
    time_length = fields.Float(related='arrange_order_id.save_work_time',string='计划时长(h)')
    clock_site = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='打卡站点')
    clock_start_time =fields.Datetime(string='上班打卡时间')
    clock_end_time = fields.Datetime(string='下班打卡时间')
    work_time = fields.Float(string='工作时长(h)')
    is_overtime = fields.Selection(selection=[('yes','加班'),('no','正常')],default = 'no')
    overtime = fields.Float(string='加班时长')




class generate_qr(models.Model):
    '''
      生成二维码 用于上下班打卡
    '''
    _name = 'funenc_xa_station.generate_qr'
    work_qr = fields.Binary(string='上班二维码')
    off_work_qr = fields.Binary(string='下班二维码')

    def init_data(self):
        self.create_qrcode()
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_generate_qr_list').id
        if self.env.user.has_group('funenc_xa_station.system_fuenc_site'):
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            context['work_qr'] = '/funenc_xa_station/static/images/work_{}.png'.format(department.id)
            context['off_work_qr'] = '/funenc_xa_station/static/images/off_work_{}.png'.format(department.id)
        obj = self.search([])[0]
        return {
            'name': '网站首页',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc.xa.station.borrow.record',
            'context': context,
            'res_id': obj.id,
            'target': 'current',
        }

    def create_qrcode(self):
        '''
        二维码生成
        '''
        if self.env.user.id ==1:
            return
        else:
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            file =os.path.dirname(os.path.dirname(__file__))
            if department.department_hierarchy == 3:

                # 获取本机计算机名称
                hostname = socket.gethostname()
                # 获取本机ip
                ip = socket.gethostbyname(hostname)
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
                qr.add_data('http://{}:8069/funenc_xa_station/check_collect/'.format(ip))
                print('http://{}/fuenc_station/index/'.format(ip))
                img = qr.make_image()
                file_name = file+"/static/images/work_{}.png".format(department.id)
                img.save(file_name)
                obj = self.create({'work_qr':file_name})
                file_name = file+"/static/images/off_work_{}.png".format(department.id)
                qr.add_data('http://{}:8069//funenc_xa_station/off_work/'.format(ip))
                img.save(file_name)
                obj.update({'off_work_qr':file_name})