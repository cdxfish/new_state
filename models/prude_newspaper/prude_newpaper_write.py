# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions
import datetime
from ..get_domain import get_domain
from odoo.exceptions import ValidationError


key = [('enter_come', '边门进出情况')
    , ('ticket_acf', '票务、AFC故障及异常情况')
    , ('ticket_sales', '日票、预制单程票售卖情况')
    , ('other_brenk', '其他设备故障情况')
    , ('normal', '普通事件')]

class PrudeNewpaperWrite(models.Model):
    _name = 'funenc_xa_staion.prude_newpaper_write'
    _inherit = ['fuenc_station.station_base','mail.thread','mail.activity.mixin']
    _rec_name = 'event_stype'
    _description = '生产日报事件类型'


    event_stype = fields.Many2one('funenc_xa_station.prude_newpaper_type',string='事件类型',required=True,track_visibility='onchange')
    event_stype_name = fields.Char(compute='_compute_event_stype_name',track_visibility='onchange')
    event_content = fields.Text(string='事件内容',compute='_event_content',store=True,track_visibility='onchange')
    event_content_create = fields.Text(string='事件内容',track_visibility='onchange')
    open_time = fields.Datetime(string='发生时间',track_visibility='onchange')
    write_time = fields.Datetime(string='填报时间',dafault=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),track_visibility='onchange')
    write_name = fields.Char(string='填报人',default=lambda self: self.default_person_id(),track_visibility='onchange')
    iobnumber = fields.Char(string='工号',default=lambda self: self.default_jobnumber_id(),track_visibility='onchange')
    Enter_person_count =fields.Integer(string='进边门人数',track_visibility='onchange')
    come_person_count = fields.Integer(string='出边门人数',track_visibility='onchange')
    two_money =fields.Char(string='2元',track_visibility='onchange')
    three_money = fields.Char(string='3元',track_visibility='onchange')
    four_money = fields.Char(string='4元',track_visibility='onchange')
    five_money =fields.Char(string='5元',track_visibility='onchange')
    six_money =fields.Char(string='6元',track_visibility='onchange')
    seven_money = fields.Char(string='7元',track_visibility='onchange')
    eight_money = fields.Char(string='8元',track_visibility='onchange')
    equipment_name = fields.Char(string='设备名称',track_visibility='onchange')
    equipment_count = fields.Char(string='设备编号',track_visibility='onchange')
    brenk_time = fields.Datetime(string='故障时间',track_visibility='onchange')
    brenk_repair_time = fields.Datetime(string='故障报修时间',track_visibility='onchange')
    brenk_state = fields.Text(string='故障情况',track_visibility='onchange')

    @api.onchange('brenk_repair_time','brenk_time')
    def time_sure(self):
        if self.brenk_time and self.brenk_repair_time:
            if self.brenk_repair_time < self.brenk_time:
                return {'value':{'brenk_time':None,'brenk_repair_time':None}}


    #自动获取登录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name

    #自动获取登录人的工号
    def default_jobnumber_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.jobnumber

    #提交功能
    def time_compare_action(self):
        new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d = datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=8)
        open_time = d + delta
        all_record = self.env['funenc_xa_station.date_time'].search_read([])
        if all_record:
            # for date_record in all_record:
            #     if str(open_time)[:10] == date_record['date_time_limit'][:10]: #判断记录有没有当天提交的记录
            #         if self.env.user.dingtalk_user.jobnumber == date_record.get('landing_job_number'):#判断当前人提交过没有
            #             raise exceptions.ValidationError('提交警告一天只能提交一次')
            pass

        item = {
            'date_time_limit': open_time,
            'landing_person':self.env.user.dingtalk_user.name,
            'landing_job_number':self.env.user.dingtalk_user.jobnumber,
        }
        self.env['funenc_xa_station.date_time'].sudo().create(item)

        values = self.env['funenc_xa_staion.prude_newpaper_write'].search_read([])

        #将select转化成为字符串
        for va in values:
            # event_stype = self.env['funenc_xa_staion.prude_newpaper_write'].sudo().search_read(
            #     [('event_stype', '=', va['event_stype']['prude_event_type'])],['id'])
            if va['event_stype'][1] == '边门进出情况':
                stype = 'enter_come'
            elif va['event_stype'][1] == '票务、AFC故障及异常情况':
                stype = 'ticket_acf'
            elif va['event_stype'][1] == '日票、预制单程票售卖情况':
                stype = 'ticket_sales'
            elif va['event_stype'][1] == '其他设备故障情况':
                stype = 'other_brenk'
            elif va['event_stype'][1] == '普通事件':
                stype = 'normal'

            va_value = {
                    'line_id' : va['line_id'][0],
                    'site_id' : va['site_id'][0],
                    'event_stype' : va['event_stype'][0],
                    'event_content' : va['event_content'],
                    'event_content_create' : va.get('event_content_create'),
                    'open_time' : va.get('open_time'),
                    'write_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'write_name' : va.get('write_name'),
                    'iobnumber' : va.get('iobnumber'),
                    'Enter_person_count' : va.get('Enter_person_count'),
                    'come_person_count' : va.get('come_person_count'),
                    'two_money' : va.get('two_money'),
                    'three_money' : va.get('three_money'),
                    'four_money' : va.get('four_money'),
                    'five_money' : va.get('five_money'),
                    'six_money' : va.get('six_money'),
                    'seven_money' : va.get('seven_money'),
                    'eight_money' : va.get('eight_money'),
                    'equipment_name' : va.get('equipment_name'),
                    'equipment_count' : va.get('equipment_count'),
                    'brenk_time' : va.get('brenk_time'),
                    'brenk_repair_time' : va.get('brenk_repair_time'),
                    'brenk_state' : va.get('brenk_state'),
                }

            #创建记录
            self.env['funenc_xa_station.prude_newspaper'].sudo().create(va_value)
        self.env['funenc_xa_staion.prude_newpaper_write'].search([]).unlink()

        return  self.env['funenc_xa_station.prude_newspaper'].get_day_plan_publish_action()

    #新创建一条记录
    def information_daynewpaper_write(self):
        view_form = self.env.ref('funenc_xa_station.prude_newspaper_write_form').id
        return{
            'name': '生产日报',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':[('create_user','=',self.env.user.id)],
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_staion.prude_newpaper_write',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target':'new',
        }

    #修改生产日报
    def prude_newpaper_type_onchange(self):
        view_form = self.env.ref('funenc_xa_station.prude_newspaper_write_form_modify').id
        return{
            'name': '日报填写',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id':self.id,
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_staion.prude_newpaper_write',
            'context': self.env.context,
            'target':'new',
        }

    def prude_newpaper_type_selete(self):
        self.env['funenc_xa_staion.prude_newpaper_write'].search([('id','=',self.id)]).unlink()

    @api.one
    @api.depends('event_stype')
    def _compute_event_stype_name(self):
        if self.event_stype:
            self.event_stype_name = self.event_stype.prude_event_type

    #更具不同的情况选择不同的字段
    @api.one
    @api.depends('event_stype')
    def _event_content(self):
        date_8 = datetime.timedelta(hours=8)
        if self.event_stype_name == '边门进出情况':
            self.event_content = str('进边门人数') + str(self.Enter_person_count or '') + ',' + str('出边门人数') + str(
                self.come_person_count or '')
        elif self.event_stype_name == '票务、AFC故障及异常情况':
            brank_time_8 = datetime.datetime.strptime(self.brenk_time, '%Y-%m-%d %H:%S:%M') + date_8
            brank_time_8 = datetime.datetime.strftime(brank_time_8, '%Y-%m-%d %H:%S:%M')
            brenk_repair_time_8 = str(datetime.datetime.strptime(self.brenk_repair_time, '%Y-%m-%d %H:%S:%M') + date_8)
            brenk_repair_time_8 = datetime.datetime.strptime(brenk_repair_time_8, '%Y-%m-%d %H:%S:%M')
            self.event_content = str('设备名称' or '') + ':' + str(self.equipment_name or '') \
                                 + str('、故障时间：') + str(brank_time_8 or '') \
                                 + str('、故障报修时间') + ':' + str(brenk_repair_time_8 or '') \
                                 + '、' + str('故障情况') + ':' + str(self.brenk_state or '')

        elif self.event_stype_name == '日票、预制单程票售卖情况':
            self.event_content = '2元' + ':' + str(self.two_money or '') \
                                 + '、' + '3元' + ':' + str(self.three_money or '') \
                                 + '、4元' + ':' + str(self.four_money or '') \
                                 + '、5元' + ':' + str(self.five_money or '') \
                                 + '、6元' + ':' + str(self.six_money or '') \
                                 + '、7元' + ':' + str(self.seven_money or '') \
                                 + '、8元' + ':' + str(self.eight_money or '')

        elif self.event_stype_name == '其他设备故障情况':
            brenk_repair_time_8 = datetime.datetime.strptime(self.brenk_repair_time, '%Y-%m-%d %H:%S:%M') + date_8
            brenk_repair_time_8 = datetime.datetime.strftime(brenk_repair_time_8, '%Y-%m-%d %H:%S:%M')
            brenk_time_8 = datetime.datetime.strptime(self.brenk_time, '%Y-%m-%d %H:%S:%M') + date_8
            brenk_time_8 = datetime.datetime.strftime(brenk_time_8, '%Y-%m-%d %H:%S:%M')
            self.event_content = '故障发时间：' + str(brenk_time_8 or '') \
                                 + '、故障报修时间:' + str(brenk_repair_time_8 or '') \
                                 + '、故障情况:' + str(self.brenk_state or '')

        else:
            self.event_content = self.event_content_create
     #修改当前的记录将新的值负值给对应的字段
    def save_current_record(self):
        if self.event_stype_name == '边门进出情况':
            self.event_content = str('进边门人数')+str(self.Enter_person_count or '') +','+ str('出边门人数') + str(self.come_person_count or '')

        elif self.event_stype_name == '票务、AFC故障及异常情况':
            self.event_content = str('设备名称' or '')+':'+str(self.equipment_name or '') + str('、故障时间：')+str(self.brenk_time or '') + \
                str('、故障报修时间')+':'+str(self.brenk_repair_time or '')+'、'+str('故障情况')+':'+str(self.brenk_state or '')

        elif self.event_stype_name == '日票、预制单程票售卖情况':
            self.event_content = '2元'+':'+str(self.two_money or '')+'、'+'3元'+':'+str(self.three_money or '')+'、4元'+':'\
                                 +str(self.four_money or '')+'、5元'+':'+str(self.five_money or '')+'、6元'+':'+str(self.six_money or '') \
                                 +'、7元'+':'+str(self.seven_money or '')+'、8元'+':'+str(self.eight_money or '')

        elif self.event_stype_name == '其他设备故障情况':
            self.event_content = '故障发时间：'+str(self.brenk_time or '')+'、故障报修时间:'+str(self.brenk_repair_time or '')\
                                 +'、故障情况:' + str(self.brenk_state or '')

        else:
            self.event_content = self.event_content_create

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.prude_newspaper_write_tree').id
        return {
            'name': '生产',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.prude_newspaper',
            'context': self.env.context,
        }


class DateTimeLimit(models.Model):
    _name = 'funenc_xa_station.date_time'

    date_time_limit = fields.Datetime(string='时间限制')
    landing_person = fields.Char(string='登录人的名字')
    landing_job_number = fields.Char(string='登录人的工号')





