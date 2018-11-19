# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api
import qrcode

import os, socket
import base64


class training_plan(models.Model):
    _name = 'funenc_xa_station.training_plan'
    _description = u'培训计划'
    _rec_name = 'training_plan_project'

    training_plan_project = fields.Char(string='培训项目')
    leaser_time = fields.Datetime(string='发布日期')
    participate_unit = fields.Char(string='参培单位')
    training_plan_mode = fields.Char(string='培训形式')
    training_plan_major = fields.Char(string='培训专业')
    training_plan_place = fields.Char(string='培训地点')
    training_plan_time = fields.One2many('funenc_xa_station.select_datetime', 'training_plan_id', string='培训时间')
    lecturer = fields.Char(string='授课人')
    training_plan_type = fields.Selection(selection=[('site', '站点培训'), ('concentrate', '集中培训')],default="site")
    remarks = fields.Char(string='备注')
    partake_site_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department', 'training_plan_department_rel_2',
                                        'training_plan_id', 'department_id', string='参与站点',
                                        doamin=[('department_hierarchy', '=', 3)])
    training_plan_qr = fields.Binary(string='培训二维码')
    state = fields.Selection(selection=[('not_started', '未开始'), ('underway', '正在进行'), ('finished', '已结束')],
                             default="not_started")

    #  站点培训成果
    site_training_results_ids = fields.One2many('funenc_xa_station.site_training_results', 'training_plan_id',
                                                string='培训成果')

    # 集中培训 培训成果
    training_plan_to_situation_ids = fields.One2many('funenc_xa_station.training_to_situation', 'training_plan_id',
                                                     string='培训情况'
                                                     )
    # 集中培训效果评价
    training_effect_to_training_plan_ids = fields.One2many('funenc_xa_station.training_effect_to_training_plan',
                                                           'training_plan_id', string='')

    # 签到
    sign_in_user_ids = fields.One2many('funenc_xa_station.personnel_situation', 'training_plan_id', string='集中签到')

    def create_qrcode(self):
        '''
        二维码生成
        '''
        # file = os.path.dirname(os.path.dirname(__file__))
        # qr_file = os.path.dirname(os.path.dirname(file))
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
        qr.add_data('http://{}:8069/controllers/training_plan/punch_the_clock?training_plan_id={}'.format(ip, self.id))
        img = qr.make_image()
        file_name = "punch_the_clock_{}.png".format(self.id)
        img.save(file_name)
        imgs = open(file_name, 'rb')
        datas = imgs.read()
        file_b64 = base64.b64encode(datas)
        self.write({
            'training_plan_qr': file_b64
        })
        imgs.close()
        os.remove(file_name)

    @api.model
    def create_training_plan(self):
        context = dict(self.env.context or {})
        return {
            'name': '培训计划创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.training_plan',
            'context': context,
            'target': 'current',
        }

    def edit(self):
        context = dict(self.env.context or {})
        return {
            'name': '培训计划编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.training_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
            'res_id': self.id,
        }

    def delete(self):

        self.unlink()

    def training_plan_save(self):
        pass

    @api.model
    def create(self, vals):

        training_plan_id = super(training_plan, self).create(vals)

        if training_plan_id.training_plan_type == 'concentrate':
            # 集中培训培训情况预设
            concentrate_training_situations = self.env['funenc_xa_station.concentrate_training_situation'].search(
                []).ids
            for concentrate_training_situation in concentrate_training_situations:
                self.env['funenc_xa_station.training_to_situation'].create(
                    {'training_plan_id': training_plan_id.id,
                     'project_id': concentrate_training_situation
                     }
                )

            # 集中培训培训效果预设
            training_effect_ids = self.env['funenc_xa_station.training_effect'].search([]).ids
            for training_effect_id in training_effect_ids:
                self.env['funenc_xa_station.training_effect_to_training_plan'].create(
                    {'training_plan_id': training_plan_id.id,
                     'training_effect_id': training_effect_id
                     }
                )

        self = training_plan_id
        self.create_qrcode()

        return training_plan_id

    def button_details(self):
        context = dict(self.env.context or {})
        if self.training_plan_type == 'site':
            view_form = self.env.ref('funenc_xa_station.funenc_xa_station_training_plan_form_1').id
        else:
            #  集中培训
            view_form = self.env.ref('funenc_xa_station.funenc_xa_station_training_plan_form_2').id

        return {
            'name': '培训计划详情',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.training_plan',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'current',
            "views": [[view_form, "form"]],
        }

    @api.model
    def return_domain_list(self):
        context = dict(self.env.context or {})
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_training_plan_list').id
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_training_plan_form').id
        return {
            'name': '培训计划详情',
            'type': 'ir.actions.act_window',
            'res_model': 'funenc_xa_station.training_plan',
            'context': context,
            'target': 'current',
            "views": [[view_tree, "tree"], [view_form, "form"]],

        }


class SelectDatetime(models.Model):
    '''
     多选选择时间
    '''

    _name = 'funenc_xa_station.select_datetime'

    name = fields.Datetime(string='培训时间')
    training_plan_id = fields.Many2one('funenc_xa_station.training_plan', string='培训计划相关')


class site_training_results(models.Model):
    '''
     站点培训成果
    '''
    _name = 'funenc_xa_station.site_training_results'
    _inherit = 'fuenc_station.station_base'

    course_hours = fields.Char(string='培训课时')
    training_person_time = fields.Integer(string='培训人次')
    percent_of_pass = fields.Float(string='培训合格率')
    training_content = fields.Text(string='培训内容')
    training_evaluate = fields.Text(string='培训评价')
    questions = fields.Text(string='问题及整改')

    ####
    training_plan_id = fields.Many2one('funenc_xa_station.training_plan', string='培训计划')
    user_ids = fields.One2many('funenc_xa_station.personnel_situation', 'site_training_results_id', string='人员情况')


class PersonnelSituation(models.Model):
    '''
    签到人员情况
    '''
    _name = 'funenc_xa_station.personnel_situation'

    user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='姓名')
    sign_in_time = fields.Datetime(string='签到时间')
    training_result = fields.Selection(string='培训结果', selection=[('qualified', '合格'), ('unqualified', '不合格')])
    line_id = fields.Many2one(related='user_id.line_id', string='所属线路')
    site_id = fields.Char(related='user_id.department_name', string='站点名')
    jobnumber = fields.Char(related='user_id.jobnumber')

    # 培训关联
    training_plan_id = fields.Many2one('funenc_xa_station.training_plan', string='培训关联')

    ### 站点培训关联
    site_training_results_id = fields.Many2one('funenc_xa_station.site_training_results', string='站点培训关联')

    @api.constrains('training_result')
    def compute_percent_of_pass(self):
        '''
        合格率
        :return:
        '''
        site_training_results_ids = self.site_training_results_id.user_ids  # 集中培训结果  签到先关人员
        pass_number = len([site_training_results_id.id for site_training_results_id in site_training_results_ids if
                           site_training_results_id == 'qualified'])  # 合格人数
        if pass_number:
            self.site_training_results_id.percent_of_pass = (pass_number / len(site_training_results_ids)) * 100
        else:
            self.site_training_results_id.percent_of_pass = 0


class training_plan_to_situation(models.Model):
    '''
     培训计划和培训情况中间表
    '''
    _name = 'funenc_xa_station.training_to_situation'
    training_plan_id = fields.Many2one('funenc_xa_station.training_plan', string='培训计划')

    project_id = fields.Many2one('funenc_xa_station.concentrate_training_situation', string='培训情况')
    describe = fields.Char(string='描述')


class concentrate_training_situation(models.Model):
    '''
    集中培训  培训情况
    '''
    _name = 'funenc_xa_station.concentrate_training_situation'
    _rec_name = 'project'

    project = fields.Char(string='项目')

    training_plan_to_situation_ids = fields.One2many('funenc_xa_station.training_to_situation', 'project_id', string='')


class TrainingEffect(models.Model):
    '''
    集中培训 培训效果
    '''
    _name = 'funenc_xa_station.training_effect'
    _description = '培训效果评价'
    _rec_name = 'evaluation_project'

    evaluation_project = fields.Char(string='评估项目')
    evaluation_project_total_score = fields.Integer(string='评估项目总分')
    training_effect_to_training_plan_ids = fields.One2many('funenc_xa_station.training_effect_to_training_plan',
                                                           'training_effect_id', string='')


class training_effect_to_training_plan(models.Model):
    '''
    培训计划和评分中间表
    '''
    _name = 'funenc_xa_station.training_effect_to_training_plan'

    training_plan_id = fields.Many2one('funenc_xa_station.training_plan', string='培训计划')

    training_effect_id = fields.Many2one('funenc_xa_station.training_effect', string='培训效果评分')
    evaluation_project = fields.Char(string='评估项目', related='training_effect_id.evaluation_project')
    evaluation_project_total_score = fields.Integer(string='评估项目总分',
                                                    related='training_effect_id.evaluation_project_total_score')
    total_score = fields.Integer(string='评价得分')
