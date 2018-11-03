# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api
from ...get_domain import get_domain
import datetime


class site_drill_plan(models.Model):
    _name = 'funenc_xa_station2.site_drill_plan'
    _description = u'站点演练详情'

    # 基本信息
    drill_plan_id = fields.Many2one('funenc_xa_station2.drill_plan', string='演练计划')  # 父
    drill_project = fields.Char(string='演练项目', related='drill_plan_id.drill_project')
    release_time = fields.Datetime(string='发布时间', related='drill_plan_id.release_time')
    site_id = fields.Many2one(string='站点', related='drill_plan_id.site_id')
    line_id = fields.Many2one(string='线路', related='drill_plan_id.line_id')
    drill_hierarchy = fields.Char(string='演练层级', related='drill_plan_id.drill_hierarchy')
    drill_time = fields.Date(string='演练时间', related='drill_plan_id.drill_time')
    drill_plan = fields.Many2many(related='drill_plan_id.drill_plan', string='演练方案')

    site_drill_result = fields.Many2many('ir.attachment', 'site_drill_plan_ir_attachment_rel_1', 'site_drill_plan_id',
                                         'ir_id', string='演练结果附件')

    # 所在站点
    position = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='所在位置')

    #  照片
    #  视频

    site_drill_plan_to_drill_situation_ids = fields.One2many('funenc_xa_station2.site_drill_plan_to_drill_situation',
                                                             'site_drill_plan_id', string='预设', ondelete='set null', )
    # 整改
    proposal_rectification_ids = fields.One2many('funenc_xa_station2.proposal_rectification', 'site_drill_plan_id',
                                                 string='意见及整改')

    # 签到
    sign_in_ids = fields.One2many('funenc_xa_station2.drill_plan_sign_in', 'site_drill_plan_id', string='站点签到')

    def edit(self):
        context = dict(self.env.context or {})
        drill_situation_ids = self.env['funenc_xa_station2.drill_situation'].search([]).ids
        if not self.site_drill_plan_to_drill_situation_ids:
            for drill_situation_id in drill_situation_ids:
                obj = self.env['funenc_xa_station2.site_drill_plan_to_drill_situation'].create({
                    'site_drill_plan_id': self.id,
                    'drill_situation_id': drill_situation_id
                })
                print(obj)

        return {
            'name': '站点演练编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station2.site_drill_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def site_drill_plan_save(self):
        pass

    # @get_domain
    @api.model
    def init_data(self):
        context = dict(self.env.context or {})
        return {
            'name': '列表',
            'type': 'ir.actions.act_window',
            "views": [[False, "tree"], [False, "form"]],
            'res_model': 'funenc_xa_station2.site_drill_plan',
            'context': context,
            'target': 'current',
            # 'domain': domain
        }


class DrillSituation(models.Model):
    _name = 'funenc_xa_station2.drill_situation'
    _description = '演练情况'

    name = fields.Char(string='项目')
    site_drill_plan_to_drill_situation_ids = fields.One2many('funenc_xa_station2.site_drill_plan_to_drill_situation',
                                                             'drill_situation_id', string='')


class site_drill_plan_to_drill_situation(models.Model):
    _name = 'funenc_xa_station2.site_drill_plan_to_drill_situation'
    _description = '站点演练和演练情况中间表'

    site_drill_plan_id = fields.Many2one('funenc_xa_station2.site_drill_plan', string='站点演练')
    drill_situation_id = fields.Many2one('funenc_xa_station2.drill_situation', string='演练情况')

    describe = fields.Char(string='描述')


class proposal_rectification(models.Model):
    _name = 'funenc_xa_station2.proposal_rectification'
    _description = '站点演练整改以及意见'

    # 意见及整改
    proposal_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='意见填写人')
    jobnumber = fields.Char(string="工号", related='proposal_user_id.jobnumber')
    proposal_time = fields.Datetime(string='意见填写时间')
    proposal_question = fields.Text(srting='存在问题及整改建议')

    # 整改

    rectification_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='整改填写人')
    rectification_no = fields.Char(string="工号", related='rectification_user_id.jobnumber')
    rectification_time = fields.Datetime(string='整改填写时间')
    rectification_question = fields.Text(srting='整改情况')

    site_drill_plan_id = fields.Many2one('funenc_xa_station2.site_drill_plan', string='站点演练')

    def edit(self):
        view_form = self.env.ref('funenc_xa_station2.site_drill_plan_edit').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station2.proposal_rectification",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': self.env.context
        }

    def rectification(self):
        view_form = self.env.ref('funenc_xa_station2.site_drill_plan_rectification').id
        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station2.proposal_rectification",
            "res_id": self.id,
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': self.env.context
        }

    def edit_save(self):
        self.proposal_time = datetime.datetime.now()

    def rectification_save(self):
        self.rectification_time = datetime.datetime.now()
