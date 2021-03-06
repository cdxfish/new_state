# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
import xlwt
from ..get_domain import get_domain
import threading


class CheckRecord(models.Model):
    _name = 'funenc_xa_station.check_record'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin','abstract.export_excel']
    _order = 'check_time desc'
    _description = '考评记录'
    _rec_name = 'staff'

    key = [('check_parment', '考核分部（室）分值')
        , ('relate_per_score', '相关负责人考核分值')
        , ('station_per_score', '车站站长考核分值')
        , ('technology_score', '技术/职能岗考核分值')
        , ('management_score', '管理岗考核分值')
        , ('loca_per_score', '当事人考核分值')
           ]
    key_record = [('safety','安全管理')
        ,('technology','技术管理')
        ,('road','施工管理')
        ,('ticket','票务管理')
        ,('server','服务管理')
        ,('train','培训管理')
        ,('goods','物资管理')
        ,('personnel','人事绩效管理')
        ,('party','党务管理')
        ,('integrated','综合管理')]

    job_number = fields.Char(related='staff.jobnumber', string='工号', readonly=True, track_visibility='onchange')
    staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='考核人员', track_visibility='onchange')
    position = fields.Text(related='staff.position', string='职位', track_visibility='onchange')
    grade = fields.Float(string='参考分值', readonly=True, track_visibility='onchange')
    chose_grade = fields.Selection([('add', '加'), ('subtraction', '减')], string='评分', default='subtraction')
    sure_grede = fields.Float(string='评分分值', track_visibility='onchange')
    check_target = fields.Selection(key_record, string='考评指标',required=True, track_visibility='onchange')
    problem_kind = fields.Many2one('problem_kind_record', string='问题类型',required=True, track_visibility='onchange')
    check_kind = fields.Selection(key, string='考核类别', track_visibility='onchange')
    check_project = fields.Many2one('check_project_record', string='考核项目', track_visibility='onchange')
    incident_describe = fields.Text(string='事件描述', track_visibility='onchange')
    check_person = fields.Char(string='考评人', default=lambda self: self.default_person_id(), track_visibility='onchange')
    check_number = fields.Char(string='工号', default=lambda self: self.default_job_number_id(), track_visibility='onchange')
    check_time = fields.Datetime(string='考评时间', default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_visibility='onchange')
    associated_add = fields.One2many('funenc_xa_station.check_record_add', 'associated', string='新增考评人员')
    all_score = fields.Float(string='总分值', default=100)
    mouth_grade = fields.Float(string='本月评分', track_visibility='onchange')
    grade_degree = fields.Float(string='考评次数', default=1, track_visibility='onchange')
    relevance_check = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='关联字段')

    #根据考核指标的变化，从而变化问题类型
    @api.onchange('check_target')
    def get_problem_record(self):
        res = {}
        if self.check_target and self.problem_kind and self.check_project:
            re = self.env['funenc_xa_station.check_standard'].search([
                ('check_standard','=',self.check_target),
                ('problem_kind','=',self.problem_kind.id),
                ('check_project','=',self.check_project.id)
            ])
            if not re:
                res['value'] = {'problem_kind':None,'check_project':None}
                return res
        if  not self.check_target:
            return {}
        elif not self.check_project:
            record = self.env['funenc_xa_station.check_standard'].search_read([('check_standard','=',self.check_target)])
            ids = [equipment['problem_kind'][0] for equipment in record]



            res['domain'] = {'problem_kind': [('id', 'in', ids)]}
            res['value'] = {'problem_kind': None}

            return  res

    #根据考核指标的变化，从而变化问题类型
    @api.onchange('problem_kind')
    def get_project_record(self):
        res = {}
        if self.check_target and self.problem_kind and self.check_project:
            re = self.env['funenc_xa_station.check_standard'].search([
                ('check_standard','=',self.check_target),
                ('problem_kind','=',self.problem_kind.id),
                ('check_project','=',self.check_project.id)
            ])
            if not re:
                res['value'] = {'check_target':None,'problem_kind':None,'check_project':None}
                return res
        if not self.problem_kind:
            res['domain'] = {'check_project': [(1, '=', 1)]}

            return res
        elif not self.check_project:
            record = self.env['funenc_xa_station.check_standard'].search(
                [('check_standard','=',self.check_target),('problem_kind','=',self.problem_kind.id)])

            ids = [i['check_project'][0].id for i in record]

            res['domain'] = {'check_project': [('id', 'in', ids)]}
            res['value'] = {'check_project': None}

            return  res

    #当问题类型和考核指标都为空的时候选择考核项目直接返回问题类型和考核指标
    @api.onchange('check_project')
    def get_standard_problem(self):
        res = {}
        if self.check_target and self.problem_kind and self.check_project:
            re = self.env['funenc_xa_station.check_standard'].search([
                ('check_standard','=',self.check_target),
                ('problem_kind','=',self.problem_kind.id),
                ('check_project','=',self.check_project.id)
            ])
            if not re:
                res['value'] = {'check_target':None,'problem_kind':None}
                return res
        res = {}
        if not self.check_project:
            res['domain'] = {'check_project': [(1, '=', 1)]}

            return res
        elif not self.problem_kind or  not self.check_target:
            record = self.env['funenc_xa_station.check_standard'].search(
                [('check_project', '=', self.check_project.id)])
            if record:
                self.problem_kind = record.problem_kind.id
                self.check_target = record.check_standard



    # 自动获取登录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id == 1:
            return
        return self.env.user.dingtalk_user.name

    # 查看登录人的工号
    @api.model
    def default_job_number_id(self):
        if self.env.user.id == 1:
            return

        return self.env.user.dingtalk_user.jobnumber

    @api.model
    @get_domain
    def get_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.check_record_tree').id
        context = self.env.context
        return {
            'name': '考评管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "list"]],
            'res_model': 'funenc_xa_station.check_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "target": "current",
            "top_widget_options": '''{'tabs':
                                   [
                                       {'title': '考评记录',
                                       'action':  'funenc_xa_station.check_record_act',
                                       'group':'funenc_xa_station.table_evaluation_record',
                                       },
                                       {
                                           'title': '考评汇总',
                                           'action2' : 'funenc_xa_station.funenc_xa_check',
                                           'group' : 'funenc_xa_station.table_evaluation_total',
                                           },
                                       {
                                           'title': '奖励记录',
                                           'action2':  'funenc_xa_station.award_record_act',
                                           'group' : 'funenc_xa_station.table_reward_record',
                                           },
                                      {
                                           'title': '奖励汇总',
                                           'action2':  'funenc_xa_station.funenc_xa_award',
                                           'group' : 'funenc_xa_station.table_reward_total',
                                           },
                                   ]
                               }''',
            'context': context,
        }

    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.check_record_tree').id
        return {
            'name': '考评管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.check_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                           [
                               {'title': '考评记录',
                               'action':  'funenc_xa_station.check_record_act',
                               'group':'funenc_xa_station.table_evaluation_record',
                               },
                               {
                                   'title': '奖励记录',
                                   'action2':  'funenc_xa_station.award_record_act',
                                   'group' : 'funenc_xa_station.table_reward_record',
                                   },
                           ]
                       }''',
            'context': self.env.context,
        }

    # 在创建的时候整数据
    @api.model
    def create(self, vals):
        if vals.get('chose_grade') == 'add':
            vals['sure_grede'] = abs(vals.get('sure_grede'))
        elif vals.get('chose_grade') == 'subtraction':
            vals['sure_grede'] = -abs(vals.get('sure_grede'))

        # 将新增的考评人员填写到页面
        record = vals.get('associated_add')
        if record:
            for i_re in record:
                key = {
                    'line_id': vals['line_id'],
                    'site_id': vals['site_id'],
                    'staff': i_re[2]['check_person'],
                    'check_target': vals['check_target'],
                    'problem_kind': vals['problem_kind'],
                    'check_project': vals['check_project'],
                    'sure_grede': i_re[2]['grade'],
                    'incident_describe': i_re[2]['incident_describe'],
                    'check_kind': i_re[2]['check_kind'],
                    'chose_grade': i_re[2]['chose_grade'],
                }
                super(CheckRecord, self).create(key)
        self.env['funenc_xa_station.check_standard'].search([
                                                    ('check_standard','=',vals.get('check_target')),
                                                    ('check_standard','=',vals.get('check_target')),
                                                     ])

        # 将数据转接到人员信息
        vals['relevance_check'] = vals['staff']
        return super(CheckRecord, self).create(vals)

    # @api.model
    # def procure_calculation(self):
    #     threaded_calculation = threading.Thread(target=self._procure_calculation_orderpoint, args=())
    #     threaded_calculation.start()
    #     return {'type': 'ir.actions.act_window_close'}
    @api.model
    def new_add_record(self):
        a= 1
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.check_record',
            # 'res_id':'',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    @api.constrains('chose_grade')
    def chose_grade_grade(self):
        if self.chose_grade == 'subtraction':
            a = -abs(self.sure_grede)
            self.sure_grede = a
        elif self.chose_grade == 'add':
            self.sure_grede = abs(self.sure_grede)

    @api.onchange('check_kind')
    def parment_score(self):
        if not self.check_kind:
            res = {}
            res['domain'] = {'check_project': [(1, '=', 1)]}

            return res
        record = self.env['funenc_xa_station.check_standard'].search_read([('check_project', '=', self.check_project.id)])
        if record:
            if self.check_kind == 'check_parment':
                check_kind1 = record[0].get('check_parment')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'relate_per_score':
                check_kind1 = record[0].get('relate_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'station_per_score':
                check_kind1 = record[0].get('station_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'technology_score':
                check_kind1 = record[0].get('technology_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'management_score':
                check_kind1 = record[0].get('management_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'loca_per_score':
                check_kind1 = record[0].get('loca_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}
            else:
                return {'value': {'grade': 0}}

    @api.onchange('check_kind')
    def parment_sure_grede(self):
        if not self.check_kind:
            res = {}
            res['domain'] = {'check_project': [(1, '=', 1)]}

            return res
        record = self.env['funenc_xa_station.check_standard'].search_read(
            [('check_project', '=', self.check_project.id)])
        if record:
            if self.check_kind == 'check_parment':
                check_kind1 = record[0].get('check_parment')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'relate_per_score':
                check_kind1 = record[0].get('relate_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'station_per_score':
                check_kind1 = record[0].get('station_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'technology_score':
                check_kind1 = record[0].get('technology_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'management_score':
                check_kind1 = record[0].get('management_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}

            elif self.check_kind == 'loca_per_score':
                check_kind1 = record[0].get('loca_per_score')
                return {'value': {'grade': check_kind1,'sure_grede':check_kind1}}
            else:
                return {'value': {'grade': 0}}

    def write_data_to_excel(self):
        one_row = ['线路', '站点', '工号', '考核人员', '职位', '评分分值', '考评指标', '问题类型', '考核类别', '考核项目', '事件描述', \
                   '考评人', '工号', '考评时间']

        # 新建一个excel文件
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        try:
            for i, one in zip([cu for cu in range(len(one_row))], one_row):
                table.write(0, i, one)
            file.save('考评记录.xls')
        except SystemError:
            print('系统错误')

    def check_record_delete(self):
        self.env['funenc_xa_station.check_record'].search([('id', '=', self.id)]).unlink()

    def check_record_change(self):
        view_form = self.env.ref('funenc_xa_station.check_record_form_modify').id
        return {
            'name': '考评记录',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.check_record',
            'res_id': self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


class AddResponsibility(models.Model):
    key = [('check_parment', '考核分部（室）分值')
        , ('relate_per_score', '相关负责人考核分值')
        , ('station_per_score', '车站站长考核分值')
        , ('technology_score', '技术/职能岗考核分值')
        , ('management_score', '管理岗考核分值')
        , ('loca_per_score', '当事人考核分值')
           ]

    _name = 'funenc_xa_station.check_record_add'

    # 用来作为关联字段来获取分数
    def __default_reference_grade(self):
        if self._context.get('active_id', False):
            return self._context['active_id']

    check_person = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='责任人员')
    position = fields.Text(related='check_person.position', string='职位')
    check_number = fields.Char(related='check_person.jobnumber', string='工号', readonly=True)
    check_kind = fields.Selection(key, string='考核类别')
    reference_grade = fields.Float(string='参考分值')
    grade = fields.Float(string='评分')
    chose_grade = fields.Selection([('add', '加'), ('subtraction', '减')], string='评分', default='subtraction')
    incident_describe = fields.Text(string='事件描述')
    associated = fields.Many2one('funenc_xa_station.check_record', string='关联字段没有实际意义',
                                 default=__default_reference_grade)

    @api.onchange('check_kind')
    def _onchange_check_kind(self):
        if self.check_kind:
            a = self.associated
            # 获取当前选项的分数
            score = self.env['funenc_xa_station.check_standard'].search_read(
                [('check_project', '=', self.associated.check_project.id)], [self.check_kind])[0].get(
                self.check_kind)
            self.reference_grade = score
            self.grade = score
