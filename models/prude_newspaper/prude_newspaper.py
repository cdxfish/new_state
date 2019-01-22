# !user/bin/env python3
# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api
from ..get_domain import get_domain



key=[('enter_come','边门进出情况')
    ,('ticket_acf','票务、AFC故障及异常情况')
    ,('ticket_sales','日票、预制单程票售卖情况')
    ,('other_brenk','其他设备故障情况')
    ,('normal','普通事件')]

class PrudeNewspaper(models.Model):
    _name = 'funenc_xa_station.prude_newspaper'
    _order = 'write_time desc'
    _description = '生产日报'
    _rec_name = 'event_content_create'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']

    event_stype = fields.Many2one('funenc_xa_station.prude_newpaper_type',string='事件类型',required=True, track_visibility='onchange')
    event_stype_name = fields.Char(string='事件类型名称',compute='_compute_event_stype_name', track_visibility='onchange')
    event_content = fields.Text(string='事件内容', track_visibility='onchange')
    event_content_create = fields.Text(string='事件内容', track_visibility='onchange')
    open_time = fields.Datetime(string='发生时间', track_visibility='onchange')
    write_time = fields.Datetime(string='提交时间', track_visibility='onchange')
    write_name = fields.Char(string='填报人', track_visibility='onchange')
    iobnumber = fields.Char(string='工号', track_visibility='onchange')
    Enter_person_count =fields.Integer(string='进边门人数', track_visibility='onchange')
    come_person_count = fields.Integer(string='出边门人数', track_visibility='onchange')
    two_money =fields.Char(string='2元', track_visibility='onchange')
    three_money = fields.Char(string='3元', track_visibility='onchange')
    four_money = fields.Char(string='4元', track_visibility='onchange')
    five_money =fields.Char(string='5元', track_visibility='onchange')
    six_money =fields.Char(string='6元', track_visibility='onchange')
    seven_money = fields.Char(string='7元', track_visibility='onchange')
    eight_money = fields.Char(string='8元', track_visibility='onchange')
    equipment_name = fields.Char(string='设备名称', track_visibility='onchange')
    equipment_count = fields.Char(string='设备编号', track_visibility='onchange')
    brenk_time = fields.Datetime(string='故障时间', track_visibility='onchange')
    brenk_repair_time = fields.Datetime(string='故障报修时间', track_visibility='onchange')
    brenk_state = fields.Text(string='故障情况', track_visibility='onchange')
    c_type = fields.Char(string='区分', track_visibility='onchange')

    #关联页面的显示效果
    @api.one
    @api.depends('event_stype')
    def _compute_event_stype_name(self):
        if self.event_stype:
            self.event_stype_name = self.event_stype.prude_event_type




    @api.one
    @api.depends('event_stype')
    def _compute_event_stype_name(self):
        if len(self.event_stype) != 0:
            self.event_stype_name = self.event_stype.prude_event_type

    #页面跳转的信息填报
    @api.model
    @get_domain
    def information_write(self,domain):
        view_form = self.env.ref('funenc_xa_station.prude_newspaper_write_tree').id
        return {
            'name': '生产日报',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'domain': domain,
            'view_mode': 'form',
            "views": [[view_form, "tree"]],
            'res_model': 'funenc_xa_staion.prude_newpaper_write',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
        }

    # #修改当前记录
    # @api.model
    # def change_change_act(self):
    #     return {
    #         'name': '生产日报',
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_id':self.id,
    #         'res_model': 'funenc_xa_station.prude_newspaper',
    #         'context': self.env.context,
    #         'flags': {'initial_mode': 'edit'},
    #     }

    #删除按钮
    # @api.model
    def delete_button_action(self):
        self.env['funenc_xa_station.prude_newspaper'].search([('id','=',self.id)]).unlink()

    # @api.onchange('event_stype')
    # def c_type_distinguish(self):
    #     cc = self.env['funenc_xa_station.prude_newspaper'].search_read([],['event_stype'])
    #     print(cc)
    #     return {
    #         'invisible':[('event_content', '!=','')]
    #     }

    @api.one
    @api.depends('event_stype')
    def _event_content(self):
        if self.event_stype.prude_event_type == '边门进出情况':
            self.event_content = str('进边门人数')+str(self.Enter_person_count or '') +','+ str('出边门人数') + str(self.come_person_count or '')

        elif self.event_stype.prude_event_type == '票务、AFC故障及异常情况':
            self.event_content = str('设备名称')+':'+str(self.equipment_name or '') + str('、故障时间：')+str(self.brenk_time or '') + \
                str('、故障报修时间')+':'+str(self.brenk_repair_time or '')+'、'+str('故障情况')+':'+str(self.brenk_state or '')

        elif self.event_stype.prude_event_type == '日票、预制单程票售卖情况':
            self.event_content = '2元'+':'+str(self.two_money or 0)+'、'+'3元'+':'+str(self.three_money or 0)+'、4元'+':'\
                                 +str(self.four_money or 0)+'、5元'+':'+str(self.five_money or 0)+'、6元'+':'+str(self.six_money or 0) \
                                 +'、7元'+':'+str(self.seven_money or 0)+'、8元'+':'+str(self.eight_money or 0)

        elif self.event_stype.prude_event_type == '其他设备故障情况':
            self.event_content = '故障发时间：'+str(self.brenk_time or '')+'、故障报修时间:'+str(self.brenk_repair_time or '')\
                                 +'、故障情况:' + str(self.brenk_state or '')

        else:
            self.event_content = self.event_content_create

    #页面修改
    def change_change_act(self):
            view_form = self.env.ref('funenc_xa_station.prude_newspaper_form_view').id
            return {
                'name': '生产日报',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.prude_newspaper',
                'context': self.env.context,
                'res_id':self.id,
                'flags': {'initial_mode': 'edit'},
                'target':'new'
            }

    # 修改页面当前记录的时候整合数据
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
        view_tree = self.env.ref('funenc_xa_station.prude_newspaper_tree_view').id
        return {
            'name': '生产日报',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.prude_newspaper',
            'context': self.env.context,
        }










