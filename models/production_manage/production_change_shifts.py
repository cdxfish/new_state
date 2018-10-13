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
    production_to_train_working_ids = fields.One2many('funenc_xa_station.check_project','production_change_shifts_id',string='运营前检查')
    focus_of_work = fields.Text(string='今日工作重点记录')
    other_work_record = fields.Text(string='其他工作记录')

    ### 车站客运情况
    daily_passenger_volume = fields.Char(string='本日进/出站客运量')
    tmv_booking = fields.Char(string='本日TVM售票数量')
    anniversary_booking = fields.Char(string='纪念票出售数量')
    number_of_opening_door = fields.Char(string='开边门次数')
    coin_stock = fields.Char(string='硬币库存量')
    stock_increase_stock = fields.Char(string='增票库存')
    day_number_of_guest_injuries = fields.Char(string='本日客伤数量')
    number_of_complaints_today = fields.Char(string='本日投诉数量')
    gratitude_number = fields.Char(string='本日感谢信/锦旗数量')
    good_people_good_deeds = fields.Char(string='好人好事量')

    #  票款收入
    tmv_booking_income = fields.Char(string='本日TVM收入')
    other_tickets_income = fields.Char(string='其他票款收入')

    driving_handover = fields.Text(string='行车有关事项交接')
    construction_handover = fields.Text(string='施工作业相关事项交')
    other_handover = fields.Text(string='其他事项交接')

    # 客运值班员
      # 基本北荣

    flight_ticket = fields.Char(string='本班票款')
    special_card_preset_id = fields.Many2one('funenc_xa_station.special_card_preset', string='特殊卡号')
    special_card_preset_no = fields.Char(string='特殊工作卡卡数')
    spare_gold_notes = fields.Char(string='备用金本班结存(纸币)')
    spare_gold_coin = fields.Char(string='备用金本班结存(硬币)')
    spare_gold_total = fields.Char(string='备用金本班结存(总计)')
    day_15_situation = fields.Text(string='车站每月15日盘点情况')

    reserver_management_ids = fields.One2many('funenc_xa_station.reserver_management','production_change_shifts_id', string='车站备用金')

        # 票务钥匙情况
    ticketing_key_type_ids = fields.One2many('funenc_xa_station.ticketing_key_type','production_change_shifts_id', string='钥匙情况')
    train_working_1_id = fields.One2many('funenc_xa_station.train_working_1','production_change_shifts_id', string='运营前检查项目')



    @api.model
    def create_production_change_shifts(self):
        context = dict(self.env.context or {})
        local_station_master_ids = set(master_to_production_change_id for  master_to_production_change_id in self.master_to_production_change_ids)
        station_master = self.env['funenc_xa_station.station_master'].search([])[0]
        inst_ids = list(set(station_master.preparedness_ids.ids) - local_station_master_ids)
        for inst_id in inst_ids:
            self.master_to_production_change_ids = (0, 0, {'station_master_id':inst_id
                                                           })

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
            'name': '交接班编辑',
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
    list_situation = fields.Char(string='清单情况')
    exceptional_situation = fields.Char(string='异常情况')




