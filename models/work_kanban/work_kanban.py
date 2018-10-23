# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class work_kanban(models.Model):
    _name = 'funenc_xa_station.work_kanban'
    _description = u'工作看板'
    _rec_name = 'task_originator_id'

    task_originator_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='任务发起人')
    originator_time = fields.Datetime(string='发起时间')
    task_send_user_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'work_kanban_user_rel_1',
                                          'work_kanban_id', 'ding_user_id', string='任务接收人')
    task_start_time = fields.Datetime(string='任务开始时间')
    task_end_time = fields.Datetime(string='任务结束时间')
    task_priority = fields.Selection(selection=[('priority', '高'), ('intermediate', '中'), ('elementary', '低')])
    task_type_id = fields.Many2one('funenc_xa_station.task_type', string='任务类型')
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
    def create_work_kanban(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_work_kanban_form').id
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
        return {
            'name': '工作看板编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.work_kanban',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def work_kanban_save(self):
        dic = self.read(
            ['originator_time', 'task_send_user_ids', 'task_start_time', 'task_end_time',
             'task_priority',
             'task_type_id', 'task_describe', 'task_state'
             ])
        if dic:
            copy_value = dic[0]
            copy_value['task_type_id'] = copy_value.get('task_type_id')[0] or None
            user_ids = self.task_send_user_ids
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
        self.task_state = 'completed'
        child_ids = self.parent_id.child_ids
        for child_id in child_ids:
            if child_id.receive_task_state != 'completed':
                flag = False
                break
        if flag:
            self.prent_id.task_state = 'completed'

    #   app
    @api.model
    def get_kanban_list(self, item):
        self.env.user

        if not item:
            kanban_list = self.search_read([],
                                           ['id', 'task_priority', 'task_describe', 'task_type_id', 'task_end_time'])
            for kanban in kanban_list:
                kanban['task_type_id'] = kanban.get('task_type_id')[1]
        else:
            if item == 'recieve':
                value = '收到的任务'
            elif item == 'send':
                value = 'send_task'
            else:
                value = ''

            kanban_list = self.search_read([('task_type','=', value)],
                                           ['id', 'task_priority', 'task_describe', 'task_type_id', 'task_end_time'])

        return kanban_list
