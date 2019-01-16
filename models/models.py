# -*- coding: utf-8 -*-

from odoo import models, fields, api

import qrcode
import os
import base64
import datetime
import calendar
from .get_domain import *
import time

import json
import xlrd, xlwt
import logging
import requests
from .python_util import *

_logger = logging.getLogger(__name__)


class fuenc_station(models.Model):
    _name = 'fuenc_station.station_base'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点',
                              )
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路',
                              )

    product_id_domain = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=False,
    )

    product_site_id_domain = fields.Char(
        compute="_compute_product_site_id_domain",
        readonly=True,
        store=False,
    )

    @api.multi
    @api.depends('line_id')
    def _compute_product_site_id_domain(self):
        for rec in self:
            line_id = rec.line_id

            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments.ids
            child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', line_id.departmentId)]).ids
            site_domain = [('id', 'in', list(set(department_ids) & set(child_department_ids)))]

            rec.product_site_id_domain = json.dumps(
                site_domain
            )

    @get_line_id_domain
    @api.multi
    @api.depends('line_id')
    def _compute_product_id_domain(self, domain):
        for rec in self:
            rec.product_id_domain = json.dumps(
                domain
            )

    @get_line_id
    @get_line_id_domain
    @api.onchange('line_id')
    def change_line_id(self, domain, line_id):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments.ids
        #创建时触发
        if not self.line_id:
            if line_id:
                department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(line_id)
                child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', department.departmentId)]).ids
                site_ids = list(set(department_ids) & set(child_department_ids))
                return {
                    'domain': {'line_id': domain},
                    'value': {'line_id': line_id,
                              'site_id': site_ids[0] if site_ids else None
                              }
                }
            else:
                if self.user_has_groups('base.group_system'):
                    return {
                        'domain': {'line_id': [('department_hierarchy', '=', 2)],
                                   }
                    }
                return {
                    'domain': {'line_id': [('id', '<', 1)],
                               'site_id': [('id', '<', 1)]
                               },
                }
                # raise msg.Warning('此人员并无人员属性,请联系管理员在：权限设置/部门管理 下设置')

        # 根据人员属性过滤
        line_id = self.line_id

        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', line_id.departmentId)]).ids
        site_domain = [('id', 'in', list(set(department_ids) & set(child_department_ids)))]

        if self.user_has_groups('base.group_system'):
            return {'domain': {'site_id': [('id', 'in', child_department_ids)],
                               'line_id': [('department_hierarchy', '=', 2)]
                               }
                    }

        return {'domain': {'site_id': site_domain,
                           'line_id': domain
                           }
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
    arrange_order_id = fields.Many2one('funenc_xa_station.arrange_order', string='班次')
    time_length = fields.Float(related='arrange_order_id.save_work_time', string='计划时长(h)')
    clock_site = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='打卡站点')
    clock_start_time = fields.Datetime(string='上班打卡时间')
    clock_end_time = fields.Datetime(string='下班打卡时间')
    work_time = fields.Float(string='工作时长(h)')
    is_overtime = fields.Selection(selection=[('yes', '加班'), ('no', '正常')], default='no')
    overtime = fields.Float(string='加班时长')
    festival_overtime = fields.Float(string='节假日加班时长')
    is_leave = fields.Integer(string='是否是请假', default=0)  # 1为请假
    show_value = fields.Char(string='统计显示')  # 用于统计显示请假类型

    @api.onchange('clock_start_time','clock_end_time')
    def save_overtime(self):
        if self.clock_start_time and self.clock_end_time:
            work_time = get_time_difference_th(self.clock_start_time, self.clock_end_time)
            if work_time <= 12:
                return {
                    'value':{
                        'work_time': work_time
                    }
                }
            else:
                return {
                    'value': {
                        'work_time': 12,
                        'is_overtime':'yes',
                        'overtime':work_time - 12
                    }
                }

    def new_increate_record_button(self):
        view_tree = self.env.ref('funenc_xa_station.fuenc_station_overtime_record_form').id
        return {
            'name': '打卡记录',
            ''
            'type': 'ir.actions.act_window',
            'clear_breadcrumbs': True,
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_tree, "form"]],
            'res_model': 'fuenc_station.clock_record',
            'context': self.env.context,
            'target':'new',
        }

    @get_domain
    @api.model
    def xa_station_clock_list_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.fuenc_station_clock_record_list').id
        if self.env.user.id ==1:
            domain_id = []
        else:
            domain_id = [['user_id','=',self.env.user.dingtalk_user.id]]
        return {
            'name': '打卡记录',
            'type': 'ir.actions.act_window',
            'clear_breadcrumbs': True,
            'view_type': 'form',
            'view_mode': 'form',
            'binding_key': 'fuenc_station_clock_record_list',
            'domain':domain_id,
            "views": [[view_tree, "tree"]],
            'res_model': 'fuenc_station.clock_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                         [
                             {'title': '打卡记录',
                             'action':  'funenc_xa_station.xa_station_clock_list_action',
                             'group':'funenc_xa_station.table_card_record',
                             },
                             {
                                 'title': '加班记录',
                                 'action2' : 'funenc_xa_station.xa_station_overtime_list_action',
                                 'group' : 'funenc_xa_station.table_overtime_record',
                                 },
                             {
                                 'title': '请假记录',
                                 'action2':  'funenc_xa_station.xa_station_leave_list_action',
                                 'group' : 'funenc_xa_station.table_leave_record',
                                 },
                         ]
                     }''',
            'context': self.env.context,
        }

    @get_domain
    @api.model
    def xa_station_overtime_list_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.fuenc_station_overtime_record_list').id
        if self.env.user.id ==1:
            domain_id = [('work_time','>',0)]
        else:
            domain_id = [('user_id','=',self.env.user.dingtalk_user.id),('work_time','>',0)]
        return {
            'name': '加班记录',
            'type': 'ir.actions.act_window',
            'clear_breadcrumbs': True,
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain_id,
            "views": [[view_tree, "tree"]],
            'res_model': 'fuenc_station.clock_record',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                            [
                                {'title': '打卡记录',
                                'action':  'funenc_xa_station.xa_station_clock_list_action',
                                'group':'funenc_xa_station.table_card_record',
                                },
                                {
                                    'title': '加班记录',
                                    'action2' : 'funenc_xa_station.xa_station_overtime_list_action',
                                    'group' : 'funenc_xa_station.table_overtime_record',
                                    },
                                {
                                    'title': '请假记录',
                                    'action2':  'funenc_xa_station.xa_station_leave_list_action',
                                    'group' : 'funenc_xa_station.table_leave_record',
                                    },
                            ]
                        }''',
            'context': self.env.context,
        }


    @api.model
    def save_clock_record(self, **kw):
        site_id = kw.get('department_id')
        user_id = kw.get('user_id')

        if kw.get('type') == 'work':
            arrange_order_id = self.env['funenc_xa_station.sheduling_record'].sudo().search(
                [('site_id', '=', site_id),
                 ('user_id', '=', user_id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {
                # 'line_id': user_id.line_id.id,
                'site_id': site_id,
                'time': datetime.datetime.now(),
                'user_id': user_id,
                'arrange_order_id': arrange_order_id.id if arrange_order_id else None,
                'clock_site': site_id,
                'clock_start_time': datetime.datetime.now(),
                'is_overtime': 'no'
            }
            self.env['fuenc_station.clock_record'].sudo().create(values)

            return '上班打卡成功'

        else:
            clock_records = self.env['fuenc_station.clock_record'].sudo().search([('site_id', '=', site_id)],
                                                                                 order='id asc')
            lens = len(clock_records)
            if clock_records:
                clock_record = clock_records[lens - 1]
                if not clock_record.clock_start_time:
                    return '请先上班打卡'
                else:
                    clock_record.clock_end_time = datetime.datetime.now()
                    work_time = get_time_difference_th(clock_record.clock_start_time, clock_record.clock_end_time)
                    if work_time <= 12:
                        compute_work_time = work_time
                        clock_record.work_time = compute_work_time
                    else:
                        compute_work_time = 12
                        clock_record.work_time = compute_work_time
                        clock_record.is_overtime = 'yes'
                        clock_record.overtime = work_time - 12
                    if clock_record.clock_end_time[:10] == clock_record.clock_start_time[:10]:  # 上下班打卡为一天
                        flag = self.get_festival_and_holiday(clock_record.clock_end_time[:10])
                        if flag:
                            clock_record.festival_overtime = compute_work_time
                    else:  # 上下班打卡不为一天
                        morning_difference_th_1 = 0
                        morning_difference_th_2 = 0
                        if self.get_festival_and_holiday(clock_record.clock_start_time[:10]):
                            morning_difference_th_1 = to_morning_difference_th(clock_record.clock_end_time[:10])
                        if self.get_festival_and_holiday(clock_record.clock_end_time[:10]):
                            morning_difference_th_2 = today_morning_difference_th(clock_record.clock_end_time[:10])
                        clock_record.festival_overtime = morning_difference_th_1 + morning_difference_th_2

                    return '下班打卡成功'
            else:
                return '请先上班打卡'

    def get_festival_and_holiday(self, dtime):
        # 判断节假日 参数 date  返回数据：工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2
        url = "http://api.goseek.cn/Tools/holiday"  #
        # 2017-11-11
        str_date = dtime[:10]
        date = '{}{}{}'.format(str_date[:4], str_date[5:7], str_date[8:10])
        data = {
            'date': date
        }
        request = requests.get(url, data).json()
        if request.get('data') == 2:
            return True
        else:
            return False

    @api.model
    def create_clock_record(self):
        context = dict(self.env.context or {})
        return {
            'name': '创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fuenc_station.clock_record',
            'context': context,
            'target': 'new',
        }

    @api.model
    def get_clock_record_date(self):

        def_data = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].get_line_or_def_site()
        line_id = def_data.get('default_line')
        site_id = def_data.get('default_site')
        line_options = def_data.get('line_options')
        site_options = def_data.get('site_options')
        default_users = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].pc_get_users_by_department_id(site_id)
        default_data = self.get_clock_record(
            start_time=time.time() * 1000 - 2,
            line_id=line_id,
            site_id=site_id
        )

        return {'line_id': line_id, 'site_id': site_id, 'line_options': line_options, 'site_options': site_options,
                'default_users': default_users,
                'default_data': default_data
                }

    @api.model
    def get_clock_record(self, **kw):
        # try:
        #     pass
        # except Exception:
        #     return [] '%Y-%m-%d %H:%M:%S'
        current_time = time.time()
        start_time = kw.get('start_time')
        start_time_second = float(start_time) / 1000
        date_time = datetime.datetime.fromtimestamp(start_time_second)
        line_id = kw.get('line_id')
        site_id = kw.get('site_id')
        user_id = kw.get('user_id')

        loc_datetime = date_time + datetime.timedelta(hours=8)
        month = loc_datetime.strftime('%Y-%m-%d')
        year = month[:4]
        month1 = month[5:7]
        day = calendar.monthrange(int(year), int(month1))[1]
        end_time = year + '-{}'.format(month1) + '-{}'.format(day)
        start_month_str_time = year + '-{}'.format(month1) + '-01'
        start_month = datetime.datetime.strptime(start_month_str_time, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        # datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        end_month_second = time.mktime(end_datetime.timetuple())
        if (end_month_second + 24 * 60 * 60 - 1) >= current_time:
            end_datetime = datetime.datetime.fromtimestamp(current_time - 24 * 60 * 60)

        days = (end_datetime - start_month).days + 1

        show_time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = start_month + datetime.timedelta(days=day)
            datetime_to_str = str_to_datetime.strftime('%Y-%m-%d')[5:11]
            if datetime_to_str == '0':
                show_time_days.append(datetime_to_str[1:])
            else:
                show_time_days.append(datetime_to_str)

        show_data = {}
        show_data['days'] = show_time_days
        domain = [('id', '<', 1)]
        if line_id and site_id and user_id:
            domain = [('time', '>=', start_month_str_time), ('time', '<=', end_time), ('site_id', '=', site_id),
                      ('user_id', '=', user_id)]
        if line_id and site_id and not user_id:
            domain = [('time', '>=', start_month_str_time), ('time', '<=', end_time), ('site_id', '=', site_id)]
        if line_id and not site_id and not user_id:
            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments.ids
            if line_id in department_ids:
                domain = [('time', '>=', start_month_str_time), ('time', '<=', end_time), ('line_id', '=', line_id)]
            else:
                domain = [('id', '<', 1)]

        clock_records = self.search_read(domain)

        # 去重
        clock_record_ids = {}  # 以人物id为key构建的打卡记录
        for clock_record in clock_records:
            clock_record_ids[clock_record.get('user_id')[0]] = clock_record

        data = []
        count_data = []
        for key_user_id in clock_record_ids.keys():
            compute_users = []  # 同一个人数据
            for group_tmp in clock_records:
                if group_tmp.get('user_id')[0] == key_user_id:
                    compute_users.append(group_tmp)

            # 构建考勤个人数据
            if compute_users:
                user_dic = {
                    'user_name': compute_users[0].get('user_id')[1] if compute_users[0].get('user_id') else '',
                    'work_number': compute_users[0].get('user_no'),
                    'position': compute_users[0].get('user_position'),
                    # 'shift_value': []
                }

                for compute_user in compute_users:
                    #########
                    # 由于打卡日期可能不是连续的所以 以日期为key
                    str = compute_user.get('time')[5:11]
                    if str == '0':
                        str = str[1:]

                    # shift_value = {
                    #     str: compute_user.get('arrange_order_id')[1] if compute_user.get(
                    #         'arrange_order_id') else '',
                    # }
                    if compute_user.get('is_leave') == 1:
                        user_dic[str] = compute_user.get('show_value')
                    else:
                        user_dic[str] = compute_user.get('arrange_order_id')[1] + '({})'.format(
                            compute_user.get('work_time')) if compute_user.get(
                            'arrange_order_id') else ''
            else:
                user_dic = {}

            data.append(user_dic)

            # 统计

            if compute_users:

                count_dic = {
                    'user_name': compute_users[0].get('user_id')[1] if compute_users[0].get('user_id') else '',
                    'work_number': compute_users[0].get('user_no'),
                    'position': compute_users[0].get('user_position'),
                    'total_work_time': sum(compute_user.get('work_time') for compute_user in compute_users),
                    'night_work_time': [],  #
                }

                no_work = True
                for count_user in compute_users:
                    if count_user.get('is_leave') == 1:
                        no_work = False
                if no_work:
                    count_dic['no_work_time'] = '缺勤'
                else:
                    count_dic['no_work_time'] = 0

                work_time = 0
                add_work_time = 0
                sick_leave = 0  # 病假
                maternity_leave = 0  # 孕假
                compassionate_leave = 0  # 事件
                year_leave = 0  # 年假
                marry_leave = 0  # 婚假
                maternited_leave = 0  # 产假
                nursing_leave = 0  # 护理假
                funeral_leave = 0  # 丧假
                job_injury_leave = 0  # 工伤假
                absenteeism = 0  # 旷工
                for count_user in compute_users:
                    clock_start_time = count_user.get('clock_start_time')
                    clock_end_time = count_user.get('clock_end_time')

                    if clock_start_time and clock_end_time:

                        start_work_time = datetime.datetime.strptime(clock_start_time,
                                                                     '%Y-%m-%d %H:%M:%S')
                        end_work_time = datetime.datetime.strptime(clock_end_time,
                                                                   '%Y-%m-%d %H:%M:%S')

                        if (start_work_time - end_work_time).days < 0:
                            work_time = work_time + round((end_work_time - start_work_time).seconds / (60 * 60), 2)

                    add_work_time = add_work_time + int(count_user.get('festival_overtime'))  # 加班
                    # 请假
                    leave_id = self.env['funenc_xa_station.leave'].search_read([('leave_user_id', '=', key_user_id), (
                        'leave_start_time', '<=', count_user.get('time')), (
                                                                                    'leave_end_time', '>=',
                                                                                    count_user.get('time'))],
                                                                               ['leave_type'])
                    if leave_id:

                        if leave_id.get('leave_type') == 'sick_leave':
                            sick_leave = sick_leave + 1
                        elif leave_id.get('leave_type') == 'maternity_leave':
                            maternity_leave = maternity_leave + 1
                        elif leave_id.get('leave_type') == 'compassionate_leave':
                            compassionate_leave = compassionate_leave + 1
                        elif leave_id.get('leave_type') == 'annual_leave':
                            year_leave = year_leave + 1
                        elif leave_id.get('leave_type') == 'marital_leave':
                            marry_leave = marry_leave + 1
                        elif leave_id.get('leave_type') == 'maternity_eave_1':
                            maternited_leave = maternited_leave + 1
                        elif leave_id.get('leave_type') == 'nursing':
                            nursing_leave = nursing_leave + 1
                        elif leave_id.get('leave_type') == 'funeral_leave':
                            funeral_leave = funeral_leave + 1
                        elif leave_id.get('leave_type') == 'injury_leave':
                            job_injury_leave = job_injury_leave + 1
                        # elif leave_id.get('leave_type') == 'leave_office':
                        #     pass

                count_dic['night_work_time'] = work_time  # 夜班
                count_dic['sick_leave'] = add_work_time  # 加班
                count_dic['maternity_leave'] = maternity_leave
                count_dic['maternity_leave'] = maternity_leave
                count_dic['compassionate_leave'] = compassionate_leave
                count_dic['year_leave'] = year_leave
                count_dic['marry_leave'] = marry_leave
                count_dic['maternited_leave'] = maternited_leave
                count_dic['nursing_leave'] = nursing_leave
                count_dic['funeral_leave'] = funeral_leave
                count_dic['job_injury_leave'] = job_injury_leave
                count_dic['absenteeism'] = absenteeism
                count_dic['add_work_time'] = add_work_time



            else:
                count_dic = {}

            count_data.append(count_dic)

        show_data['attendance_table_data'] = data
        show_data['attendance_total_table_data'] = count_data

        return show_data

    # def _compute_work_time(self):
    #     for this in self:
    #         if this.clock_start_time:
    #             start_time = datetime.datetime.strptime(this.clock_start_time,
    #                                                     '%Y-%m-%d %H:%M:%S')
    #             if this.clock_end_time:
    #                 end_time = datetime.datetime.strptime(this.clock_end_time, '%Y-%m-%d %H:%M:%S')
    #                 work_time = round((end_time - start_time).seconds / (60 * 60), 2)
    #                 this.work_time = work_time if work_time <= 12 else 12
    #
    #                 if work_time > 12:
    #                     this.overtime = work_time - 12
    #                 else:
    #                     this.overtime = 0
    #             else:
    #                 this.work_time = 0

    @api.model
    def get_month_clock_record(self, month):
        if self.env.user != 1:
            year = month[:4]
            month1 = month[5:7]
            days = calendar.monthrange(int(year), int(month1))[1]
            select_date = year + '-{}'.format(month1) + '-{}'.format(days)
            ding_user = self.env.user.dingtalk_user
            # '&',
            # ('clock_end_time', '>=', month),
            # ('clock_end_time', '<=', select_date)
            clock_records = self.search_read(
                ['&', ('user_id', '=', ding_user.id),
                 '&',
                 ('clock_start_time', '>=', month),
                 ('clock_start_time', '<=', select_date),


                 ],
                ['id', 'line_id', 'site_id', 'clock_start_time', 'clock_end_time'])
        else:
            clock_records = self.search_read([], ['id', 'line_id', 'site_id', 'clock_start_time', 'clock_end_time'])

        data = []
        for clock_record in clock_records:
            dic = {}
            if clock_record.get('clock_start_time'):
                dic['clockType'] = '上班打卡'
                dic['id'] = clock_record.get('id')
                dic['time'] = get_add_8th_str_time(clock_record.get('clock_start_time')) if clock_record.get(
                    'clock_start_time') else ''
                dic['line_id'] = clock_record.get('line_id')[1] if clock_record.get('line_id') else ''
                dic['site_id'] = clock_record.get('site_id')[1] if clock_record.get('site_id') else ''
            data.append(dic)

        for clock_record in clock_records:
            dic1 = {}
            if clock_record.get('clock_end_time'):
                dic1['clockType'] = '下班打卡'
                dic1['id'] = clock_record.get('id')
                dic1['time'] = get_add_8th_str_time(clock_record.get('clock_end_time')) if clock_record.get(
                    'clock_end_time') else ''
                dic1['line_id'] = clock_record.get('line_id')[1] if clock_record.get('line_id') else ''
                dic1['site_id'] = clock_record.get('site_id')[1] if clock_record.get('site_id') else ''
                data.append(dic1)

        return data


class generate_qr(models.Model):
    '''
      生成二维码 用于上下班打卡
    '''
    name = fields.Char(string='', default="上下班二维码")
    _name = 'funenc_xa_station.generate_qr'
    _inherit = 'fuenc_station.station_base'
    work_qr = fields.Binary(string='上班二维码')
    off_work_qr = fields.Binary(string='下班二维码')
    add_date = fields.Date(string='今天二维码时间')

    def init_data(self):

        if self.env.user.has_group('base.group_system'):
            return

        start_time = time.time()
        ding_user = self.env.user.dingtalk_user[0]
        department_ids = ding_user.user_property_departments
        str_now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        site_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                site_ids.append(department_id.id)
        file = os.path.dirname(os.path.dirname(__file__))
        for site_id in site_ids:

            obj = self.search([('site_id', '=', site_id)])

            # department.id)
            work_add_data = {
                'model': 'fuenc_station.clock_record',
                'func': 'save_clock_record',
                'type': 'work',
                'department_id': site_id
            }
            work_file_name = file + "work_{}.png".format(str_now_date[:10])
            off_work_add_data = {
                'model': 'fuenc_station.clock_record',
                'func': 'save_clock_record',
                'type': 'off_work',
                'department_id': site_id
            }
            off_work_name = file + "off_work_{}.png".format(str_now_date[:10])

            if obj:

                if obj.add_date != str_now_date:
                    work_b64 = self.create_qrcode_1(work_add_data, work_file_name)

                    off_work_b64 = self.create_qrcode_1(off_work_add_data, off_work_name)
                    obj.sudo().write({

                        'work_qr': work_b64,
                        'off_work_qr': off_work_b64,
                        'add_date': datetime.datetime.now()

                    })

            else:

                work_b64 = self.create_qrcode_1(work_add_data, work_file_name)

                off_work_b64 = self.create_qrcode_1(off_work_add_data, off_work_name)

                department_obj = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(site_id)
                line_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=', department_obj.parentid)]).id

                self.sudo().create({
                    'work_qr': work_b64,
                    'off_work_qr': off_work_b64,
                    'add_date': datetime.datetime.now(),
                    'line_id': line_id,
                    'site_id': site_id,
                })
        end_time = time.time()
        print(end_time - start_time)
        lens = len(site_ids)
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_generate_qr_form').id
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_generate_qr_list').id
        if lens == 1:
            res_id = self.search([('site_id', '=', site_ids[0])]).id
            return {
                'name': '上下班打卡',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.generate_qr',
                'res_id': res_id,
                'target': 'current',
            }
        elif lens > 1:
            context['group_by'] = 'line_id'
            return {
                'name': '上下班打卡',
                'type': 'ir.actions.act_window',
                "views": [[view_tree, 'tree'], [view_form, "form"]],
                'res_model': 'funenc_xa_station.generate_qr',
                'target': 'current',
                'domain': [('site_id', 'in', site_ids)],
            }
        else:
            return
            # raise Warning('你未在 权限管理/部门管理 设置人员属性')

    def create_qrcode_1(self, add_data, file_name):

        '''
        二维码生成
        '''
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
        qr.add_data(add_data)
        img = qr.make_image()
        img.save(file_name)
        imgs = open(file_name, 'rb')
        datas = imgs.read()
        file_b64 = base64.b64encode(datas)
        imgs.close()
        os.remove(file_name)

        return file_b64


class inherit_department(models.Model):
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_department'
    count_user = fields.Integer(seting='人员数量', compute='_compute_count_user')

    department_property_users = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users',
                                                 'dingtalk_users_to_departments', 'department_id', 'ding_user_id',
                                                 string='人员属性部门')

    def station_detail(self):
        view_form = self.env.ref('funenc_xa_station.statio_summary_form').id
        res_id = self.env['funenc_xa_station.station_summary'].search([('site_id', '=', self.id)])
        site_users = self.department_property_users.ids
        dic = {
            'name': '车站详情',
            'type': 'ir.actions.act_window',
            'res_model': 'funenc_xa_station.station_summary',
            "views": [[view_form, "form"]],
            'context': self.env.context,
            'target': 'current',

        }
        if res_id:
            station_summary_id = res_id.read(['id'])[0].get('id')
            dic['res_id'] = station_summary_id

        else:
            line_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('departmentId', '=', self.parentid)]
            ).id
            obj = self.env['funenc_xa_station.station_summary'].create(
                {'line_id': line_id,
                 'site_id': self.id
                 }
            )
            station_summary_id = obj.read(['id'])[0].get('id')
            dic['res_id'] = station_summary_id

        # 车站人员
        sql_data = []
        for site_user_id in site_users:
            user_data = []  # (station_summary_id,ding_user_id)
            user_data.append(station_summary_id)
            user_data.append(site_user_id)
            sql_data.append(tuple(user_data))

        del_sql = "delete from station_summary_ding_user_rel_10_20 " \
                  "where station_summary_id = {}" \
            .format(station_summary_id)
        self.env.cr.execute(del_sql)
        if str(sql_data)[1:-1]:
            insert_sql = "insert into station_summary_ding_user_rel_10_20(station_summary_id,ding_user_id)" \
                         "values{}".format(str(sql_data)[1:-1])
            self.env.cr.execute(insert_sql)
        # end 车站人员

        return dic

    def _compute_count_user(self):
        for this in self:
            this.count_user = len(this.department_property_users.ids)

    @api.model
    def get_xa_departments(self):
        departments = self.sudo().search_read([], ['departmentId', 'name', 'parentid', 'department_hierarchy'])
        dic = {}
        dic['root_department'] = 1
        departments.append({
            'departmentId': 1,
            'name': '根部门',
            'parentid': 0
        })
        for department in departments:
            if department.get('department_hierarchy') == 1:
                department['parentid'] = 1
        dic['departments'] = departments

        return dic

    @api.model
    def get_users_by_department_id(self, departmentid):
        users = self.browse(departmentid).department_property_users.read(['id', 'jobnumber', 'name',
                                                                          'departments', 'avatar',
                                                                          'position'])
        # users = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].sudo().search_read([('department_property_users', '=', departmentid)]
        #                                                                            , ['id', 'jobnumber', 'name',
        #                                                                               'departments', 'avatar',
        #                                                                               'position'])
        for user in users:
            user['departmentId'] = user.get('departments')[0] if user.get('departments') else None

        return users

    @api.model
    def pc_get_users_by_department_id(self, site_id):
        try:
            users = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search_read(
                [('user_property_departments', '=', int(site_id))]
                , ['id', 'name'])

            return users
        except  Exception:
            return []

    @api.model
    def get_line_id(self):
        if self.env.user.id == 1:
            return self.search_read([('department_hierarchy', '=', 2)], ['id', 'name'])
        else:
            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments
            line_ids = []
            for department_id in department_ids:
                if department_id.department_hierarchy == 3:
                    obj = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId', '=', department_id.parentid)])

                    if {'id': obj.id, 'name': obj.name} not in line_ids:
                        line_ids.append({
                            'id': obj.id,
                            'name': obj.name
                        })

            return line_ids

    @api.model
    def get_line_or_def_site(self):
        '''
         获取 默认站点 线路 和站点线路下拉数据
        :return:  {'default_line': 默认线路,
                'site_options': 权限可见站点,
                'default_site': 默认站点,
                'line_options':权限可见线路,
                }
        '''
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        site_obj_ids = []
        line_obj_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                site_obj_ids.append(department_id)
                obj = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=', department_id.parentid)])
                if obj not in line_obj_ids:
                    line_obj_ids.append(obj)
        default_line = line_obj_ids[0] if line_obj_ids else None
        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', default_line.departmentId if default_line else None)])
        site_ids = list(set(department_ids) & set(child_department_ids))
        site_list_dic = []
        for site_id in site_ids:
            site_list_dic.append({
                'id': site_id.id,
                'name': site_id.name
            })

        default_site = site_list_dic[0].get('id') if site_list_dic else None
        line_ids = []
        for line_obj in line_obj_ids:
            line_ids.append(
                {'id': line_obj.id,
                 'name': line_obj.name
                 }
            )

        return {'default_line': default_line.id if default_line else '',
                'site_options': site_list_dic,
                'default_site': default_site,
                'line_options': line_ids,
                }

    @api.model
    def get_default_sheduling_data(self):
        default_line_data = self.get_line_or_def_site()
        start_time = datetime.datetime.now().strftime('%Y-%m-%d')
        start_time = '{}-01'.format(start_time[:7])
        year = start_time[:4]
        month1 = start_time[5:7]
        days = calendar.monthrange(int(year), int(month1))[1]
        end_time = year + '-{}'.format(month1) + '-{}'.format(days)
        default_data = self.env['funenc_xa_station.sheduling_manage'].get_sheuling_list_1(
            default_line_data.get('default_site'), start_time,
            end_time)

        return {'default_line': default_line_data.get('default_line'),
                'site_options': default_line_data.get('site_options'),
                'default_site': default_line_data.get('default_site'),
                'line_options': default_line_data.get('line_options'),
                'days': default_data.get('days', []),
                'day_table_data': default_data.get('day_table_data', []),
                'total_table_data': default_data.get('total_table_data', []),
                'arrange_orders': default_data.get('arrange_orders', []),
                }

    @api.model
    def get_sites(self, line_id):
        try:
            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments.ids
            department_id = self.browse(int(line_id)).departmentId

            child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department_id)]).ids
            site_domain = [('id', 'in', list(set(department_ids) & set(child_department_ids)))]

            return self.search_read(site_domain, ['id', 'name'])
        except Exception:
            return []

    @api.model
    def save_user_departments(self, user_ids, department_ids):
        # try:
        if department_ids and user_ids:
            # 设置部门
            ins_data = []
            for department_id in department_ids:
                for user_id in user_ids:
                    # ('department_id','user_id')
                    data = []
                    data.append(department_id)
                    data.append(user_id)
                    ins_data.append(tuple(data))

            if str(ins_data)[1:-1]:
                if len(user_ids) == 1:
                    del_sql = "delete from dingtalk_users_to_departments " \
                              "where ding_user_id = {}" \
                        .format(user_ids[0])
                    self.env.cr.execute(del_sql)
                else:
                    del_sql = "delete from dingtalk_users_to_departments " \
                              "where ding_user_id in {}" \
                        .format(tuple(user_ids))
                    self.env.cr.execute(del_sql)
                ins_sql = "insert into  dingtalk_users_to_departments(department_id,ding_user_id) " \
                          "values{}" \
                    .format(str(ins_data)[1:-1])
                self.env.cr.execute(ins_sql)

        if user_ids and not department_ids:
            # 清空部门
            ding_users = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].browse(user_ids)
            for ding_user in ding_users:
                ding_user.user_property_departments = False

        return '保存成功'

    # except Exception:
    #
    #     return '保存失败'


class UserInherit(models.Model):
    '''
    继承钉钉人员表,新增人员属性字段用于人员调动
    '''
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_users'

    user_property_departments = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_department',
                                                 'dingtalk_users_to_departments', 'ding_user_id', 'department_id',
                                                 string='人员属性部门')

    @api.model
    def get_user_settings_departments(self):

        department_tree = []

        # 客运部
        parent_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].sudo(1).search(
            [('department_hierarchy', '=', 1)])
        for parent_department_id in parent_department_ids:
            parent_department = {'label': parent_department_id.name}
            parent_department['id'] = parent_department_id.id

            # 中心部门
            gentral_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].sudo(1).search_read(
                [('parentid', '=', parent_department_id.departmentId)], ['parentid', 'name', 'id', 'departmentId'])
            child_departments = []
            for gentral_department_id in gentral_department_ids:
                department_map = {}
                department_map['label'] = gentral_department_id.get('name')
                department_map['id'] = gentral_department_id.get('id')

                gentral_department_department_id = gentral_department_id.get('departmentId')

                site_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].sudo(1).search_read(
                    [('parentid', '=', gentral_department_department_id)], ['parentid', 'name', 'id', 'departmentId'])
                # 站点部门
                site_department_list = []
                for site_department_id in site_department_ids:
                    site_department_map = {}
                    site_department_map['label'] = site_department_id.get('name')
                    site_department_map['id'] = site_department_id.get('id')
                    site_department_list.append(site_department_map)
                department_map['children'] = site_department_list
                child_departments.append(department_map)
            parent_department['children'] = child_departments
            department_tree.append(parent_department)

        return {'department_tree': department_tree
                }

    @api.model
    def get_user_by_name_or_no(self, name_or_no):
        '''
         根据姓名或者工号查询用户
        :return: 用户列表
        '''

        user_list = self.search(['|', ('name', 'ilike', name_or_no), ('jobnumber', 'ilike', name_or_no)])
        show_user_list = []
        for user in user_list:

            user_dic = {
                'id': user.id,
                'jobnumber': user.jobnumber,
                'name': user.name,
                'line_name': user.line_id.name if user.line_id else '',
                'branch_department': '',
                'department_name': user.department_name,
                'position': user.position,
                'tel': user.tel
            }

            if user.departments:
                # 分部
                department = user.departments[0]
                if department.department_hierarchy == 1:
                    user_dic['branch_department'] = department.name
                elif department.department_hierarchy == 1:
                    user_dic['branch_department'] = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId', '=', department.parentid)]).name
                else:
                    parent_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId', '=', department.parentid)])

                    user_dic['branch_department'] = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId', '=', parent_id.parentid)]).name

            else:
                user_dic['branch_department'] = ''

            show_user_list.append(user_dic)

        return show_user_list

    @api.model
    def get_user_property_by_user_id(self, user_id):
        user = self.browse(user_id)
        user_property_departments = user.user_property_departments.ids

        return user_property_departments


class ImportGroupUser(models.Model):
    _name = 'import_group_user'
    _description = '导入角色组成员'

    xls_file = fields.Binary('导入的xlsx文件')

    @api.model
    def create(self, vals):
        obj = super(ImportGroupUser, self).create(vals)

        return obj


    def save(self):
        '''
        导入职位角色组人员  没用try  让异常暴露出来
        :return:
        '''

        data = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))

        sheet_data = data.sheet_by_name(data.sheet_names()[0])
        sheet1 = data.sheet_by_index(0)
        if sheet_data:
            position_map = {
                '经理': self.env.ref('funenc_xa_station.module_position_manager_100'),
                '副经理': self.env.ref('funenc_xa_station.module_position_deputy_manager_102'),
                '人事管理助理': self.env.ref('funenc_xa_station.module_position_personnel_administration_assistant_103'),
                '运输管理助理': self.env.ref('funenc_xa_station.module_position_transport_administration_assistant_104'),
                '技术开发助理': self.env.ref('funenc_xa_station.module_position_technological development_assistant_106'),
                '综合管理助理': self.env.ref('funenc_xa_station.module_position_integrated_management_assistant_107'),
                '安全管理主办': self.env.ref('funenc_xa_station.module_position_security_administration_host_108'),
                '副主任': self.env.ref('funenc_xa_station.module_position_deputy_director_109'),
                '安全管理助理': self.env.ref('funenc_xa_station.module_position_security_administration_assistant_110'),
                '票务管理助理': self.env.ref('funenc_xa_station.module_position_security_ticketing_assistant_111'),
                '培训管理助理': self.env.ref('funenc_xa_station.module_position_training_management_assistant_112'),
                '值班站长': self.env.ref('funenc_xa_station.module_position_be_on_duty_site_114'),
                '站长': self.env.ref('funenc_xa_station.module_position_stationmaster_115'),
                '站长助理': self.env.ref('funenc_xa_station.module_position_stationmaster_assistant_116'),
                '站务员': self.env.ref('funenc_xa_station.module_position_depot_118'),
                '未定岗': self.env.ref('funenc_xa_station.module_position_undetermined_position_119'),
                '值班员': self.env.ref('funenc_xa_station.module_position_training_management_assistant_113'),
                '质量与计划管理主办': self.env.ref('funenc_xa_station.module_position_quality_host_120'),
                '副部长': self.env.ref('funenc_xa_station.position_undersecretary_121'),
                '主任': self.env.ref('funenc_xa_station.position_director_122'),
                '人事管理主办': self.env.ref('funenc_xa_station.position_personnel_matters_123'),
                '票务管理主办': self.env.ref('funenc_xa_station.position_ticket_business_host_124'),
                '服务管理助理': self.env.ref('funenc_xa_station.position_service_assistant_125'),
                '生产调度': self.env.ref('funenc_xa_station.position_dispatch_126'),
                '运输技术助理': self.env.ref('funenc_xa_station.position_general_manager_127'),
                '综合管理员': self.env.ref('funenc_xa_station.position_integrated_management_128'),
                '综合管助理': self.env.ref('funenc_xa_station.position_integrated_management_assistant_129'),
                '计划统计助理': self.env.ref('funenc_xa_station.position_statistics_assistant_130'),
                '党工团干事': self.env.ref('funenc_xa_station.position_party_secretary_131'),
                '综合管理主办': self.env.ref('funenc_xa_station.position_comprehensive_management_132'),

            }
            # 相同职位人员
            users_group = {
                self.env.ref('funenc_xa_station.module_position_manager_100').id: [],
                self.env.ref('funenc_xa_station.module_position_deputy_manager_102').id: [],
                self.env.ref('funenc_xa_station.module_position_personnel_administration_assistant_103').id: [],
                self.env.ref('funenc_xa_station.module_position_transport_administration_assistant_104').id: [],
                self.env.ref('funenc_xa_station.module_position_technological development_assistant_106').id: [],
                self.env.ref('funenc_xa_station.module_position_integrated_management_assistant_107').id: [],
                self.env.ref('funenc_xa_station.module_position_security_administration_host_108').id: [],
                self.env.ref('funenc_xa_station.module_position_deputy_director_109').id: [],
                self.env.ref('funenc_xa_station.module_position_security_administration_assistant_110').id: [],
                self.env.ref('funenc_xa_station.module_position_security_ticketing_assistant_111').id: [],
                self.env.ref('funenc_xa_station.module_position_training_management_assistant_112').id: [],
                self.env.ref('funenc_xa_station.module_position_be_on_duty_site_114').id: [],
                self.env.ref('funenc_xa_station.module_position_stationmaster_115').id: [],
                self.env.ref('funenc_xa_station.module_position_stationmaster_assistant_116').id: [],
                self.env.ref('funenc_xa_station.module_position_depot_118').id: [],
                self.env.ref('funenc_xa_station.module_position_undetermined_position_119').id: [],
                self.env.ref('funenc_xa_station.module_position_training_management_assistant_113').id: [],
                self.env.ref('funenc_xa_station.module_position_quality_host_120').id: [],
                self.env.ref('funenc_xa_station.position_undersecretary_121').id: [],
                self.env.ref('funenc_xa_station.position_director_122').id: [],
                self.env.ref('funenc_xa_station.position_personnel_matters_123').id: [],
                self.env.ref('funenc_xa_station.position_ticket_business_host_124').id: [],
                self.env.ref('funenc_xa_station.position_service_assistant_125').id: [],
                self.env.ref('funenc_xa_station.position_dispatch_126').id: [],
                self.env.ref('funenc_xa_station.position_general_manager_127').id: [],
                self.env.ref('funenc_xa_station.position_integrated_management_128').id: [],
                self.env.ref('funenc_xa_station.position_integrated_management_assistant_129').id: [],
                self.env.ref('funenc_xa_station.position_statistics_assistant_130').id: [],
                self.env.ref('funenc_xa_station.position_party_secretary_131').id: [],
                self.env.ref('funenc_xa_station.position_comprehensive_management_132').id: [],
            }

            lines = sheet_data.nrows
            import_fail_job_numbers = []
            for i in range(lines):
                if i > 0:
                    # 用来预设人员属性
                    line = sheet1.row_values(i)
                    job_number = line[1]  # 工号
                    ding_user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search(
                        [('jobnumber', '=', job_number)])
                    # res_user_id_loas = ding_user_id.id  # 获取角色的id
                    # res_line_id_load = line[5]  # 获取角色的部门
                    # no_res_line_id_load = ding_user_id.department_name  # 如果 excel 不存在部门就用之前的
                    # if res_user_id_loas:
                    #     res_line_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    #         [('name', '=', res_line_id_load)])
                    #     if res_line_name.id:
                    #         select_sql = 'select * from dingtalk_users_to_departments where ding_user_id={} ' \
                    #                      'and department_id={}'.format(res_user_id_loas, res_line_name.id)
                    #         cr = self._cr
                    #         cr.execute(select_sql)
                    #         record = cr.fetchall()
                    #         if not record:
                    #             ins_sql_load = "insert into dingtalk_users_to_departments(ding_user_id,department_id) " \
                    #                            "values({},{})" \
                    #                 .format(res_user_id_loas, res_line_name.id)
                    #             self.env.cr.execute(ins_sql_load)
                    #     else:
                    #         res_line_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    #             [('name', '=', line[5])])
                    #         if res_line_name:
                    #             res_line_name_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    #                 [('parentid', '=', res_line_name.departmentId)])
                    #             for i in res_line_name_ids.ids:
                    #
                    #                 select_sql = 'select * from dingtalk_users_to_departments where ding_user_id={} ' \
                    #                              'and department_id={}'.format(res_user_id_loas, i)
                    #                 cr = self._cr
                    #                 cr.execute(select_sql)
                    #                 record = cr.fetchall()
                    #                 if not record:
                    #                     ins_sql_load = "insert into dingtalk_users_to_departments(ding_user_id,department_id) " \
                    #                                    "values({},{})" \
                    #                         .format(res_user_id_loas, i)
                    #                     self.env.cr.execute(ins_sql_load)
                    res_user_id = ding_user_id.user.id
                    position = line[5]
                    self_position = position_map[position]
                    if res_user_id:

                        # 在规定组中添加不在删除
                        if res_user_id not in self_position.users.ids:
                            ins_sql = "insert into res_groups_users_rel(gid,uid) " \
                                      "values({},{})" \
                                .format(self_position.id, res_user_id)
                            self.env.cr.execute(ins_sql)
                        else:
                            tmp_groups = users_group.values()
                            del_sql  = "DELETE FROM res_groups_users_rel" \
                                      "where uid ={} and gid in {}".format(res_user_id,tuple(tmp_groups))
                            self.env.cr.execute(del_sql)

                        # self_position.users = [(6,0,[res_user_id])]

                    else:
                        import_fail_job_numbers.append((line[1], line[2], line[7]))
            _logger.info('import_fail_job_numbers={}'.format(import_fail_job_numbers))
            _logger.info('count={}'.format(len(import_fail_job_numbers)))
            print(users_group)
            for group_id in users_group:
                _logger.info('group_id={}'.format(group_id))
                if users_group[group_id]:
                    group = self.env['res.groups'].browse(group_id)
                    group.users = [(6,0,users_group[group_id])]
        self.unlink()

    # def save(self):
    #     '''
    #     导入职位角色组人员  没用try  让异常暴露出来
    #     :return:
    #     '''
    #
    #     data = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))
    #
    #     sheet_data = data.sheet_by_name(data.sheet_names()[0])
    #     sheet1 = data.sheet_by_index(0)
    #     if sheet_data:
    #         position_map = {
    #             '经理': self.env.ref('funenc_xa_station.module_position_manager_100'),
    #             '副经理': self.env.ref('funenc_xa_station.module_position_deputy_manager_102'),
    #             '人事管理助理': self.env.ref('funenc_xa_station.module_position_personnel_administration_assistant_103'),
    #             '运输管理助理': self.env.ref('funenc_xa_station.module_position_transport_administration_assistant_104'),
    #             '技术开发助理': self.env.ref('funenc_xa_station.module_position_technological development_assistant_106'),
    #             '综合管理助理': self.env.ref('funenc_xa_station.module_position_integrated_management_assistant_107'),
    #             '安全管理主办': self.env.ref('funenc_xa_station.module_position_security_administration_host_108'),
    #             '副主任': self.env.ref('funenc_xa_station.module_position_deputy_director_109'),
    #             '安全管理助理': self.env.ref('funenc_xa_station.module_position_security_administration_assistant_110'),
    #             '票务管理助理': self.env.ref('funenc_xa_station.module_position_security_ticketing_assistant_111'),
    #             '培训管理助理': self.env.ref('funenc_xa_station.module_position_training_management_assistant_112'),
    #             '值班站长': self.env.ref('funenc_xa_station.module_position_be_on_duty_site_114'),
    #             '站长': self.env.ref('funenc_xa_station.module_position_stationmaster_115'),
    #             '站长助理': self.env.ref('funenc_xa_station.module_position_stationmaster_assistant_116'),
    #             '站务员': self.env.ref('funenc_xa_station.module_position_depot_118'),
    #             '未定岗': self.env.ref('funenc_xa_station.module_position_undetermined_position_119'),
    #             '值班员': self.env.ref('funenc_xa_station.module_position_training_management_assistant_113'),
    #             '质量与计划管理主办': self.env.ref('funenc_xa_station.module_position_quality_host_120'),
    #             '副部长': self.env.ref('funenc_xa_station.position_undersecretary_121'),
    #             '主任': self.env.ref('funenc_xa_station.position_director_122'),
    #             '人事管理主办': self.env.ref('funenc_xa_station.position_personnel_matters_123'),
    #             '票务管理主办': self.env.ref('funenc_xa_station.position_ticket_business_host_124'),
    #             '服务管理助理': self.env.ref('funenc_xa_station.position_service_assistant_125'),
    #             '生产调度': self.env.ref('funenc_xa_station.position_dispatch_126'),
    #             '运输技术助理': self.env.ref('funenc_xa_station.position_general_manager_127'),
    #             '综合管理员': self.env.ref('funenc_xa_station.position_integrated_management_128'),
    #             '综合管助理': self.env.ref('funenc_xa_station.position_integrated_management_assistant_129'),
    #             '计划统计助理': self.env.ref('funenc_xa_station.position_statistics_assistant_130'),
    #             '党工团干事': self.env.ref('funenc_xa_station.position_party_secretary_131'),
    #             '综合管理主办': self.env.ref('funenc_xa_station.position_comprehensive_management_132'),
    #
    #         }
    #         # 相同职位人员
    #         users_group = {
    #             self.env.ref('funenc_xa_station.module_position_manager_100').id: [],
    #             self.env.ref('funenc_xa_station.module_position_deputy_manager_102').id: [],
    #             self.env.ref('funenc_xa_station.module_position_personnel_administration_assistant_103').id: [],
    #             self.env.ref('funenc_xa_station.module_position_transport_administration_assistant_104').id: [],
    #             self.env.ref('funenc_xa_station.module_position_technological development_assistant_106').id: [],
    #             self.env.ref('funenc_xa_station.module_position_integrated_management_assistant_107').id: [],
    #             self.env.ref('funenc_xa_station.module_position_security_administration_host_108').id: [],
    #             self.env.ref('funenc_xa_station.module_position_deputy_director_109').id: [],
    #             self.env.ref('funenc_xa_station.module_position_security_administration_assistant_110').id: [],
    #             self.env.ref('funenc_xa_station.module_position_security_ticketing_assistant_111').id: [],
    #             self.env.ref('funenc_xa_station.module_position_training_management_assistant_112').id: [],
    #             self.env.ref('funenc_xa_station.module_position_be_on_duty_site_114').id: [],
    #             self.env.ref('funenc_xa_station.module_position_stationmaster_115').id: [],
    #             self.env.ref('funenc_xa_station.module_position_stationmaster_assistant_116').id: [],
    #             self.env.ref('funenc_xa_station.module_position_depot_118').id: [],
    #             self.env.ref('funenc_xa_station.module_position_undetermined_position_119').id: [],
    #             self.env.ref('funenc_xa_station.module_position_training_management_assistant_113').id: [],
    #             self.env.ref('funenc_xa_station.module_position_quality_host_120').id: [],
    #             self.env.ref('funenc_xa_station.position_undersecretary_121').id: [],
    #             self.env.ref('funenc_xa_station.position_director_122').id: [],
    #             self.env.ref('funenc_xa_station.position_personnel_matters_123').id: [],
    #             self.env.ref('funenc_xa_station.position_ticket_business_host_124').id: [],
    #             self.env.ref('funenc_xa_station.position_service_assistant_125').id: [],
    #             self.env.ref('funenc_xa_station.position_dispatch_126').id: [],
    #             self.env.ref('funenc_xa_station.position_general_manager_127').id: [],
    #             self.env.ref('funenc_xa_station.position_integrated_management_128').id: [],
    #             self.env.ref('funenc_xa_station.position_integrated_management_assistant_129').id: [],
    #             self.env.ref('funenc_xa_station.position_statistics_assistant_130').id: [],
    #             self.env.ref('funenc_xa_station.position_party_secretary_131').id: [],
    #             self.env.ref('funenc_xa_station.position_comprehensive_management_132').id: [],
    #         }
    #
    #         lines = sheet_data.nrows
    #         import_fail_job_numbers = []
    #         for i in range(lines):
    #             if i > 0:
    #                 # 用来预设人员属性
    #                 line = sheet1.row_values(i)
    #                 job_number = '{}00{}'.format(line[1][0], line[1][1:])  # 工号
    #                 ding_user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search(
    #                     [('jobnumber', '=', job_number)])
    #                 res_user_id_loas = ding_user_id.id  # 获取角色的id
    #                 res_line_id_load = line[6]  # 获取角色的部门
    #                 no_res_line_id_load = ding_user_id.department_name  # 如果 excel 不存在部门就用之前的
    #                 if res_user_id_loas:
    #                     res_line_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
    #                         [('name', '=', res_line_id_load)])
    #                     if res_line_name.id:
    #                         select_sql = 'select * from dingtalk_users_to_departments where ding_user_id={} ' \
    #                                      'and department_id={}'.format(res_user_id_loas, res_line_name.id)
    #                         cr = self._cr
    #                         cr.execute(select_sql)
    #                         record = cr.fetchall()
    #                         if not record:
    #                             ins_sql_load = "insert into dingtalk_users_to_departments(ding_user_id,department_id) " \
    #                                            "values({},{})" \
    #                                 .format(res_user_id_loas, res_line_name.id)
    #                             self.env.cr.execute(ins_sql_load)
    #                     else:
    #                         res_line_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
    #                             [('name', '=', line[5])])
    #                         if res_line_name:
    #                             res_line_name_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
    #                                 [('parentid', '=', res_line_name.departmentId)])
    #                             for i in res_line_name_ids.ids:
    #
    #                                 select_sql = 'select * from dingtalk_users_to_departments where ding_user_id={} ' \
    #                                              'and department_id={}'.format(res_user_id_loas, i)
    #                                 cr = self._cr
    #                                 cr.execute(select_sql)
    #                                 record = cr.fetchall()
    #                                 if not record:
    #                                     ins_sql_load = "insert into dingtalk_users_to_departments(ding_user_id,department_id) " \
    #                                                    "values({},{})" \
    #                                         .format(res_user_id_loas, i)
    #                                     self.env.cr.execute(ins_sql_load)
    #                 res_user_id = ding_user_id.user.id
    #                 position = line[7]
    #                 self_position = position_map[position]
    #                 if res_user_id:
    #                     users_group[self_position.id].append(res_user_id)
    #                     if res_user_id not in self_position.users.ids:
    #                         ins_sql = "insert into res_groups_users_rel(gid,uid) " \
    #                                   "values({},{})" \
    #                             .format(self_position.id, res_user_id)
    #                         self.env.cr.execute(ins_sql)
    #                     self_position.users = [(6,0,[res_user_id])]
    #
    #                 else:
    #                     #
    #                     # print('gh=', line[1])
    #                     # print('user_name=', line[2])
    #                     # print('job_number=', job_number)
    #                     # print('res_user_id=', res_user_id)
    #                     # print('ding_user=', ding_user_id)
    #                     # print('职位=', position)
    #                     import_fail_job_numbers.append((line[1], line[2], line[7]))
    #         _logger.info('import_fail_job_numbers={}'.format(import_fail_job_numbers))
    #         _logger.info('count={}'.format(len(import_fail_job_numbers)))
    #         print(users_group)
    #         for group_id in users_group:
    #             _logger.info('group_id={}'.format(group_id))
    #             if users_group[group_id]:
    #                 group = self.env['res.groups'].browse(group_id)
    #                 group.users = [(6,0,users_group[group_id])]
    #         # 钉钉未设置人员
    #         # f = xlwt.Workbook()
    #         # sheet1 = f.add_sheet('钉钉未设置人员', cell_overwrite_ok=True)
    #         # row0 = ["工号", "姓名", "职位"]
    #         # for k in range(0, len(row0)):
    #         #     sheet1.write(0, k, row0[k])
    #         # for j,import_fail_job_number in enumerate(import_fail_job_numbers):
    #         #     for l,value in enumerate(import_fail_job_number):
    #         #         sheet1.write(j+1, l, value)
    #         #
    #         # f.save('二分部钉钉未设置人员.xls')
    #     self.unlink()

    # def download_save(self):
    #     data = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))
    #
    #     sheet_data = data.sheet_by_name(data.sheet_names()[0])
    #     sheet1 = data.sheet_by_index(0)
    #     if sheet_data:
    #         lines = sheet_data.nrows
    #         import_fail_job_numbers = []
    #         for i in range(40):
    #             if i > 0:
    #
    #                 line = sheet1.row_values(i)
    #                 job_number = '{}00{}'.format(line[1][0], line[1][1:])  # 工号
    #                 ding_user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search(
    #                     [('jobnumber', '=', job_number)])
    #                 res_user_id_loas = ding_user_id.id
    #                 res_line_id_load = ding_user_id.department_name
    #                 res_line_name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('name','=',res_line_id_load)])
    #                 if res_user_id_loas:
    #                     select_sql = 'select * from dingtalk_users_to_departments where ding_user_id={} ' \
    #                                  'and department_id={}'.format(res_user_id_loas,res_line_name.id)
    #                     cr = self._cr
    #                     cr.execute(select_sql)
    #                     record = cr.fetchall()
    #                     if not record:
    #                         ins_sql_load = "insert into dingtalk_users_to_departments(ding_user_id,department_id) " \
    #                                   "values({},{})" \
    #                             .format(res_user_id_loas, res_line_name.id)
    #                         self.env.cr.execute(ins_sql_load)
    #     self.unlink()
