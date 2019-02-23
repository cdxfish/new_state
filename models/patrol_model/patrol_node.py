# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime
from ast import literal_eval
import operator


class PatrolNode(models.Model):
    _name = 'funenc_xa_station.patrol_node'
    _description = '电子巡更'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'project_name'

    project_name = fields.Char(string='计划名称', required=True)
    create_name = fields.Char(string='创建人')
    create_time = fields.Datetime(string='创建时间')
    node_order = fields.Many2many('funenc_xa_station.patrol_node_setting', 'setting_node_ref', 'setting_id', 'node_id',
                                  string='节点顺序')
    participants = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'node_cdtct_ref', 'node_id', 'users_id',
                                    string='参会人员', required=True)
    check_cycle = fields.Char(string='检查周期', required=True, default='每天')
    check_start_time = fields.Datetime(string='检查开始时间', required=True)
    page_check_start_time = fields.Char(string='检查开始时间')
    check_end_time = fields.Datetime(string='检查结束时间', required=True)
    page_check_end_time = fields.Char(string='检查结束时间')
    state = fields.Selection([('normal', '正常'), ('stop', '停用')], string='状态', default='normal')
    node_record = fields.One2many('funenc_xa_station.patrol_node_record', 'record_data', string='巡更记录')

    @api.model
    def create(self, vals):
        create_new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
        create_new_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
        vals['create_time'] = create_new_time
        user_id = vals['participants'][0][-1]  # 人员id
        lis = []
        patrol_record_details = []
        record = super(PatrolNode, self).create(vals)
        str_start = record.check_start_time  # 开始时间转化成为时分秒
        time_8 = datetime.datetime.strptime(str_start, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)  # 加上8个小时的时间
        page_8_time_start = datetime.datetime.strftime(time_8, '%Y-%m-%d %H:%M:%S')
        record.page_check_start_time = page_8_time_start[-8:]
        str_end = record.check_end_time  # 结束时间转化成为时分秒
        time_8 = datetime.datetime.strptime(str_end, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)  # 加上8个小时的时间
        page_8_time_end = datetime.datetime.strftime(time_8, '%Y-%m-%d %H:%M:%S')
        record.page_check_end_time = page_8_time_end[-8:]
        for user in user_id:
            neme = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].browse(user).id
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            lis.append((0, 0, {
                'date': create_new_date,
                'name': neme,
                'start_time': page_8_time_start[-8:],
                'end_time': page_8_time_end[-8:],
            }))
        for details in record.node_order:
            patrol_record_details.append((0, 0, {
                'name': neme,
                'node_name': details.node_name,
                'qr_image': details.qr_code,
            }))
        record.node_record = lis
        for i in record.node_record:
            i.patrol_record_details = patrol_record_details

        record.create_name = self.env.user.dingtalk_user.name
        return record

    # 新增节点
    def new_increate_node(self):
        return {
            'name': '创建计划',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.patrol_node',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    # 启动计划
    def start_project(self):
        self.state = 'normal'

    # 停用计划
    def stop_project(self):
        self.state = 'stop'

    # 计划详情
    def detailed_record(self):
        form_tree = self.env.ref('funenc_xa_station.patrol_node_from_record').id
        date = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        for i in self.node_record:
            loacl_day_time = i.date + ' ' + i.end_time  # 当天操作的最后时间
            if loacl_day_time < date:  # 延时
                i.state = 'delay'

        return {
            'name': '详情',
            'type': 'ir.actions.act_window',
            "views": [[form_tree, "form"]],
            'res_id': self.id,
            'res_model': 'funenc_xa_station.patrol_node',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
        }

    # 查看二维码的详情
    def search_qr_details(self):
        form_tree = self.env.ref('funenc_xa_station.patrol_node_setting_from_search_qr').id
        return {
            'name': '二维码',
            'type': 'ir.actions.act_window',
            "views": [[form_tree, "form"]],
            'res_model': 'funenc_xa_station.patrol_node_setting',
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'context': self.env.context,
            'target': 'new',
        }

    # 获取数据保存
    @api.model
    def save_rec(self, **kw):
        lis = []
        name = self.env.user.dingtalk_user.name
        name_id = self.env.user.dingtalk_user.id
        name_card = self.env.user.dingtalk_user.jobnumber
        record = self.search([('participants', '=', name_id)])
        for i in record:
            for rec in i.node_record:
                if rec.state:
                    if rec.state == 'ongoing':
                        state = '进行中'
                    elif rec.state == 'complete':
                        state = '完成'
                i_rec = {
                    'id': i.id,
                    'project_name': i.project_name,
                    'state': state,
                    'check_start_time': i.page_check_start_time,
                    'check_end_time': i.page_check_end_time,
                    'date': rec.date,
                    'last_time': i.write_date
                }
                lis.append(i_rec)
        return sorted(lis, key=operator.itemgetter('last_time'), reverse=True)

    # 节点接口
    @api.model
    def save_rec_node(self, **kw):
        lis = []
        self_record = self.search([('id', '=', kw.get('id'))])
        for i in self_record.node_record.patrol_record_details:
            rec_state = i.state
            if rec_state:
                if rec_state == 'nocomplete':
                    state = '未完成'
                elif rec_state == 'complete':
                    state = '已完成'
            value = {
                'self_id': i.id,
                'node_name': i.node_name,
                'state': state,
                'time': i.patrol_time,
            }
            lis.append(value)
        return lis


class PatrolNodeRecord(models.Model):
    _name = 'funenc_xa_station.patrol_node_record'
    _description = '变更记录'

    date = fields.Date(string='日期')
    name = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='姓名')
    start_time = fields.Char(string='开始巡更时间')
    end_time = fields.Char(string='结束巡更时间')
    state = fields.Selection([('complete', '完成'), ('ongoing', '进行中'), ('delay', '延误')], string='状态', default='ongoing')
    record_data = fields.Many2one('funenc_xa_station.patrol_node')
    patrol_record_details = fields.One2many('funenc_xa_station.patrol_record_details', 'patrol_rec')

    def detailed_record(self):
        form_tree = self.env.ref('funenc_xa_station.patrol_node_tree_information_search_qr').id
        return {
            'name': '巡更记录详情',
            'type': 'ir.actions.act_window',
            "views": [[form_tree, "tree"]],
            'res_model': 'funenc_xa_station.patrol_record_details',
            'flags': {'initial_mode': 'readonly'},
            'context': self.env.context,
            'domain': [('id', 'in', self.patrol_record_details.ids)],
        }

    # 定时任务
    @api.model
    def update_patrol_time(self):
        create_new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
        all_record = self.env['funenc_xa_station.patrol_node'].search([])
        for rec in all_record:
            lis = []
            for node in rec.participants:
                # 创建巡更记录详情
                patrol_record_details = []  # 用来存放详情的节点内容
                for details in rec.node_order:
                    patrol_record_details.append((0, 0, {
                        'name': node.id,
                        'node_name': details.node_name,
                    }))
                lis.append((0, 0, {
                    'date': create_new_time,
                    'name': node.id,
                    'start_time': rec.page_check_start_time,
                    'end_time': rec.page_check_end_time,
                    'patrol_record_details': patrol_record_details,
                }))  # 新巡更人的巡更记录
            rec.node_record = lis


class PatrolRecordDeteils(models.Model):
    _name = 'funenc_xa_station.patrol_record_details'
    _description = '巡更记录详情'
    _rec_name = 'node_name'

    name = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='姓名')
    node_name = fields.Char(string='节点名称')
    patrol_time = fields.Datetime(string='巡测时间')
    qr_image = fields.Binary(string='二维码图片')
    patrol_rec = fields.Many2one('funenc_xa_station.patrol_node_record')
    desc = fields.Char(string='描述')
    load_file_test = fields.One2many('video_voice_model', 'patrol_node_imange', string='图片上传',
                                     track_visibility='onchange')
    imgs = fields.Char('照片路径')  # 存的字典  自己转
    nodeid = fields.Integer(string='节点的id')
    state = fields.Selection([('complete', '已完成'), ('nocomplete', '未完成')], string='状态', default='nocomplete')

    def search_qr_code(self):
        form_tree = self.env.ref('funenc_xa_station.search_patrol_image_node_from').id
        return {
            'name': '巡更记录详情-巡察情况',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[form_tree, "form"]],
            'res_model': 'funenc_xa_station.patrol_record_details',
            'flags': {'initial_mode': 'readonly'},
            'context': self.env.context,
            'res_id': self.id,
            'target': 'new',
        }

    # 巡更记录详情接口
    @api.model
    def qr_get_data(self, **kwargs):
        date = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            record = self.search([('id', '=', kwargs.get('id'))])
            record.patrol_time = date
            return 'true'
        except Exception as err:
            return 'err'

    # 巡更记录巡察情况
    @api.model
    def patrol_state_image(self, **value):
        imgs = literal_eval(value.get('imgs'))
        for img in imgs:
            self.env['video_voice_model'].create({
                'patrol_node_imange': value.get('nodeid'),
                'url': img['url']
            })
        rec_loacl = self.search([('id', '=', value.get('nodeid'))])
        rec_loacl.state = 'complete'  # 修改他的状态
        rec_loacl.desc = value.get('desc')  # 获取描述
        rec_loacl.node_name = value.get('qrname')  # 获取节点名称
        up_id = rec_loacl.patrol_rec
        all_rec = up_id.patrol_record_details  # 找出当前记录下面所有的节点
        lis_state = []  # 储存状态
        for i in all_rec:
            state_lower = i.state  # 当前记录下面的状态
            if state_lower == 'nocomplete':
                lis_state.append(state_lower)
        if len(lis_state) == 0:
            up_id.state = 'complete'
        return True

    # 接口完成记录
    @api.model
    def complete_record(self, **kwargs):
        self_record = self.search([('id', '=', kwargs.get('id'))])
        image = self_record.load_file_test
        lis = []
        if image:
            for i in image:  # 获取图片的url
                lis.append({'url': i.url})
        return {
            'name': self_record.node_name,
            'desc': self_record.desc,
            'imgs': lis,
            'check_time': self_record.patrol_time
        }
