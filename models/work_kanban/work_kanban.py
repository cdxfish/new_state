# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api

import datetime


class work_kanban(models.Model):
    _name = 'funenc_xa_station.work_kanban'
    _description = u'工作看板'
    _rec_name = 'task_originator_id'
    # _inherit = 'fuenc_station.station_base'

    task_originator_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='任务发起人', readonly=True,
                                         default=lambda self: self.default_task_originator_id())
    originator_time = fields.Datetime(string='发起时间', required=True)
    task_send_user_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'work_kanban_user_rel_1',
                                          'work_kanban_id', 'ding_user_id', string='任务接收人', required=True)
    task_start_time = fields.Datetime(string='任务开始时间', required=True)
    task_end_time = fields.Datetime(string='任务结束时间', required=True)
    task_priority = fields.Selection(selection=[('priority', '高'), ('intermediate', '中'), ('elementary', '低')],
                                     required=True)
    task_type_id = fields.Many2one('funenc_xa_station.task_type', string='任务类型', required=True)
    task_type = fields.Selection(selection=[('send_task', '发起的任务'), ('receive_task', '收到的任务')],
                                 default="send_task")  # 区分接收的任务还是发送的任务分类
    is_send = fields.Integer(string='任务是否发送')
    task_describe = fields.Char(string='任务描述')
    task_state = fields.Selection(selection=[('completed', '完成'), ('not_completed', '未完成')],
                                  default="not_completed")  # 发送任务状态

    ####
    parent_id = fields.Many2one('funenc_xa_station.work_kanban', string='发起任务')
    child_ids = fields.One2many('funenc_xa_station.work_kanban', 'parent_id', string='接收任务情况')
    task_feedback = fields.Char(string='任务反馈')
    receive_task_state = fields.Selection(selection=[('receive_state', '接收状态'), ('completed', '已完成')])  # 接收任务状态
    completed_time = fields.Datetime(string='接收任务完成时间')
    task_send_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='完成任务接收人')  # 完成任务接收人

    @api.model
    def default_task_originator_id(self):
        if self.env.user.id == 1:
            return
        else:
            return self.env.user.dingtalk_user.id

    @api.model
    def create_work_kanban(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_create_form').id
        return {
            'name': '新增任务发起',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_form_2').id
        return {
            'name': '工作看板编辑',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
            'res_id': self.id
        }

    def delete(self):
        self.unlink()

    def detail(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_form').id
        return {
            'name': '工作看板编辑',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
            'res_id': self.id
        }

    def work_kanban_save(self):
        dic = self.read(
            ['originator_time', 'task_send_user_ids', 'task_start_time', 'task_end_time',
             'task_priority', 'task_originator_id',
             'task_type_id', 'task_describe', 'task_state'
             ])
        if dic:
            copy_value = dic[0]
            if copy_value.get('task_originator_id'):
                copy_value['task_originator_id'] = copy_value.get('task_originator_id')[0]
            else:
                copy_value['task_originator_id'] = None

            if copy_value['task_type_id']:
                copy_value['task_type_id'] = copy_value.get('task_type_id')[0]
            else:
                copy_value['task_type_id'] = None
            user_ids = self.task_send_user_ids
            copy_value['task_send_user_ids'] = [(6, 0, copy_value.get('task_send_user_ids'))]

            for user in user_ids:
                # 人物不多循环创建不影响效率
                copy_value['task_type'] = 'receive_task'
                copy_value['parent_id'] = self.id
                copy_value['receive_task_state'] = 'receive_state'
                copy_value['task_send_user_id'] = user.id
                copy_value['receive_task_state'] = 'receive_state'

                self.create(copy_value)
        self.is_send = 1

    def check_task_complete(self):
        '''
         任务完成
        :return:
        '''
        flag = True
        self.receive_task_state = 'completed'
        self.completed_time = datetime.datetime.now()
        child_ids = self.parent_id.child_ids
        for child_id in child_ids:
            if child_id.receive_task_state != 'completed':
                flag = False
                break
        if flag:
            self.parent_id.task_state = 'completed'
            self.parent_id.child_ids.write({
                'task_state': 'completed'
            })

    #   app
    @api.model
    def get_kanban_list(self, item):
        ding_user = self.env.user.dingtalk_user

        if not item:
            return []
            # kanban_list = self.search_read([],
            #                                ['id', 'task_priority', 'task_describe', 'task_type_id', 'task_end_time'])
            # for kanban in kanban_list:
            #     kanban['task_type_id'] = kanban.get('task_type_id')[1]
        else:
            if item == 'recieve':
                kanban_list = self.search_read(
                    [('task_type', '=', 'receive_task'), ('task_send_user_id', '=', ding_user.id)],
                    ['id', 'task_priority', 'task_describe', 'task_type_id',
                     'task_end_time'])
            elif item == 'send':
                kanban_list = self.search_read(
                    [('task_type', '=', 'send_task'), ('task_originator_id', '=', ding_user.id)],
                    ['id', 'task_priority', 'task_describe', 'task_type_id',
                     'task_end_time'])

            else:
                kanban_list = self.search_read(
                    ['|', '&', ('task_type', '=', 'receive_task'), ('task_send_user_id', '=', ding_user.id), '&',
                     ('task_type', '=', 'send_task'), ('task_originator_id', '=', ding_user.id)],
                    ['id', 'task_priority', 'task_describe', 'task_type_id',
                     'task_end_time'])

            for kanban in kanban_list:
                kanban['task_type_id'] = kanban.get('task_type_id')[1]

        return kanban_list

    @api.model
    def get_kanban_by_id(self, id):
        kanban = self.search_read([('id', '=', id)],
                                  ['id', 'task_originator_id', 'originator_time', 'task_start_time', 'task_state',
                                   'task_end_time', 'task_priority', 'task_type_id', 'task_send_user_id',
                                   'task_describe', 'task_send_user_ids', 'receive_task_state',
                                   'task_send_user_id', 'child_ids', 'task_type'
                                   ])
        if kanban:
            kanban = kanban[0]
            if kanban.get('task_originator_id'):
                kanban['sender'] = kanban.get('task_originator_id')[1]
            else:
                kanban['sender'] = None
            kanban.pop('task_originator_id')
            if kanban.get('task_send_user_ids'):
                kanban['sendee'] = kanban.get('task_send_user_ids')
                kanban['sendee'] = [self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search([('id', '=', user_id)]).name
                                    for user_id in kanban.get('task_send_user_ids')]

            else:
                kanban['sendee'] = None
            kanban.pop('task_send_user_id')
            kanban['complateInfo'] = []
            child_ids = self.search([('id', 'in', kanban.get('child_ids'))])
            for child_id in child_ids:
                dic = {'id': child_id.task_send_user_id.id,
                       'name': child_id.task_send_user_id.name,
                       'complateTime': child_id.completed_time or '',
                       'feedback': child_id.task_feedback or '',
                       }
                kanban['complateInfo'].append(dic)
            if kanban.get('task_type_id'):
                kanban['task_type_id'] = kanban.get('task_type_id')[1]
            else:
                kanban['task_type_id'] = None

            return kanban
        else:
            return []

    @api.model
    def app_save_work_kanban(self, **kw):
        try:
            ding_user = self.env.user.dingtalk_user

            kw['task_originator_id'] = ding_user.id
            kw['originator_time'] = datetime.datetime.now()

            task_send_user_ids = [int(id) for id in kw.get('ids')]
            kw['task_send_user_ids'] = [(6, 0, task_send_user_ids)]
            obj = self.create(kw)
            obj.write({'is_send': 1})

            for user_id in task_send_user_ids:
                kw['task_type'] = 'receive_task'
                kw['parent_id'] = obj.id
                kw['receive_task_state'] = 'receive_state'
                kw['task_send_user_id'] = user_id

                self.create(kw)

            return True
        except Exception:
            return False

    @api.model
    def app_save_kanban_type(self, taskid, feedBackContent):
        self = self.browse([int(taskid)])
        if self:
            flag = True
            self.receive_task_state = 'completed'
            self.completed_time = datetime.datetime.now()
            self.task_feedback = feedBackContent
            child_ids = self.parent_id.child_ids
            for child_id in child_ids:
                if child_id.receive_task_state != 'completed':
                    flag = False
                    break
            if flag:
                self.parent_id.task_state = 'completed'

            return {'receive_task_state': 'completed'}
        else:
            return {'receive_task_state': 'receive_state'}

    @api.multi
    def init_data(self):
        context = dict(self.env.context or {})
        context['group_by'] = 'task_type'
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_form').id
        list = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_list').id
        # kabna_id =self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_kanban').id
        if self.env.user.id == 1:
            domain = []
        else:
            ding_user = self.env.user.dingtalk_user
            #     if department_id.department_hierarchy ==1:
            #         domain=[]
            #     elif department_id.department_hierarchy == 2:
            #         domain=[]
            #     else:
            #         domain = []

            domain = ['|', '&', '&', '&',

                      ('task_originator_id', '=', ding_user.id), ('task_state', '=', 'not_completed'),
                      ('task_state', '=', 'not_completed'), ('task_type', '=', 'send_task'),
                      '&', ('task_send_user_id', '=', ding_user.id),
                      ('receive_task_state', '=', 'receive_state')
                      ]

        return {
            'name': '新增任务发起',
            'type': 'ir.actions.act_window',
            "views": [[list, 'tree'], [view_form, 'form']],
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'target': 'current',
            'domain': domain
        }

    @api.multi
    def my_work_kanban(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_form_2').id
        list = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_list_2').id
        # kabna_id =self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_kanban').id
        if self.env.user.id == 1:
            domain = []
        else:
            ding_user = self.env.user.dingtalk_user
            #     if department_id.department_hierarchy ==1:
            #         domain=[]
            #     elif department_id.department_hierarchy == 2:
            #         domain=[]
            #     else:
            #         domain = []

            domain = ['|',
                      '&', ('task_originator_id', '=', ding_user.id), ('task_type', '=', 'send_task'),
                      ('task_send_user_id', '=', ding_user.id)

                      ]

        return {
            'name': '新增任务发起',
            'type': 'ir.actions.act_window',
            "views": [[list, 'tree'], [view_form, 'form']],
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'target': 'current',
            'domain': domain
        }
