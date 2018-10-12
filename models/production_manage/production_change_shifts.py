# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class production_change_shifts(models.Model):
    _name = 'funenc_xa_station.production_change_shifts'
    _inherit = 'fuenc_station.station_base'
    _description = u'生产管理交接班'

    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',stirng='交班人')
    take_over_from_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',stirng='接班人')
    on_duty_time = fields.Datetime(string='当班时间')
    change_shifts_time = fields.Datetime(string='交班时间')
    #####
    take_over_from_time = fields.Datetime(string='接班时间')
    state = fields.Selection(selection=[('draft','草稿'),('change_shifts','交班'),('take_over_from','接班')],default="draft")

    # 值班站长
    # 工作情况字段
    anticipation_security = fields.Text(string='安全预想')
    before_on_duty = fields.Text(string='班前情况')
    put_question_ids = fields.One2many('funenc_xa_station.put_question', 'production_change_shifts_id', string='班前提问')
    meeting_ids = fields.One2many("funenc_xa_station.meeting_dateils",'shifts_id',string='会议记录')
    master_to_production_change_ids = fields.One2many('funenc_xa_station.station_master_to_production_change_shifts','production_change_shifts_id',string='备品')

    # 班中工
    complete_task = fields.Text(stirng='当前工作完成情况')
    equipment_problem = fields.Text(string='设备设施存在的问题')
    handover = fields.Text(string='交接事项')
    after_work = fields.Text(string='班后总结')

    focus_of_handover = fields.Text(string='交接重点')

    # 行车值班员
    in_the_rough = fields.Text(string='未完成')


    @api.model
    def create_production_change_shifts(self):
        context = dict(self.env.context or {})
        local_station_master_ids = set(self.master_to_production_change_ids.ids)
        station_master = self.env['funenc_xa_station.station_master'].search([])[0]
        inst_ids = list(set(station_master.preparedness_ids.ids) - local_station_master_ids)
        for inst_id in inst_ids:
            self.master_to_production_change_ids =  (0, 0, {'station_master_id':inst_id})

        return {
            'name': '交接班创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.production_change_shifts',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '耗材出库编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.production_change_shifts',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def production_change_shifts_save(self):
        pass

    def submit(self):
        self.state = 'change_shifts'


class put_question(models.Model):
    _name = 'funenc_xa_station.put_question'
    _description = u'班前提问'

    put_question_name = fields.Char(string='提问姓名')
    examination_questions = fields.Char(string='题目')
    score = fields.Char(string='分数')
    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts',string='交接班')


class station_master_to_production_change_shifts(models.Model):
    _name = 'funenc_xa_station.station_master_to_production_change_shifts'
    _description = u'备品交接班中间表'

    KEY=[('station_master','站长'),
         ('train_working','行车'),
         ('station_service','站务'),
         ('ticket_booth', '票亭'),
         ('passenger_transport','客运'),
         ]

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    station_master_id = fields.Many2one('funenc_xa_station.station_master', string='备品')
    unit = fields.Char(realted='station_master_id.unit',string='单位')
    # type = fields.Selection(selection=KEY,related='station_master_id.type' ,string='备品类型')
    count = fields.Integer(string='数量')
    state = fields.Selection(selection=[('fine','良好'),('abnormity','异常')])
    remarks = fields.Text(string='备注')



