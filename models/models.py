# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.exceptions as msg
import qrcode
from PIL import Image
import os
import base64
from odoo import http
import socket, datetime
import calendar


class fuenc_station(models.Model):
    _name = 'fuenc_station.station_base'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点',
                              default=lambda self: self.default_site_id())
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路',
                              default=lambda self: self.default_line_id())

    @api.model
    def default_line_id(self):
        if self.env.user.id == 1:
            return

        return self.env.user.dingtalk_user.line_id.id

    @api.model
    def default_site_id(self):
        if self.env.user.id == 1:
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
                sql = 'update {} set site_id = {}, line_id = {} where id = {}'.format(model, site_id, line_id, self.id)
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
    arrange_order_id = fields.Many2one('funenc_xa_station2.arrange_order', string='班次')
    time_length = fields.Float(related='arrange_order_id.save_work_time', string='计划时长(h)')
    clock_site = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='打卡站点')
    clock_start_time = fields.Datetime(string='上班打卡时间')
    clock_end_time = fields.Datetime(string='下班打卡时间')
    work_time = fields.Float(string='工作时长(h)', compute='_compute_work_time', store=True)
    is_overtime = fields.Selection(selection=[('yes', '加班'), ('no', '正常')], default='no')
    overtime = fields.Float(string='加班时长', compute='_compute_work_time', store=True)
    festival_overtime = fields.Float(string='节假日加班时长')
    is_leave = fields.Integer(string='是否是请假', default=0)  # 1为请假
    show_value = fields.Char(string='统计显示')  # 用于统计显示请假类型

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
    def get_clock_record(self, start_time, site_id, user_id):
        # try:
        #     pass
        # except Exception:
        #     return []
        start_time = start_time[:10]
        loc_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%d') + datetime.timedelta(hours=24)
        month = loc_datetime.strftime('%Y-%m-%d')
        year = month[:4]
        month1 = month[5:7]
        day = calendar.monthrange(int(year), int(month1))[1]
        end_time = year + '-{}'.format(month1) + '-{}'.format(day)
        end_datetime = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        # datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        days = (end_datetime - loc_datetime).days + 1

        show_time_days = []  # 排班显示时间
        for day in range(days):
            str_to_datetime = loc_datetime + datetime.timedelta(days=day)
            datetime_to_str = str_to_datetime.strftime('%Y-%m-%d')[5:11]
            if datetime_to_str == '0':
                show_time_days.append(datetime_to_str[1:])
            else:
                show_time_days.append(datetime_to_str)

        show_data = {}
        show_data['days'] = show_time_days

        if user_id:
            clock_records = self.search_read(
                [('time', '>=', start_time), ('time', '<=', end_time), ('site_id', '=', site_id),
                 ('user_id', '=', user_id)])
        else:
            clock_records = self.search_read(
                [('time', '>=', start_time), ('time', '<=', end_time), ('site_id', '=', site_id)])

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
                sick_leave = 0 # 病假
                maternity_leave = 0  # 孕假
                compassionate_leave = 0 # 事件
                year_leave = 0 # 年假
                marry_leave = 0 # 婚假
                maternited_leave = 0 # 产假
                nursing_leave = 0 # 护理假
                funeral_leave = 0 # 丧假
                job_injury_leave = 0 # 工伤假
                absenteeism = 0 # 旷工
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
                    leave_id = self.env['funenc_xa_station2.leave'].search_read([('leave_user_id', '=', key_user_id), (
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
                            maternited_leave = maternited_leave +1
                        elif leave_id.get('leave_type') == 'nursing':
                            nursing_leave = nursing_leave + 1
                        elif leave_id.get('leave_type') == 'funeral_leave':
                            funeral_leave = funeral_leave + 1
                        elif leave_id.get('leave_type') == 'injury_leave':
                            job_injury_leave =  job_injury_leave + 1
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

    def _compute_work_time(self):
        for this in self:
            if this.clock_start_time:
                start_time = datetime.datetime.strptime(this.clock_start_time,
                                                        '%Y-%m-%d %H:%M:%S')
                if this.clock_end_time:
                    end_time = datetime.datetime.strptime(this.clock_end_time, '%Y-%m-%d %H:%M:%S')
                    work_time = round((end_time - start_time).seconds / (60 * 60), 2)
                    this.work_time = work_time if work_time <= 12 else 12

                    if work_time > 12:
                        this.overtime = work_time - 12
                    else:
                        this.overtime = 0
                else:
                    this.work_time = 0

    @api.model
    def get_month_clock_record(self, month):
        if self.env.user != 1:
            year = month[:4]
            month1 = month[5:7]
            days = calendar.monthrange(int(year), int(month1))[1]
            select_date = year + '-{}'.format(month1) + '-{}'.format(days)
            ding_user = self.env.user.dingtalk_user
            clock_records = self.search_read(
                ['|', ('user_id', '=', ding_user.id),
                 '&',
                 ('clock_start_time', '>=', month),
                 ('clock_start_time', '<=', select_date),
                 '&',
                 ('clock_start_time', '>=', month),
                 ('clock_start_time', '<=', select_date)

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
                dic['time'] = clock_record.get('clock_start_time')
                dic['line_id'] = clock_record.get('line_id')[1]
                dic['site_id'] = clock_record.get('site_id')[1]
            data.append(dic)

        for clock_record in clock_records:
            dic1 = {}
            if clock_record.get('clock_end_time'):
                dic1['clockType'] = '下班打卡'
                dic1['id'] = clock_record.get('id')
                dic1['time'] = clock_record.get('clock_end_time')
                dic1['line_id'] = clock_record.get('line_id')[1]
                dic1['site_id'] = clock_record.get('site_id')[1]
            data.append(dic1)

        return data


class generate_qr(models.Model):
    '''
      生成二维码 用于上下班打卡
    '''
    _name = 'funenc_xa_station2.generate_qr'
    work_qr = fields.Binary(string='上班二维码')
    off_work_qr = fields.Binary(string='下班二维码')

    def init_data(self):
        self.create_qrcode()
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station2.funenc_xa_station_generate_qr_list').id
        if self.env.user.has_group('funenc_xa_station2.system_fuenc_site'):
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            context['work_qr'] = '/funenc_xa_station2/static/images/work_{}.png'.format(department.id)
            context['off_work_qr'] = '/funenc_xa_station2/static/images/off_work_{}.png'.format(department.id)
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
        if self.env.user.id == 1:
            return
        else:
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            file = os.path.dirname(os.path.dirname(__file__))
            if department.department_hierarchy == 3:
                # 获取本机计算机名称
                hostname = socket.gethostname()
                # 获取本机ip
                ip = socket.gethostbyname(hostname)
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10,
                                   border=4, )
                qr.add_data('http://{}:8069/funenc_xa_station2/check_collect/'.format(ip))
                print('http://{}/fuenc_station/index/'.format(ip))
                img = qr.make_image()
                file_name = file + "/static/images/work_{}.png".format(department.id)
                img.save(file_name)
                obj = self.create({'work_qr': file_name})
                file_name = file + "/static/images/off_work_{}.png".format(department.id)
                qr.add_data('http://{}:8069//funenc_xa_station2/off_work/'.format(ip))
                img.save(file_name)
                obj.update({'off_work_qr': file_name})


# def create_qrcode_1():
#         '''
#         二维码生成
#         :param filename:
#         :return:
#         '''
#
#         # 获取本机计算机名称
#         hostname = socket.gethostname()
#         # 获取本机ip
#         ip = socket.gethostbyname(hostname)
#         qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
#         qr.add_data('http://{}:8069/funenc_xa_station2/check_collect/'.format(ip))
#         print('http://{}/fuenc_station/index/'.format(ip))
#         img = qr.make_image()
#         img.save("../static/images/advanceduse.png")
# create_qrcode_1()

class inherit_department(models.Model):
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_department'

    @api.model
    def get_xa_departments(self):
        departments = self.sudo().search_read([], ['departmentId', 'name', 'parentid'])
        dic = {}
        dic['departments'] = departments
        dic['root_department'] = self.search_read([('department_hierarchy', '=', 1)],
                                                  ['departmentId', 'name', 'parentid'])[0].get('departmentId')

        return dic

    @api.model
    def get_users_by_department_id(self, departmentid):
        users = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search_read([('departments', '=', departmentid)]
                                                                                   , ['id', 'jobnumber', 'name',
                                                                                      'departments', 'avatar',
                                                                                      'position'])
        for user in users:
            user['departmentId'] = user.get('departments')[0]

        return users

    @api.model
    def pc_get_users_by_department_id(self, site_id):
        try:
            users = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search_read(
                [('departments', '=', int(site_id))]
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
            department = ding_user.departments[0]
            if department.department_hierarchy == 1:
                return self.search_read([('department_hierarchy', '=', 2)], ['id', 'name'])
            elif department.department_hierarchy == 2:

                return [{'id': department.id, 'name': department.name}]
            else:
                return self.search_read([('departmentId', '=', department.parentid)],
                                        ['id', 'name'])

    # @api.model
    # def get_sites(self, line_id):
    #     if self.env.user.id == 1:
    #         return self.search_read([('department_hierarchy', '=', 3)], ['id', 'name'])
    #     else:
    #         ding_user = self.env.user.dingtalk_user
    #         department = ding_user.departments[0]
    #
    #         if department.department_hierarchy == 1 or department.department_hierarchy == 2:
    #             department_id = self.browse(line_id).departmentId
    #             return self.search_read([('parentid', '=', department_id)], ['id', 'name'])
    #         else:
    #             return [{'id': ding_user.departments[0].id, 'name': ding_user.department_name}]

    @api.model
    def get_sites(self, line_id):
        try:
            department_id = self.browse(int(line_id)).departmentId
            return self.search_read([('parentid', '=', department_id)], ['id', 'name'])
        except Exception:
            return []
