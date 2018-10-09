# !user/bin/env python3
# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api


key=[('enter_come','边门进出情况')
    ,('ticket_acf','票务、AFC故障及异常情况')
    ,('ticket_sales','日票、预制单程票售卖情况')
    ,('other_brenk','其他设备故障情况')
    ,('normal','其他设备故障情况')]

class PrudeNewspaper(models.Model):
    _name = 'funenc_xa_station.prude_newspaper'
    _inherit = 'fuenc_station.station_base'

    event_stype = fields.Many2one('funenc_xa_station.prude_newpaper_type',string='事件类型')
    event_stype_name = fields.Char(compute='_compute_event_stype_name')
    event_content = fields.Text(string='事件内容',compute='_event_content',store=True)
    event_content_create = fields.Text(string='事件内容')
    open_time = fields.Datetime(string='发生时间')
    write_time = fields.Datetime(string='填报时间')
    write_name = fields.Char(string='填报人')
    iobnumber = fields.Char(string='工号')
    Enter_person_count =fields.Integer(string='进边门人数')
    come_person_count = fields.Integer(string='出边门人数')
    two_money =fields.Char(string='2元')
    three_money = fields.Char(string='3元')
    four_money = fields.Char(string='4元')
    five_money =fields.Char(string='5元')
    six_money =fields.Char(string='6元')
    seven_money = fields.Char(string='7元')
    eight_money = fields.Char(string='8元')
    equipment_name = fields.Char(string='设备名称')
    equipment_count = fields.Char(string='设备编号')
    brenk_time = fields.Datetime(string='故障时间')
    brenk_repair_time = fields.Datetime(string='故障保修时间')
    brenk_state = fields.Text(string='故障情况')
    c_type = fields.Char(string='区分')


    @api.one
    @api.depends('event_stype')
    def _compute_event_stype_name(self):
        if len(self.event_stype) != 0:
            self.event_stype_name = self.event_stype.prude_event_type

    @api.model
    def information_write(self):
        view_form = self.env.ref('funenc_xa_station.prude_newspaper_form').id
        return {
            'name': '生产日报',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.prude_newspaper',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

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
            self.event_content = str('进边门人数')+str(self.Enter_person_count) +','+ str('出边门人数') + str(self.come_person_count)

        elif self.event_stype.prude_event_type == '票务、AFC故障及异常情况':
            self.event_content = str('设备名称')+':'+str(self.equipment_name) + str('、故障时间：')+str(self.brenk_time) + \
                str('、故障保修时间')+':'+str(self.brenk_repair_time)+'、'+str('故障情况')+':'+str(self.brenk_state)

        elif self.event_stype.prude_event_type == '日票、预制单程票售卖情况':
            self.event_content = '2元'+':'+self.two_money+'、'+'3元'+':'+str(self.three_money)+'、4元'+':'\
                                 +str(self.four_money)+'、5元'+':'+str(self.five_money)+'、6元'+':'+str(self.six_money) \
                                 +'、7元'+':'+str(self.seven_money)+'、8元'+':'+str(self.eight_money)

        elif self.event_stype.prude_event_type == '其他设备故障情况':
            self.event_content = '故障发时间：'+str(self.brenk_time)+'、故障报修时间:'+str(self.brenk_repair_time)\
                                 +'、故障情况:' + str(self.brenk_state)

        else:
            self.event_content = self.event_content_create









