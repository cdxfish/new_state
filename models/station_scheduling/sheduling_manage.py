# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

import datetime


class ShedulingManage(models.Model):
    _name = 'funenc_xa_station.sheduling_manage'
    _description = '排班管理'
    _inherit = 'fuenc_station.station_base'

    sheduling_start_time = fields.Date(string='开始时间', required=True)
    sheduling_end_time = fields.Date(string='结束时间', required=True)
    class_group_ids = fields.Many2many('funenc_xa_station.class_group', 'sheduling_manage_class_group_2_ref',
                                       'sheduling_manage_id', 'class_group_id', string='选择班组'
                                       )
    arrange_order_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_2_ref',
                                         'sheduling_manage_id', 'arrange_order_id', string='班组班次'
                                         )
    motorized_user_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'sheduling_manage_ding_user_6_ref',
                                          'sheduling_manage_id', 'ding_user_id', string='机动人员选择'
                                          )
    motorized_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_3_ref',
                                     'sheduling_manage_id', 'arrange_order_id', string='机动人员班次'
                                     )
    sheduling_arrange_order_ids = fields.Many2many('funenc_xa_station.arrange_order',
                                                   'sheduling_manage_arrange_order_4_ref',
                                                   'sheduling_manage_id', 'arrange_order_id', string='班组排班规则')
    motorized_rule_ids = fields.Many2many('funenc_xa_station.arrange_order', 'sheduling_manage_arrange_order_5_ref',
                                          'sheduling_manage_id', 'arrange_order_id', string='机动人员排班规则')
    current_rule = fields.Text(string='当前冲突规则', default=lambda self: self.default_current_rule())
    # sort = fields.Integer(string='排序', default=1)

    #  tree显示字段
    show_class_group_name = fields.Char(string='班组')
    show_arrange_order_name = fields.Text(string='班次')
    show_rule_name = fields.Char(string='排班规则', default='无')
    show_sheduling_time = fields.Char(string='排班时间')

    def default_current_rule(self):
        if self.env.user.id == 1:
            return

        site_id = self.env.user.dingtalk_user.departments[0].id
        conflict_rule_dics = self.env['funenc_xa_station.conflict_rule'].search_read([('site_id', '=', site_id),
                                                                                      ('conflict_rule_state', '=',
                                                                                       'enable')
                                                                                      ]
                                                                                     , ['conflict_rule_content',
                                                                                        'conflict_rule'])
        current_rule = ''
        for conflict_rule_dic in conflict_rule_dics:
            current_rule = current_rule + (
                    conflict_rule_dic.get('conflict_rule_content', '') + conflict_rule_dic.get('conflict_rule',
                                                                                               '') + '\n')

        return current_rule

    @api.constrains('class_group_ids', 'arrange_order_ids', 'sheduling_start_time', 'sheduling_end_time')
    def compute_value(self):
        show_class_group_name = ''
        for i, class_group_id in enumerate(self.class_group_ids):
            if i == 0:
                show_class_group_name = show_class_group_name + class_group_id.name
            else:
                show_class_group_name = show_class_group_name + ',' + class_group_id.name

        show_arrange_order_name = ''
        for k, arrange_order_id in enumerate(self.arrange_order_ids):
            if k == 0:
                show_arrange_order_name = show_arrange_order_name + (arrange_order_id.name + arrange_order_id.time)
            else:
                show_arrange_order_name = show_arrange_order_name + ' ,' + (
                        arrange_order_id.name + arrange_order_id.time)
        self.show_class_group_name = show_class_group_name
        self.show_arrange_order_name = show_arrange_order_name
        self.show_rule_name = ''
        self.show_sheduling_time = self.sheduling_start_time + '至' + self.sheduling_end_time

    @api.model
    def sheduling_manage_create(self):
        res_user = self.env.user
        context = dict(self.env.context or {})
        motorized_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].get_motorized_users()
        context['funenc_motorized_user_ids'] = [motorized_user_id.get('id') for motorized_user_id in motorized_user_ids]

        if res_user.id == 1:

            return {
                'name': '创建排班',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'funenc_xa_station.sheduling_manage',
                'context': context,
                # 'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }
        else:
            context['sheduling_manage_site_id'] = res_user.dingtalk_user.departments[0].id
            return {
                'name': '创建排班',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'funenc_xa_station.sheduling_manage',
                'context': context,
                # 'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }

    def sheduling_manage_edit(self):
        context = dict(self.env.context or {})
        res_user = self.env.user
        motorized_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].get_motorized_users()
        context['funenc_motorized_user_ids'] = [motorized_user_id.get('id') for motorized_user_id in motorized_user_ids]
        if res_user.id == 1:
            return {
                'name': '排班详情编辑',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'funenc_xa_station.sheduling_manage',
                'context': context,
                'flags': {'initial_mode': 'edit'},
                'res_id': self.id,
                'target': 'new',
            }
        else:
            context['sheduling_manage_site_id'] = res_user.dingtalk_user.departments[0].id
            return {
                'name': '排班详情编辑',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'funenc_xa_station.sheduling_manage',
                'context': context,
                'flags': {'initial_mode': 'edit'},
                'res_id': self.id,
                'target': 'new',
            }

    def sheduling_manage_delete(self):
        self.unlink()

    @api.model
    def sheduling_start(self,res_id):
        '''
         排班开始  生成排班管理
        :return:
        '''
        if not self:
            self = self.search([('id', '=', res_id)])
        res_user = self.env.user
        if res_user.id == 1:
            return

        site_id = self.env.user.dingtalk_user.departments[0].id
        conflict_rule_dics = self.env['funenc_xa_station.conflict_rule'].search_read([('site_id', '=', site_id),
                                                                                      ('conflict_rule_state', '=',
                                                                                       'enable'),
                                                                                      ('is_certificate', '=', 2)
                                                                                      ], ['save_conflict_rule'],
                                                                                     order='conflict_rule_index asc')
        class_interval = conflict_rule_dics[0].get('save_conflict_rule')  # 版与班之间的间隔 >= h
        rest_day = conflict_rule_dics[1].get('save_conflict_rule')  # 每人连续休息时间 <= d
        night_shift = conflict_rule_dics[2].get('save_conflict_rule')  # 第二天必须排休  1d

        ding_user = res_user.dingtalk_user
        show_position = ding_user.line_name + '-' + ding_user.departments[0].name
        show_sheduling_time = self.show_sheduling_time
        show_arrange_order_name = self.show_arrange_order_name
        current_rule = self.current_rule

        class_group_ids = self.class_group_ids  # 班组
        arrange_order_ids = self.arrange_order_ids.read()  # 班次
        night_index = -1000  # 夜班下标
        for index, arrange_order_id_1 in enumerate(arrange_order_ids):
            if arrange_order_id_1.get('end_time_select') == 'next_day':
                night_index = index

        arrange_order_3 = arrange_order_ids[:-1]  # 排班班次
        start_time = self.sheduling_start_time  # 排班开始时间
        start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = self.sheduling_end_time  # 排班结束时间
        days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1
        time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = start_datetime + datetime.timedelta(days=day)
            datetime_to_str = str_to_datetime.strftime('%Y-%m-%d')[5:11]
            if datetime_to_str == '0':
                time_days.append(datetime_to_str[1:])
            else:
                time_days.append(datetime_to_str)

        group_data = []  # 班组排班
        for class_group_id in class_group_ids:
            class_group_name = class_group_id.name
            group_user_ids = class_group_id.group_user_ids.read(['name', 'position'])  # 班组人员
            for i, group_user_id in enumerate(group_user_ids):
                # group_user_id['index'] = i + 1
                group_user_id['class_group_name'] = class_group_name
                # group_user_id['user_name'] = group_user_id.get('name')
                # group_user_id['position'] = group_user_id.get('position')

                work_time = 0  # 工作总时长
                last_work_time = 0  # 上次工作时长
                # last_class_group_index = 0 # 上次班次 下标
                last_is_night_shift = False  # 上次工作是否是夜班
                night_rest_time = 0  # 夜班休息次数
                continuous_rest_time = 0  # 连续休息时长
                next_work_time = 0  # 下次工作日期范围
                for j, time_day in enumerate(time_days):
                    if j == 0:
                        group_user_id[time_day] = arrange_order_ids[0].get('name')
                        work_time = work_time + arrange_order_ids[0].get('save_work_time')
                        last_work_time = arrange_order_ids[0].get('save_work_time')
                        # last_class_group_index = 0
                        work_time = work_time + arrange_order_ids[0].get('save_work_time')
                        last_work_time = arrange_order_ids[0].get('save_work_time')
                        if arrange_order_ids[0].get('end_time_select') == 'next_day':  # 第一次排班是否是夜班
                            night_rest_time = night_shift
                            last_is_night_shift = True
                            next_work_time = 0
                        else:
                            last_is_night_shift = False

                            if next_work_time + class_interval < 24:
                                next_work_time = next_work_time + class_interval
                            else:
                                next_work_time = abs(next_work_time + class_interval - 24)
                        # arrange_order_ids = arrange_order_ids[-1:] + [arrange_order_ids[0]] # 班次重新排序
                    else:
                        if last_is_night_shift:  # 上次是否是夜班
                            # 这里有问题  夜班不一定设置进去了的 所以班次应该固定
                            group_user_id[time_day] = arrange_order_ids[-1].get('name')
                            last_work_time = 0
                            night_rest_time = night_rest_time - 1
                            if night_rest_time == 0:
                                last_is_night_shift = False

                        else:
                            for arrange_order in arrange_order_ids[:-1]:
                                if int(arrange_order.get('time')[:2] or 0) >= next_work_time:
                                    group_user_id[time_day] = arrange_order.get('name')
                                    last_work_time = arrange_order.get('save_work_time')
                                    work_time = work_time + arrange_order.get('save_work_time')
                                    if arrange_order.get('end_time_select') == 'next_day':
                                        night_rest_time = night_shift
                                        last_is_night_shift = True
                                        next_work_time = 0
                                    else:
                                        last_is_night_shift = False

                                        if next_work_time + class_interval < 24:
                                            next_work_time = next_work_time + class_interval
                                        else:
                                            next_work_time = abs(next_work_time + class_interval - 24)

                                    break

                group_data.append(group_user_id)
            # 上组人员 班次除开休班排最后
            lens = len(arrange_order_ids)
            if lens > 2:
                tail = [arrange_order_ids.pop(lens - 1)]
                arrange_order_ids = arrange_order_ids[1:] + [arrange_order_ids[0]] + tail  # 班组与班次轮排
                if night_index != -1000:
                    night_index = night_index - 1
                    if night_index == -1:
                        night_index = lens - 2


        motorized_data = []  # 班组排班
        motorized_user_ids = self.motorized_user_ids.read()
        motorized_ids = self.motorized_ids.read()

        for i, group_user_id in enumerate(motorized_user_ids):

            work_time = 0  # 工作总时长
            last_work_time = 0  # 上次工作时长
            # last_class_group_index = 0 # 上次班次 下标
            last_is_night_shift = False  # 上次工作是否是夜班
            night_rest_time = 0  # 夜班休息次数
            continuous_rest_time = 0  # 连续休息时长
            next_work_time = 0  # 下次工作日期范围
            for j, time_day in enumerate(time_days):
                if j == 0:
                    group_user_id[time_day] = motorized_ids[0].get('name')
                    work_time = work_time + motorized_ids[0].get('save_work_time')
                    last_work_time = motorized_ids[0].get('save_work_time')
                    # last_class_group_index = 0
                    work_time = work_time + motorized_ids[0].get('save_work_time')
                    last_work_time = motorized_ids[0].get('save_work_time')
                    if motorized_ids[0].get('end_time_select') == 'next_day':  # 第一次排班是否是夜班
                        night_rest_time = night_shift
                        last_is_night_shift = True
                        next_work_time = 0
                    else:
                        last_is_night_shift = False

                        if next_work_time + class_interval < 24:
                            next_work_time = next_work_time + class_interval
                        else:
                            next_work_time = abs(next_work_time + class_interval - 24)
                    # arrange_order_ids = arrange_order_ids[-1:] + [arrange_order_ids[0]] # 班次重新排序
                else:
                    if last_is_night_shift:  # 上次是否是夜班
                        # 这里有问题  夜班不一定设置进去了的 所以班次应该固定
                        group_user_id[time_day] = motorized_ids[-1].get('name')
                        last_work_time = 0
                        night_rest_time = night_rest_time - 1
                        if night_rest_time == 0:
                            last_is_night_shift = False

                    else:
                        for arrange_order in motorized_ids[:-1]:
                            if int(arrange_order.get('time')[:2] or 0) >= next_work_time:
                                group_user_id[time_day] = arrange_order.get('name')
                                last_work_time = arrange_order.get('save_work_time')
                                work_time = work_time + arrange_order.get('save_work_time')
                                if arrange_order.get('end_time_select') == 'next_day':
                                    night_rest_time = night_shift
                                    last_is_night_shift = True
                                    next_work_time = 0
                                else:
                                    last_is_night_shift = False

                                    if next_work_time + class_interval < 24:
                                        next_work_time = next_work_time + class_interval
                                    else:
                                        next_work_time = abs(next_work_time + class_interval - 24)

                                break

            motorized_data.append(group_user_id)
        # 上组人员 班次除开休班排最后
        # lens = len(motorized_ids)
        # if lens > 2:
        #     tail = [motorized_ids.pop(lens - 1)]
        #     arrange_order_ids = motorized_ids[1:] + [motorized_ids[0]] + tail  # 班组与班次轮排
        #     if night_index != -1000:
        #         night_index = night_index - 1
        #         if night_index == -1:
        #             night_index = lens - 2
        group_cols = [{'col': 'class_group_name', 'label': '班组名称'}, {'col': 'name', 'label': '人员名称'},
                      {'col': 'position', 'label': '岗位'}]
        motorized_cols = [{'col': 'name', 'label': '人员名称'}, {'col': 'position', 'label': '岗位'}]
        for key in time_days:
            group_cols.append({'col': key, 'label': key})
            motorized_cols.append({'col': key, 'label': key})
        return [[show_position, show_sheduling_time, show_arrange_order_name, current_rule]] \
               + [group_cols,motorized_cols] + [group_data] + [motorized_data]

    def save(self):
        # self.sheduling_start()
        context = dict(self.env.context or {})
        return {
            'name': '排班管理',
            'type': 'ir.actions.client',
            'res_id': self.id,
            'tag': 'funenc_xa_station_sheduling_manage',
            'target': 'current'
        }

