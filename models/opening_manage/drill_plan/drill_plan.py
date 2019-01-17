# -*- coding: utf-8 -*-
from odoo import models, fields, api

import datetime, time, os
import qrcode
import base64

from ...get_domain import get_line_site_id

class drill_plan(models.Model):
    _name = 'funenc_xa_station.drill_plan'
    _description = u'演练计划'
    _inherit = 'fuenc_station.station_base'
    _rec_name = 'drill_project'
    _order = 'drill_time desc'

    drill_project = fields.Char(string='演练项目', required=True)
    drill_time = fields.Date(string='演练时间', required=True)
    drill_plan = fields.Many2many('ir.attachment', 'drill_plan_ir_attachment_rel_1', 'drill_plan_id',
                                  'ir_attachment_id', string='演练方案')
    drill_hierarchy = fields.Char(string='演练层级', required=True)
    state = fields.Selection(selection=[('not_started', '未开始'), ('underway', '进行中'), ('end', '已结束')],
                             default="not_started"
                             , compute='_compute_state'
                             )
    partake_site_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department', 'drill_plan_ding_department_rel_1',
                                        'drill_plan_id', 'ding_department_id', string='参与站点',
                                        domain=[('department_hierarchy', '=', 3)],required=True)
    is_release = fields.Integer(string='是否已经发布')
    release_time = fields.Datetime(string='发布时间')
    drill_plan_qr = fields.Binary(string='二维码')

    # 演练结果
    drill_result_ids = fields.One2many('funenc_xa_station.drill_result', 'drill_plan_id', string='演练结果',ondelete='set null')

    # 人员签到
    sign_in_ids = fields.One2many('funenc_xa_station.drill_plan_sign_in', 'drill_plan_sign_in_id', string='人员签到情况',ondelete='set null')

    #站点演练
    site_drill_plan_ids = fields.One2many('funenc_xa_station.site_drill_plan','drill_plan_id',string='',ondelete='set null') #  子

    @api.model
    def create(self, vals):
        drill_plan_id = super(drill_plan, self).create(vals)

        # 生成二维码
        self = drill_plan_id
        self.create_qrcode()

        return drill_plan_id

    def _compute_state(self):
        for this in self:
            if this.is_release == 1:
                drill_time = datetime.datetime.strptime(this.drill_time, '%Y-%m-%d')  # 演练时间
                current_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),
                                                          '%Y-%m-%d')  # 当前时间
                drill_time_seconds = time.mktime(drill_time.timetuple())
                current_time_seconds = time.mktime(current_time.timetuple())
                if drill_time_seconds == current_time_seconds:
                    this.state = 'underway'
                elif drill_time_seconds < current_time_seconds:
                    this.state = 'end'
                else:
                    this.state = 'not_started'

    @api.model
    def create_drill_plan(self):
        context = dict(self.env.context or {})
        return {
            'name': '创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.drill_plan',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        return {
            'name': '编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.drill_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'target': 'current',
            'res_id': self.id,
        }

    def delete(self):
        self.unlink()

    def drill_plan_save(self):
        pass

    # 页面详情按钮
    def details(self):
        # record_ids = self.search([
        #     ()
        # ]).ids
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_drill_plan_form_2').id
        return {
            'name': '演练详情',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.drill_plan',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            # 'target': 'new',
        }

    def drill_plan_start(self):
        self.is_release = 1
        self.release_time = datetime.datetime.now()
        partake_site_ids = self.partake_site_ids
        self_id = self.id

        insert_id = []
        #  若此处出现效率问题  采用一条sql插入 没有时间暂用orm 形如下
        #生成 演练结果
        for partake_site_id in partake_site_ids:
            insert_id.append((self_id,1,partake_site_id.id))
            line_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('departmentId', '=', partake_site_id.parentid)]).id
            self.env['funenc_xa_station.drill_result'].create({
                'line_id': line_id,
                'site_id': partake_site_id.id,
                'drill_plan_id': self.id
            })

        # 生成站点详情   此可解决循环orm多次调用数据库问题
        if insert_id:
            sql = 'insert into funenc_xa_station_site_drill_plan(drill_plan_id,create_uid,position) values{}'.format(str(insert_id)[1:-1])
            self.env.cr.execute(sql)

    @get_line_site_id
    @api.model
    def save_drill_plan(self,get_line_site_id,**kw):
        line_id,site_id = get_line_site_id
        user_id = kw.get('user_id')
        drill_plan_id = kw.get('drill_plan_id')
        if line_id and site_id :
            # 生成签到
            check_in = self.env['funenc_xa_station.drill_plan_sign_in'].sudo().search(
                [('sign_user_id', '=', user_id), ('drill_plan_sign_in_id', '=', drill_plan_id)])

            if check_in:
                return '你已签到'

            # 签到人员统计
            drill_plan = self.env['funenc_xa_station.drill_plan'].sudo().search(
                [('id', '=', drill_plan_id)])

            if site_id in drill_plan.partake_site_ids.ids:

                obj = self.env['funenc_xa_station.drill_plan_sign_in'].sudo().create({
                    'sign_in_time': datetime.datetime.now(),
                    'sign_user_id': user_id,
                    'drill_plan_sign_in_id': drill_plan_id,
                    'line_id': line_id,
                    'site_id': site_id

                })

                for drill_result_id in drill_plan.drill_result_ids:
                    if drill_result_id.site_id.id == site_id:
                        # 统计
                        drill_result_id.people_number = drill_result_id.people_number + 1

                for site_drill_plan_id in drill_plan.site_drill_plan_ids:
                    if site_drill_plan_id.position.id == site_id:
                        # 人员签到和站点关联
                        obj.write({'site_drill_plan_id': site_drill_plan_id.id})
                return '签到成功'
            else:
                return '你不属于演练签到人员'
        else:
            return '此人员并无人员属性,请联系管理员在：权限设置/部门管理 下设置'

    def create_qrcode(self):
        '''
        二维码生成
        '''
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
        add_data = {
            'model':'funenc_xa_station.drill_plan',
            'func': 'save_drill_plan',
            'drill_plan_id': self.id
        }
        qr.add_data(add_data)
        img = qr.make_image()
        file_name ="drill_plan_{}.png".format(self.id)

        img.save(file_name)
        imgs = open(file_name, 'rb')
        datas = imgs.read()
        file_b64 = base64.b64encode(datas)
        self.write({
            'drill_plan_qr': file_b64
        })
        imgs.close()
        os.remove(file_name)


class drill_result(models.Model):
    _name = 'funenc_xa_station.drill_result'
    _description = u'演练结果'
    _rec_name = 'line_id'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点',
                              )
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路',
                             )
    people_number = fields.Integer(string='参与演练人数')
    state = fields.Selection(string='状态', selection=[('already_filled', '已填写'), ('unfilled', '未填写')])
    fill_in_date = fields.Datetime(string='填写时间')
    fill_in_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='填写人')

    drill_plan_id = fields.Many2one('funenc_xa_station.drill_plan', string='演练计划相关')
    drill_time = fields.Date(string='演练时间', related='drill_plan_id.drill_time',store=True)


    def edit(self):
        context = dict(self.env.context or {})
        id = None
        for site_drill_plan_id in self.drill_plan_id.site_drill_plan_ids:
            if self.site_id.id == site_drill_plan_id.position.id:
                id = site_drill_plan_id

        drill_situation_ids = self.env['funenc_xa_station.drill_situation'].search([]).ids
        if not id.site_drill_plan_to_drill_situation_ids:
            for drill_situation_id in drill_situation_ids:
                id.env['funenc_xa_station.site_drill_plan_to_drill_situation'].create({
                    'site_drill_plan_id': id.id,
                    'drill_situation_id': drill_situation_id
                })

        return {
            'name': '站点演练编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.site_drill_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': id.id,
            'target': 'current',
        }


class drill_plan_sign_in(models.Model):
    _name = 'funenc_xa_station.drill_plan_sign_in'
    _description = u'演练计划签到情况'

    sign_in_time = fields.Datetime(string='签到时间')
    sign_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='姓名')
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路')
    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点')
    jobnumber = fields.Char(related='sign_user_id.jobnumber', string="工号")
    position = fields.Text(related='sign_user_id.position', string="职位")

    drill_plan_sign_in_id = fields.Many2one('funenc_xa_station.drill_plan', string='演练相关')

    # 站点演练签到
    site_drill_plan_id = fields.Many2one('funenc_xa_station.site_drill_plan',string='站点演练签到相关')

    #  委外人员
    is_alien = fields.Integer(string='外人')  # 1 为外人 其他为签到