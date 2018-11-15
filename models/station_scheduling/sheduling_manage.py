# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

import datetime
import calendar
from copy import deepcopy


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
    sheduling_arrange_order_id = fields.Many2one('funenc_xa_station.arrange_class_manage', string='班组排班规则')
    motorized_rule_id = fields.Many2one('funenc_xa_station.arrange_class_manage', string='机动人员排班规则')
    current_rule = fields.Text(string='当前冲突规则', default=lambda self: self.default_current_rule())

    #  tree显示字段
    show_class_group_name = fields.Char(string='班组')
    show_arrange_order_name = fields.Text(string='班次')
    show_rule_name = fields.Char(string='排班规则', default='无')
    show_sheduling_time = fields.Char(string='排班时间')

    @api.onchange('site_id')
    def onchange_site_id(self):
        if not self.site_id:
            return
        funenc_motorized_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].get_motorized_users_by_site_id(self.site_id.id)

        return {'domain': {'motorized_user_ids': [('id', 'in', funenc_motorized_user_ids)]}
                }

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
                    conflict_rule_dic.get('conflict_rule_content', '') + (conflict_rule_dic.get('conflict_rule',
                                                                                                '') or '*0') + '\n')
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
        context['funenc_motorized_user_ids'] = None

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
        context['funenc_motorized_user_ids'] =  self.env['cdtct_dingtalk.cdtct_dingtalk_users'].get_motorized_users_by_site_id(self.site_id.id)
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

    def save(self):
        show_data = self.sheduling_start()
        return {
            'name': '排班管理',
            'type': 'ir.actions.client',
            'tag': 'act_xa_station_sheduling_manage_1_action',
            'target': 'current',
            'params': {'show_data': show_data}
        }

    def sheduling_manage_clint(self):
        show_data = self.get_sheuling_list(self.site_id.id, self.sheduling_start_time, self.sheduling_end_time)
        return {
            'name': '排班管理',
            'type': 'ir.actions.client',
            'tag': 'act_xa_station_sheduling_manage_1_action',
            'target': 'current',
            'params': {'show_data': show_data}
        }

    # @api.model
    # def sheduling_start(self):
    #     '''
    #      排班开始  生成排班记录
    #     :return:
    #     '''
    #     # if not self:
    #     #     self = self.search([('id', '=', res_id)])
    #     # res_user = self.env.user
    #     # if res_user.id == 1:
    #     #     return
    #
    #     # site_id = self.env.user.dingtalk_user.departments[0].id
    #     line_id = self.line_id.id
    #     site_id = self.site_id.id
    #     conflict_rule_dics = self.env['funenc_xa_station.conflict_rule'].search_read([('site_id', '=', site_id),
    #                                                                                   ('conflict_rule_state', '=',
    #                                                                                    'enable'),
    #                                                                                   ('is_certificate', '=', 2)
    #                                                                                   ], ['save_conflict_rule'],
    #                                                                                  order='conflict_rule_index asc')
    #     class_interval = conflict_rule_dics[0].get('save_conflict_rule')  # 版与班之间的间隔 >= h
    #     rest_day = conflict_rule_dics[1].get('save_conflict_rule')  # 每人连续休息时间 <= d
    #     night_shift = conflict_rule_dics[2].get('save_conflict_rule')  # 第二天必须排休  1d
    #
    #     # ding_user = res_user.dingtalk_user
    #     show_position = self.line_id.name + '-' + self.site_id.name
    #     show_sheduling_time = self.show_sheduling_time
    #     show_arrange_order_name = self.show_arrange_order_name
    #     current_rule = self.current_rule
    #
    #     class_group_ids = self.class_group_ids  # 班组
    #     arrange_order_ids = self.arrange_order_ids.read()  # 班次
    #     night_index = -1000  # 夜班下标
    #     for index, arrange_order_id_1 in enumerate(arrange_order_ids):
    #         if arrange_order_id_1.get('end_time_select') == 'next_day':
    #             night_index = index
    #
    #     arrange_order_3 = arrange_order_ids[:-1]  # 排班班次
    #     start_time = self.sheduling_start_time  # 排班开始时间
    #     start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    #     end_time = self.sheduling_end_time  # 排班结束时间
    #     days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1
    #     time_days = []  # 排班显示时间
    #     for day in range(days):
    #         str_to_datetime = start_datetime + datetime.timedelta(days=day)
    #         time_days.append(str_to_datetime)
    #
    #     group_data = []  # 班组排班
    #     for class_group_id in class_group_ids:
    #         class_group_name = class_group_id.name
    #         group_user_ids = class_group_id.group_user_ids.read(['name', 'position', 'id'])  # 班组人员
    #         for i, group_user_id in enumerate(group_user_ids):
    #             # group_user_id['index'] = i + 1
    #             # group_user_id['user_name'] = group_user_id.get('name')
    #             # group_user_id['position'] = group_user_id.get('position')
    #
    #             work_time = 0  # 工作总时长
    #             last_work_time = 0  # 上次工作时长
    #             # last_class_group_index = 0 # 上次班次 下标
    #             last_is_night_shift = False  # 上次工作是否是夜班
    #             night_rest_time = 0  # 夜班休息次数
    #             continuous_rest_time = 0  # 连续休息时长
    #             next_work_time = 0  # 下次工作日期范围
    #             for j, time_day in enumerate(time_days):
    #                 data = []  # 班组   (line_id,site_id,user_id,class_group_id,sheduling_date,order_type,work_time,arrange_order_id)
    #                 data.append(line_id)
    #                 data.append(site_id)
    #                 data.append(group_user_id.get('id'))
    #                 data.append(class_group_id.id)
    #                 data.append(time_day.strftime('%Y-%m-%d'))
    #                 data.append('order_group')
    #                 data.append(arrange_order_ids[0].get('save_work_time', 0))
    #                 if j == 0:
    #                     data.append(arrange_order_ids[0].get('id'))
    #                     work_time = work_time + arrange_order_ids[0].get('save_work_time')
    #                     last_work_time = arrange_order_ids[0].get('save_work_time')
    #                     if arrange_order_ids[0].get('end_time_select') == 'next_day':  # 第一次排班是否是夜班
    #                         night_rest_time = night_shift
    #                         last_is_night_shift = True
    #                         next_work_time = 0
    #                     else:
    #                         last_is_night_shift = False
    #
    #                         if next_work_time + class_interval < 24:
    #                             next_work_time = next_work_time + class_interval
    #                         else:
    #                             next_work_time = abs(next_work_time + class_interval - 24)
    #                     # arrange_order_ids = arrange_order_ids[-1:] + [arrange_order_ids[0]] # 班次重新排序
    #                 else:
    #                     if last_is_night_shift:  # 上次是否是夜班
    #                         # 这里有问题  夜班不一定设置进去了的 所以班次应该固定
    #                         data.append(arrange_order_ids[-1].get('id'))
    #                         last_work_time = 0
    #                         night_rest_time = night_rest_time - 1
    #                         if night_rest_time == 0:
    #                             last_is_night_shift = False
    #
    #                     else:
    #                         for arrange_order in arrange_order_ids[:-1]:
    #                             if int(arrange_order.get('time')[:2] or 0) >= next_work_time:
    #                                 data.append(arrange_order.get('id'))
    #                                 last_work_time = arrange_order.get('save_work_time')
    #                                 work_time = work_time + arrange_order.get('save_work_time')
    #                                 if arrange_order.get('end_time_select') == 'next_day':
    #                                     night_rest_time = night_shift
    #                                     last_is_night_shift = True
    #                                     next_work_time = 0
    #                                 else:
    #                                     last_is_night_shift = False
    #
    #                                     if next_work_time + class_interval < 24:
    #                                         next_work_time = next_work_time + class_interval
    #                                     else:
    #                                         next_work_time = abs(next_work_time + class_interval - 24)
    #
    #                                 break
    #                 group_data.append(tuple(data))
    #
    #             # group_data.append(group_user_id)
    #         # 上组人员 班次除开休班排最后
    #         lens = len(arrange_order_ids)
    #         if lens > 2:
    #             tail = [arrange_order_ids.pop(lens - 1)]
    #             arrange_order_ids = arrange_order_ids[1:] + [arrange_order_ids[0]] + tail  # 班组与班次轮排
    #             if night_index != -1000:
    #                 night_index = night_index - 1
    #                 if night_index == -1:
    #                     night_index = lens - 2
    #
    #     motorized_data = []  # 机动人员排班
    #     motorized_user_ids = self.motorized_user_ids.read()
    #     motorized_ids = self.motorized_ids.read()
    #
    #     # motorized_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].get_motorized_users()
    #     # set([motorized_user_id.get('id') for motorized_user_id in motorized_user_ids]) -
    #
    #     for i, group_user_id in enumerate(motorized_user_ids):
    #
    #         work_time = 0  # 工作总时长
    #         last_work_time = 0  # 上次工作时长
    #         # last_class_group_index = 0 # 上次班次 下标
    #         last_is_night_shift = False  # 上次工作是否是夜班
    #         night_rest_time = 0  # 夜班休息次数
    #         continuous_rest_time = 0  # 连续休息时长
    #         next_work_time = 0  # 下次工作日期范围
    #         for j, time_day in enumerate(time_days):
    #             data_2 = []  # (line_id,site_id,user_id,sheduling_date,order_type,work_time,arrange_order_id)
    #             data_2.append(line_id)
    #             data_2.append(site_id)
    #             data_2.append(group_user_id.get('id'))
    #             data_2.append(time_day.strftime('%Y-%m-%d'))
    #             data_2.append('motorized_group')
    #             data_2.append(arrange_order_ids[0].get('save_work_time', 0))
    #             if j == 0:
    #                 data_2.append(motorized_ids[0].get('id'))
    #                 work_time = work_time + motorized_ids[0].get('save_work_time')
    #                 last_work_time = motorized_ids[0].get('save_work_time')
    #                 # last_class_group_index = 0
    #                 if motorized_ids[0].get('end_time_select') == 'next_day':  # 第一次排班是否是夜班
    #                     night_rest_time = night_shift
    #                     last_is_night_shift = True
    #                     next_work_time = 0
    #                 else:
    #                     last_is_night_shift = False
    #
    #                     if next_work_time + class_interval < 24:
    #                         next_work_time = next_work_time + class_interval
    #                     else:
    #                         next_work_time = abs(next_work_time + class_interval - 24)
    #                 # arrange_order_ids = arrange_order_ids[-1:] + [arrange_order_ids[0]] # 班次重新排序
    #             else:
    #                 if last_is_night_shift:  # 上次是否是夜班
    #                     # 这里有问题  夜班不一定设置进去了的 所以班次应该固定
    #                     data_2.append(motorized_ids[-1].get('id'))
    #                     last_work_time = 0
    #                     night_rest_time = night_rest_time - 1
    #                     if night_rest_time == 0:
    #                         last_is_night_shift = False
    #
    #                 else:
    #                     for arrange_order in motorized_ids[:-1]:
    #                         if int(arrange_order.get('time')[:2] or 0) >= next_work_time:
    #                             data_2.append(arrange_order.get('id'))
    #                             last_work_time = arrange_order.get('save_work_time')
    #                             work_time = work_time + arrange_order.get('save_work_time')
    #                             if arrange_order.get('end_time_select') == 'next_day':
    #                                 night_rest_time = night_shift
    #                                 last_is_night_shift = True
    #                                 next_work_time = 0
    #                             else:
    #                                 last_is_night_shift = False
    #
    #                                 if next_work_time + class_interval < 24:
    #                                     next_work_time = next_work_time + class_interval
    #                                 else:
    #                                     next_work_time = abs(next_work_time + class_interval - 24)
    #
    #                             break
    #             motorized_data.append(tuple(data_2))
    #     if str(group_data)[1:-1]:
    #         insert_sql = "insert into funenc_xa_station_sheduling_record(line_id,site_id,user_id,class_group_id,sheduling_date,order_type,work_time,arrange_order_id)" \
    #                      "values{}".format(str(group_data)[1:-1])
    #         self.env.cr.execute(insert_sql)
    #     if str(motorized_data)[1:-1]:
    #         insert_sql = "insert into funenc_xa_station_sheduling_record(line_id,site_id,user_id,sheduling_date,order_type,work_time,arrange_order_id)" \
    #                      "values{}".format(str(motorized_data)[1:-1])
    #         self.env.cr.execute(insert_sql)
    #
    #     show_data = self.get_sheuling_list(site_id, start_time, end_time)
    #
    #     return show_data

    # @api.model
    # def sheduling_start(self):
    #
    #     site_id = self.site_id.id
    #     conflict_rule_dics = self.env['funenc_xa_station.conflict_rule'].search_read([('site_id', '=', site_id),
    #                                                                                   ('conflict_rule_state', '=',
    #                                                                                    'enable'),
    #                                                                                   ('is_certificate', '=', 2)
    #                                                                                   ], ['save_conflict_rule'],
    #                                                                                  order='conflict_rule_index asc')
    #     class_interval = conflict_rule_dics[0].get('save_conflict_rule')  # 版与班之间的间隔 >= h
    #     rest_day = conflict_rule_dics[1].get('save_conflict_rule')  # 每人连续休息时间 <= d
    #     night_shift = conflict_rule_dics[2].get('save_conflict_rule')  # 第二天必须排休  1d
    #
    #     show_position = self.line_id.name + '-' + self.site_id.name
    #     show_sheduling_time = self.show_sheduling_time
    #     show_arrange_order_name = self.show_arrange_order_name
    #     current_rule = self.current_rule
    #     sheduling_arrange_order_ids = self.sheduling_arrange_order_ids  # 班组人员规则规则
    #     motorized_rule_ids = self.motorized_rule_ids  # 机动规则规则
    #
    #     class_group_ids = self.class_group_ids  # 班组
    #     arrange_order_ids = self.arrange_order_ids  # 班次
    #     motorized_user_ids = self.motorized_user_ids  # 机动人员
    #     motorized_ids = self.motorized_ids  # 机动人员班次
    #
    #     start_time = self.sheduling_start_time  # 排班开始时间
    #     start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    #     end_time = self.sheduling_end_time  # 排班结束时间
    #     days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1
    #     time_days = []  # 排班显示时间
    #     for day in range(days):
    #         str_to_datetime = start_datetime + datetime.timedelta(days=day)
    #         time_days.append(str_to_datetime)
    #
    #     problem = Problem()
    #     # problem.addVariables(['[1,2,3]', '[4,5,6]'], [1, 2])
    #     # 构建排班
    #     # 此完全采用orm 效率会非常低
    #     if sheduling_arrange_order_ids:  # 有临时班组规则
    #         # 类型为班组
    #         for sheduling_arrange_order_id in sheduling_arrange_order_ids:
    #             arrange_class_type = sheduling_arrange_order_id.arrange_class_type  # 班次s
    #             arrange_class_obj = sheduling_arrange_order_id.arrange_class_obj  # 班组s
    #             arrange_order_groups = problem.addVariables([arrange_class.id for arrange_class in arrange_class_obj],
    #                                                         [arrange_class.id for arrange_class in
    #                                                          arrange_class_type])  # (['班组a id,班组b id,班组c id], [班次a id, 班次b id])
    #             # 班组要转换成对应的人
    #
    #             # for arrange_order_group in arrange_order_groups:
    #             #     for key in arrange_order_group:
    #             #         group_user_ids = self.env['funenc_xa_station.class_group'].browse(key).group_user_ids  # 班组成员
    #             #         for in
    #
    #
    #
    #
    #     else:  # 无临时排班规则
    #         # 类型为班组
    #         arrange_order_groups = problem.addVariables([arrange_class.id for arrange_class in class_group_ids],
    #                                                     [arrange_class.id for arrange_class in
    #                                                      arrange_order_ids])  # (['班组a id,班组b id,班组c id], [班次a id, 班次b id])
    #         # 班组要转换成对应的人
    #     if motorized_rule_ids:  # 机动人员规则
    #         # 类型为机动人员
    #         for motorized_rule_id in motorized_rule_ids:
    #             arrange_class_type = motorized_rule_id.arrange_class_type  # 班次s
    #             arrange_class_obj = motorized_rule_id.arrange_class_obj  # 班组s
    #             arrange_order_groups = problem.addVariables([arrange_class.id for arrange_class in arrange_class_obj],
    #                                                         [arrange_class.id for arrange_class in
    #                                                          arrange_class_type])  # (['班组a id,班组b id,班组c id], [班次a id, 班次b id])
    #             # 班组要转换成对应的人
    #
    #     else:  # 无临时机动人员规则
    #         # 类型为机动人员
    #         arrange_order_groups = problem.addVariables([arrange_class.id for arrange_class in motorized_user_ids],
    #                                                     [arrange_class.id for arrange_class in
    #                                                      motorized_ids])  # (['班组a id,班组b id,班组c id], [班次a id, 班次b id])
    #         # 班组要转换成对应的人
    #
    #     #  最后把构建的数据插入 模型 funenc_xa_station.sheduling_record
    #     # sheduling_date 排班日期为排班当天
    #     # 排班类型 sheduling_date order_type('order_group', '班组'), ('motorized_group', '机动人员')
    #
    #     show_data = self.get_sheuling_list(site_id, start_time, end_time)
    #
    #     return show_data

    @api.model
    def sheduling_start(self):
        line_id = self.line_id.id
        site_id = self.site_id.id
        conflict_rule_dics = self.env['funenc_xa_station.conflict_rule'].search_read([('site_id', '=', site_id),
                                                                                      ('conflict_rule_state', '=',
                                                                                       'enable'),
                                                                                      ('is_certificate', '=', 2)
                                                                                      ], ['save_conflict_rule'],
                                                                                     order='conflict_rule_index asc')
        class_interval = conflict_rule_dics[0].get('save_conflict_rule')  # 版与班之间的间隔 >= h
        rest_day = conflict_rule_dics[1].get('save_conflict_rule')  # 每人连续休息时间 <= d
        night_shift = conflict_rule_dics[2].get('save_conflict_rule')  # 第二天必须排休  1d

        show_position = self.line_id.name + '-' + self.site_id.name
        show_sheduling_time = self.show_sheduling_time
        show_arrange_order_name = self.show_arrange_order_name
        current_rule = self.current_rule
        sheduling_arrange_order_id = self.sheduling_arrange_order_id  # 班组人员规则规则
        motorized_rule_id = self.motorized_rule_id  # 机动规则规则

        class_group_ids = self.class_group_ids  # 班组
        arrange_order_ids = self.arrange_order_ids  # 班次
        motorized_user_ids = self.motorized_user_ids  # 机动人员
        motorized_ids = self.motorized_ids  # 机动人员班次

        start_time = self.sheduling_start_time  # 排班开始时间
        start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = self.sheduling_end_time  # 排班结束时间
        days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1
        time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = start_datetime + datetime.timedelta(days=day)
            time_days.append(str_to_datetime.strftime('%Y-%m-%d'))

        # problem.addVariables(['[1,2,3]', '[4,5,6]'], [1, 2])
        # 构建排班
        group_data = []
        motorized_data = []
        if sheduling_arrange_order_id:  # 有临时班组规则
            # 类型为班组
            tmp_class_order_ids = [order_to_arrange_id.arrange_order_id.id for order_to_arrange_id in
                                   sheduling_arrange_order_id.order_to_arrange_ids]  # 班次

            tmp_class_group_ids = class_group_ids  # 班组




        else:  # 无临时排班规则
            # 类型为班组
            tmp_class_order_ids = arrange_order_ids.ids  # 班次
            tmp_class_group_ids = class_group_ids  # 班组
        if tmp_class_order_ids and tmp_class_group_ids:
            for i, time_day in enumerate(time_days):  # 时间
                # tmp_class_order_ids  # 班次s
                iden_arrange_class_types = deepcopy(tmp_class_order_ids)
                # tmp_class_group_ids # 班组
                # 班组   (line_id,site_id,user_id,class_group_id,sheduling_date,order_type,work_time,arrange_order_id)
                for k, group_id in enumerate(tmp_class_group_ids):
                    for user_id in group_id.group_user_ids:
                        data = []
                        data.append(line_id)
                        data.append(site_id)
                        data.append(user_id.id)
                        data.append(group_id.id)
                        data.append(time_day)
                        data.append('order_group')
                        data.append(8)
                        data.append(tmp_class_order_ids[0])  # 班次
                        group_data.append(tuple(data))
                    tmp_class_order_ids = tmp_class_order_ids[1:] + [tmp_class_order_ids[0]]

                iden_arrange_class_types = iden_arrange_class_types[1:] + [
                    iden_arrange_class_types[0]]
                tmp_class_order_ids = iden_arrange_class_types

        if motorized_rule_id:  # 机动人员规则
            # 类型为机动人员

            tmp_class_motorized_ids = [order_to_arrange_id.arrange_order_id.id for order_to_arrange_id in
                                       motorized_rule_id.order_to_arrange_ids]  # 机动人员班次

            tmp_motorized_group_ids = motorized_user_ids.ids  # 机动人员

        else:  # 无临时机动人员规则

            tmp_class_motorized_ids = motorized_ids.ids  # 机动人员班次

            tmp_motorized_group_ids = motorized_user_ids.ids  # 机动人员

        if tmp_class_motorized_ids and tmp_motorized_group_ids:
            for i, time_day in enumerate(time_days):  # 时间
                iden_arrange_class_types = deepcopy(tmp_class_motorized_ids)
                for k, user_id in enumerate(tmp_motorized_group_ids):
                    data = []
                    data.append(line_id)
                    data.append(site_id)
                    data.append(user_id)
                    data.append(time_day)
                    data.append('motorized_group')
                    data.append(8)
                    data.append(tmp_class_motorized_ids[0])  # 班次
                    motorized_data.append(tuple(data))
                    tmp_class_motorized_ids = tmp_class_motorized_ids[1:] + [tmp_class_motorized_ids[0]]

                iden_arrange_class_types = iden_arrange_class_types[1:] + [
                    iden_arrange_class_types[0]]
                tmp_class_motorized_ids = iden_arrange_class_types

        if str(group_data)[1:-1]:
            insert_sql = "insert into funenc_xa_station_sheduling_record(line_id,site_id,user_id,class_group_id,sheduling_date,order_type,work_time,arrange_order_id)" \
                         "values{}".format(str(group_data)[1:-1])
            self.env.cr.execute(insert_sql)

        if str(motorized_data)[1:-1]:
            insert_sql = "insert into funenc_xa_station_sheduling_record(line_id,site_id,user_id,sheduling_date,order_type,work_time,arrange_order_id)" \
                         "values{}".format(str(motorized_data)[1:-1])
            self.env.cr.execute(insert_sql)

        show_data = self.get_sheuling_list(site_id, start_time, end_time)

        return show_data

    @api.model
    def get_cline_data(self, site_id, start_time):
        try:
            start_time = start_time[:10]
            loc_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d') + datetime.timedelta(hours=24)
            month = loc_datetime.strftime('%Y-%m-%d')
            year = month[:4]
            month1 = month[5:7]
            days = calendar.monthrange(int(year), int(month1))[1]
            end_time = year + '-{}'.format(month1) + '-{}'.format(days)

            data = self.get_sheuling_list_1(site_id, loc_datetime.strftime('%Y-%m-%d'), end_time)

            return data
        except Exception:

            return []

    def get_sheuling_list_1(self, site_id, start_time, end_time):
        '''
        统计  方法有点重复后面改
        :param site_id:
        :param start_time:
        :param end_time:
        :return:
    '''

        start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1

        show_data = {}
        show_time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = start_datetime + datetime.timedelta(days=day)
            datetime_to_str = str_to_datetime.strftime('%Y-%m-%d')[5:11]
            if datetime_to_str == '0':
                show_time_days.append(datetime_to_str[1:])
            else:
                show_time_days.append(datetime_to_str)

        show_data['days'] = show_time_days

        sel_groups = self.env['funenc_xa_station.sheduling_record'].search_read(
            [('site_id', '=', site_id), ('sheduling_date', '>=', start_time), ('sheduling_date', '<=', end_time)],
            order='sheduling_date asc')

        show_data['day_table_data'] = self.get_data_1(sel_groups)
        sheuling_datas = self.get_data(sel_groups)
        arrange_orders = self.env['funenc_xa_station.arrange_order'].search([('site_id', '=', site_id)], order='id asc')

        show_data['arrange_orders'] = [arrange_order.name for arrange_order in arrange_orders]
        # show_data['total_table_data'] =
        for sheuling_data in sheuling_datas:
            sheuling_data['total'] = []
            shift_value_ids = [obj.get('id') for obj in sheuling_data.get('shift_value')]
            for arrange_order in arrange_orders:
                sheuling_data['total'].append(shift_value_ids.count(arrange_order.id))
                # dic = {
                #     'id': arrange_order.id,  # 班次id
                #     'arrange_order_name': shift_value_ids.count(arrange_order.name),  # 班次名称
                #     'count': shift_value_ids.count(arrange_order.id)  # 班次 数量
                # }
                #
                # sheuling_data['total_table_data'].append(dic)
            show_data['total_table_data'] = sheuling_datas

        return show_data

    def total_group(self, groups, days):
        '''
        汇总统计
        :return:
        '''

        data = []
        group_ids = {}  # id为key去重
        for group in groups:
            group_ids[group.get('arrange_order_id')[0]] = group

        for group_id in group_ids.keys():
            compute_groups = []  # 同一班次数据
            for group_tmp in groups:
                if group_tmp.get('arrange_order_id')[0] == group_id:
                    group_tmp['sheduling_date'] = group_tmp['sheduling_date'][5:] if group_tmp[
                        'sheduling_date'] else '无'
                    compute_groups.append(group_tmp)

            # 构建排班统计数据
            if compute_groups:
                user_dic = {
                    'group_name': compute_groups[0].get('arrange_order_id')[1] if compute_groups[0].get(
                        'class_group_id') else '',
                    'shift_value': []
                }

                for day in days:

                    count = 0
                    for compute_group in compute_groups:
                        if compute_group.get('sheduling_date') == day:
                            count = count + 1
                    user_dic['shift_value'].append({
                        'user_number': count
                    })

            else:
                user_dic = {}

            data.append(user_dic)

        return data

    def get_sheuling_list(self, site_id, start_time, end_time):
        #  统计

        # days
        start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        days = (datetime.datetime.strptime(end_time, '%Y-%m-%d') - start_datetime).days + 1

        show_data = {}
        show_time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = start_datetime + datetime.timedelta(days=day)
            datetime_to_str = str_to_datetime.strftime('%Y-%m-%d')[5:11]
            if datetime_to_str == '0':
                show_time_days.append(datetime_to_str[1:])
            else:
                show_time_days.append(datetime_to_str)

        show_data['days'] = show_time_days

        #  数据太多不能循环用orm
        # 班组
        sel_groups = self.env['funenc_xa_station.sheduling_record'].search_read(
            [('site_id', '=', site_id), ('sheduling_date', '>=', start_time), ('sheduling_date', '<=', end_time),
             ('order_type', '=', 'order_group')], order='sheduling_date asc')

        show_data['group_table_data'] = self.get_data(sel_groups)

        # 机动
        motorizeds = self.env['funenc_xa_station.sheduling_record'].search_read(
            [('site_id', '=', site_id), ('sheduling_date', '>=', start_time), ('sheduling_date', '<=', end_time),
             ('order_type', '=', 'motorized_group')])
        show_data['motorized_group_table_data'] = self.get_data(motorizeds)
        show_data['total_group_table_data'] = self.total_group_table_data(sel_groups + motorizeds, show_time_days)

        shift_options = []

        arrange_orders = self.env['funenc_xa_station.arrange_order'].search_read([('site_id', '=', site_id)],
                                                                                 ['id', 'name'])
        for arrange_order in arrange_orders:
            tmp = {
                'id': arrange_order.get('id'),
                'label': arrange_order.get('name')
            }
            shift_options.append(tmp)

        show_data['shift_options'] = shift_options
        show_data['arrange_orders'] = arrange_orders

        return show_data

    def total_group_table_data(self, groups, days):
        '''
        统计班次次数
        :param groups:  参数需要按时间升序
        :return:
        '''
        data = []
        group_ids = {}  # id为key去重
        for group in groups:
            group_ids[group.get('arrange_order_id')[0]] = group

        for group_id in group_ids.keys():
            compute_groups = []  # 同一班次数据
            for group_tmp in groups:
                if group_tmp.get('arrange_order_id')[0] == group_id:
                    group_tmp['sheduling_date'] = group_tmp['sheduling_date'][5:] if group_tmp[
                        'sheduling_date'] else '无'
                    compute_groups.append(group_tmp)

            # 构建排班统计数据
            if compute_groups:
                user_dic = {
                    'group_name': compute_groups[0].get('arrange_order_id')[1] if compute_groups[0].get(
                        'class_group_id') else '无',
                    'shift_value': []
                }
                print()

                for day in days:

                    count = 0
                    for compute_group in compute_groups:
                        if compute_group.get('sheduling_date') == day:
                            count = count + 1
                    user_dic['shift_value'].append({
                        'user_number': count
                    })

            else:
                user_dic = {}

            data.append(user_dic)

        return data

    def get_data(self, group_data):
        '''
        获取排班
        :param group_data:
        :return:
        '''
        groups = group_data
        data = []
        group_user_ids = {}  # 去重
        for group in groups:
            group_user_ids[group.get('user_id')[0]] = group

        for user_id in group_user_ids.keys():
            compute_users = []  # 同一个人数据
            for group_tmp in groups:
                if group_tmp.get('user_id')[0] == user_id:
                    compute_users.append(group_tmp)

            # 构建排班个人数据
            if compute_users:
                user_dic = {
                    'user_name': compute_users[0].get('user_id')[1] if compute_users[0].get('user_id') else '',
                    'group_name': compute_users[0].get('class_group_id')[1] if compute_users[0].get(
                        'class_group_id') else '',
                    'work_number': compute_users[0].get('user_no'),
                    'position': compute_users[0].get('user_position'),
                    'shift_value': []
                }

                for compute_user in compute_users:
                    shift_value = {
                        'id': compute_user.get('arrange_order_id')[0] if compute_user.get('arrange_order_id') else '',
                        'shift': compute_user.get('arrange_order_id')[1] if compute_user.get(
                            'arrange_order_id') else '',
                        'sheduling_record_id': compute_user.get('id')
                    }
                    user_dic['shift_value'].append(shift_value)
            else:
                user_dic = {}

            data.append(user_dic)

        return data

    def get_data_1(self, group_data):
        '''
        获取排班
        :param group_data:
        :return:
        '''
        groups = group_data
        data = []
        group_user_ids = {}  # 去重
        for group in groups:
            group_user_ids[group.get('user_id')[0]] = group

        for user_id in group_user_ids.keys():
            compute_users = []  # 同一个人数据
            for group_tmp in groups:
                if group_tmp.get('user_id')[0] == user_id:
                    compute_users.append(group_tmp)

            # 构建排班个人数据
            if compute_users:
                user_dic = {
                    'user_name': compute_users[0].get('user_id')[1] if compute_users[0].get('user_id') else '',
                    'group_name': compute_users[0].get('class_group_id')[1] if compute_users[0].get(
                        'class_group_id') else '',
                    'work_number': compute_users[0].get('user_no'),
                    'position': compute_users[0].get('user_position'),
                    'shift_value': []
                }

                for compute_user in compute_users:
                    # shift_value = {
                    #     'shift': compute_user.get('arrange_order_id')[1] if compute_user.get(
                    #         'arrange_order_id') else '',
                    #     'sheduling_record_id': compute_user.get('id')
                    # }
                    shift_value = compute_user.get('arrange_order_id')[1] if compute_user.get(
                        'arrange_order_id') else ''
                    user_dic['shift_value'].append(shift_value)
            else:
                user_dic = {}

            data.append(user_dic)

        return data

    @api.model
    def save_change_data(self, **kw):
        try:

            sheduling_records = kw.get('kw').get('motorized_group_table_data') + kw.get('kw').get('group_table_data')
            for sheduling_record in sheduling_records:
                shift_values = sheduling_record.get('shift_value')
                for record in shift_values:
                    if isinstance(record.get('shift'), int):
                        self.env['funenc_xa_station.sheduling_record'].browse(
                            [int(record.get('sheduling_record_id'))]).write({
                            'arrange_order_id': int(record.get('shift'))
                        })
            return {'message': '\u4fdd\u5b58\u6210\u529f'}

        except Exception:
            return {'message': '保存失败'}


class ShedulingRecordr(models.Model):
    _name = 'funenc_xa_station.sheduling_record'
    _description = '排班记录'
    _inherit = 'fuenc_station.station_base'
    _order = 'id asc'

    class_group_id = fields.Many2one('funenc_xa_station.class_group', string='班组')
    arrange_order_id = fields.Many2one('funenc_xa_station.arrange_order', string='班次')
    time_interval = fields.Char(related='arrange_order_id.time', string='班次时间')
    sheduling_date = fields.Date(string='排班时间')
    order_type = fields.Selection(selection=[('order_group', '班组'), ('motorized_group', '机动人员')], string='班组类型')
    work_time = fields.Integer(string='工作时长')  # 工作时长

    #####
    user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='排班人员')
    user_name = fields.Char(related='user_id.name', string="名字")
    user_position = fields.Text(related='user_id.position', string="职位")
    user_no = fields.Char(related='user_id.jobnumber', string="工号")

    @api.model
    def get_sheduling_record_by_user(self, month):
        if month:
            year = month[:4]
            month1 = month[5:7]
            days = calendar.monthrange(int(year), int(month1))[1]
            select_date = year + '-{}'.format(month1) + '-{}'.format(days)

            ding_user = self.env.user.dingtalk_user
            search_read = self.search_read([('user_id', '=', ding_user.id), ('sheduling_date', '>=', month),
                                            ('sheduling_date', '<=', select_date)],
                                           ['sheduling_date', 'arrange_order_id', 'time_interval'])
            for search in search_read:
                search['arrange_order_id'] = search['arrange_order_id'][1]

            return search_read

    @api.model
    def get_sheduling_record_by_user_id(self, month, user_id):
        try:
            if month:
                year = month[:4]
                month1 = month[5:7]
                days = calendar.monthrange(int(year), int(month1))[1]
                select_date = year + '-{}'.format(month1) + '-{}'.format(days)

                # ding_user = self.env.user.dingtalk_user
                search_read = self.search_read([('user_id', '=', int(user_id)), ('sheduling_date', '>=', month),
                                                ('sheduling_date', '<=', select_date)],
                                               ['sheduling_date', 'arrange_order_id', 'time_interval', 'id'])
                for search in search_read:
                    search['arrange_order_id'] = search['arrange_order_id'][1]

                return search_read
        except Exception:
            return []

    @api.model
    def get_sheduling_object(self):
        if self.env.user.id == 1:
            return []
        else:
            ding_user = self.env.user.dingtalk_user
            department = ding_user.departments[0]
            data = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search_read([('departments', '=', department.id)],
                                                                               ['id', 'name', 'jobnumber', 'avatar',
                                                                                'position'])

            return data

    @api.model
    def get_sheduling_by_user_id(self, month, user_id):
        try:
            if month:
                year = month[:4]
                month1 = month[5:7]
                days = calendar.monthrange(int(year), int(month1))[1]
                select_date = year + '-{}'.format(month1) + '-{}'.format(days)

                # ding_user = self.env.user.dingtalk_user
                search_read = self.search_read([('user_id', '=', int(user_id)), ('sheduling_date', '>=', month),
                                                ('sheduling_date', '<=', select_date)],
                                               ['sheduling_date', 'arrange_order_id', 'time_interval', 'id'])
                for search in search_read:
                    search['arrange_order_id'] = search['arrange_order_id'][1]

                return search_read
        except Exception:
            return []

    @api.model
    def save_sheduling_record(self, **kw):
        try:
            self.create(kw)
            return True
        except Exception:
            return False
