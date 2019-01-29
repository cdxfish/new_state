# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from ..get_domain import get_domain
from ..python_util import get_add_8th_str_time
from odoo.exceptions import ValidationError

from ..get_domain import get_line_id_domain

KEY = [('station_master', '值班站长'),
       ('train_working', '行车值班员'),
       ('station_service', '站务'),
       ('ticket_booth', '票亭'),
       ('passenger_transport', '客运'),
       ]


class production_change_shifts(models.Model):
    _name = 'funenc_xa_station.production_change_shifts'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _description = u'生产管理交接班'
    _order = 'change_shifts_time desc'
    _rec_name = 'change_shifts_user_id'

    @api.model
    def default_user(self):
        if self.env.user.id == 1:
            return
        else:

            return self.env.user.dingtalk_user.id

    @api.model
    def default_production_state(self):


        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            return 'station_master'
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车
            return 'train_working'
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            return 'passenger_transport'
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            # 站务
            return 'station_service'
        else:
            # 票务
            return 'ticket_booth'

    # @api.model
    # def get_views(self):
    #     if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
    #         list_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list')
    #         form_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_form')
    #         domain = [('production_state', '=', 'station_master')]
    #         # 值班站长
    #         return {
    #             'list_views': list_views,
    #             'form_views': form_views,
    #             'domain': domain
    #         }
    #     elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
    #         # 行车
    #         list_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list')
    #         form_views = self.env.ref('funenc_xa_station.production_change_train_working_shifts_form11')
    #         domain = [('production_state', '=', 'train_working')]
    #         return {
    #             'list_views': list_views,
    #             'form_views': form_views,
    #             'domain': domain
    #         }
    #     # 客运
    #     elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
    #         list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
    #         form_views = self.env.ref('funenc_xa_station.station_service_form')
    #         domain = [('production_state', '=', 'station_service')]
    #         return {
    #             'list_views': list_views,
    #             'form_views': form_views,
    #             'domain': domain
    #         }
    #     # 站台岗
    #     elif self.env.user.has_group('funenc_xa_station.module_depot'):
    #         list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
    #         form_views = self.env.ref('funenc_xa_station.passenger_transport_train_working_shifts_form11')
    #         domain = [('production_state', '=', 'passenger_transport')]
    #         return {
    #             'list_views': list_views,
    #             'form_views': form_views,
    #             'domain': domain
    #         }
    #     else:
    #         # 票务
    #         list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
    #         form_views = self.env.ref('funenc_xa_station.station_service_form')
    #         domain = [('production_state', '=', 'ticket_booth')]
    #         return {
    #             'list_views': list_views,
    #             'form_views': form_views,
    #             'domain': domain
    #         }

    @api.onchange('preparedness_2_ids')
    def onchange_preparedness_2_ids(self):
        try:
            if not self.preparedness_2_ids:
                obj = self.env['funenc_xa_station.passenger_transport'].search([])[0]
                inst_ids = obj.preparedness_ids
                default_data = []
                for inst_id in inst_ids:
                    default_data.append((0, 0, {'name': inst_id.preparedness_name}))
                return {
                    'value': {'preparedness_2_ids': default_data}
                }
            else:
                return
        except:
            raise ValidationError('请检查系统配置中的预设交接班是否配置')

    @api.onchange('prefabricate_ticket_type_2_ids')
    def onchange_prefabricate_ticket_type_2_ids(self):
        try:
            if not self.prefabricate_ticket_type_2_ids:
                obj = self.env['funenc_xa_station.passenger_transport'].search([])[0]
                inst_ids = obj.prefabricate_ticket_type_ids
                default_data = []
                for inst_id in inst_ids:
                    default_data.append((0, 0, {'name': inst_id.name}))
                return {
                    'value': {'prefabricate_ticket_type_2_ids': default_data}
                }

            else:
                return
        except:
            raise ValidationError('请检查系统配置中的预设交接班是否配置')


    @api.onchange('ticketing_key_type_2_ids')
    def onchange_ticketing_key_type_2_ids(self):
        try:
            if not self.ticketing_key_type_2_ids:
                obj = self.env['funenc_xa_station.passenger_transport'].search([])[0]
                inst_ids = obj.ticketing_key_type_ids
                default_data = []
                for inst_id in inst_ids:
                    default_data.append((0, 0, {'name': inst_id.name}))
                return {
                    'value': {'ticketing_key_type_2_ids': default_data}
                }
            else:
                return
        except:
            raise ValidationError('请检查系统配置中的预设交接班是否配置')

    ticketing_key_type_2_ids = fields.One2many('funenc_xa_station.ticketing_key_type_2', 'production_change_shifts_id',
                                               string='票务钥匙使用情况', track_visibility='onchange')

    prefabricate_ticket_type_2_ids = fields.One2many('funenc_xa_station.prefabricate_ticket_type_2',
                                                     'production_change_shifts_id', string='车票使用情况', track_visibility='onchange')
    preparedness_2_ids = fields.One2many('funenc_xa_station.preparedness_2', 'production_change_shifts_id', track_visibility='onchange')

    production_state = fields.Selection(selection=KEY, string='记录状态',
                                        default=lambda self: self.default_production_state())  #
    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', stirng='交班人',
                                            default=lambda self: self.default_user(), track_visibility='onchange')
    job_number_per = fields.Char(string='交班人工号',related='change_shifts_user_id.jobnumber')
    take_over_from_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', stirng='接班人', track_visibility='onchange')
    job_no = fields.Char("工号", related='take_over_from_user_id.jobnumber')
    position = fields.Text("职位", related='take_over_from_user_id.position')
    on_duty_time = fields.Datetime(string='当班时间', track_visibility='onchange')
    change_shifts_time = fields.Datetime(string='交班时间', track_visibility='onchange')
    #####
    take_over_from_time = fields.Datetime(string='接班时间', track_visibility='onchange')
    state = fields.Selection(selection=[('draft', '草稿'), ('change_shifts', '待接班'), ('take_over_from', '已接班')],
                             default="draft")

    # 值班站长
    # 工作情况字段
    anticipation_security = fields.Text(string='安全预想', track_visibility='onchange')
    before_on_duty = fields.Text(string='班前情况', track_visibility='onchange')
    put_question_ids = fields.One2many('funenc_xa_station.put_question', 'production_change_shifts_id', string='班前提问', track_visibility='onchange')
    meeting_ids = fields.One2many("funenc_xa_station.meeting_dateils", 'shifts_id', string='会议记录', track_visibility='onchange')
    my_change_ids = fields.One2many('funenc_xa_station.preparedness_6',
                                    'shifts_id', string='备品', track_visibility='onchange'
                                    )

    ## 票务和站务备品
    preparedness_1_ids = fields.One2many('funenc_xa_station.preparedness_1', 'production_change_shifts_id',
                                         string='票务和站务备品', track_visibility='onchange')

    # 班中工
    complete_task = fields.Text(stirng='当前工作完成情况', track_visibility='onchange')
    equipment_problem = fields.Text(string='设备设施存在的问题', track_visibility='onchange')
    handover = fields.Text(string='交接事项', track_visibility='onchange')
    after_work = fields.Text(string='班后总结', track_visibility='onchange')

    focus_of_handover = fields.Text(string='交接重点', track_visibility='onchange')

    # 行车值班员
    in_the_rough = fields.Text(string='未完成')
    production_to_train_working_ids = fields.One2many('funenc_xa_station.check_project_to_production_change_shifts',
                                                      'production_change_shifts_id',
                                                      string='运营前检查', track_visibility='onchange'
                                                      # default=lambda self: self.default_production()
                                                      )
    driving_my_change_ids = fields.One2many('funenc_xa_station.preparedness_7',
                                    'shifts_id', string='行车备品', track_visibility='onchange'
                                    )


    check_project_ids = fields.One2many('funenc_xa_station.train_working_2', 'production_change_shifts1_id',
                                        string='运营前检查', track_visibility='onchange'
                                        # default=lambda self:self.default_check_project_ids()
                                        )

    preparedness_state = fields.Selection(selection=[('正常', '正常'), ('异常', '异常')], default="正常", string='备品状态', track_visibility='onchange')  # 备品状态

    is_take_over_from = fields.Integer(string='是否可接班',compute='_compute_is_take_over_from') # 用于接班按钮显示 1为显示
    xml_id = fields.Integer(string='视图xml_id') #  用于 clint判断进哪个页面

    @api.constrains('meeting_ids')
    def constrains_constrains(self):
        line_id = self.line_id.id
        site_id = self.site_id.id
        meeting_ids =self.meeting_ids
        for meeting_id in meeting_ids:
            meeting_id.line_id = line_id
            meeting_id.site_id = site_id

    def _compute_is_take_over_from(self):
        if self.env.user.id ==1:
            for this in self:
                this.is_take_over_from = 1
        else:
            ding_user_id = self.env.user.dingtalk_user.id
            for this in self:
                if this.state == 'change_shifts'  :
                    if this.change_shifts_user_id.id == ding_user_id:
                        this.is_take_over_from = 0
                    else:
                        this.is_take_over_from = 1

    @api.onchange('check_project_ids')
    def onchange_check_project_ids(self):
        # 预设行车
        try:
            if not self.check_project_ids:
                obj = self.env['funenc_xa_station.car_line'].search([])[0]
                inst_ids = obj.check_project_ids
                default_data = []
                for inst_id in inst_ids:
                    default_data.append((0, 0, {'context': inst_id.context}))

                return {
                    'value': {'check_project_ids': default_data}
                }

            else:
                return
        except:
            raise ValidationError('请检查系统配置中的预设交接班是否配置')

    @api.onchange('preparedness_1_ids')
    def onchange_preparedness_1_ids(self):
        if not self.preparedness_1_ids:
            obj = self.env['funenc_xa_station.car_line'].search([])[0]
            inst_ids = obj.check_project_ids
            default_data = []
            for inst_id in inst_ids:
                default_data.append((0, 0, {'context': inst_id.context}))
            return {
                'value': {'check_project_ids': default_data}
            }
        else:
            return

    #### 这种就是坑 不能用方法来填默认值
    @api.model
    def default_check_project_ids(self):
        obj = self.env['funenc_xa_station.car_line'].search([])[0]
        inst_ids = obj.check_project_ids
        default_data = []
        for inst_id in inst_ids:
            default_data.append((0, 0, {'context': inst_id.context}))

    @api.onchange('preparedness_1_ids')
    def onchange_preparedness_1_ids(self):
        # 判断是不是站务
        try:
            if not self.preparedness_1_ids:
                if self._context.get('is_station_service'):
                    # 站务
                    obj = self.env['funenc_xa_station.station_service'].search([])
                    only_obj = obj[0] if obj else None
                else:
                    # 票务
                    obj = self.env['funenc_xa_station.ticket_booth'].search([])
                    only_obj = obj[0] if obj else None
                if only_obj:
                    inst_ids = only_obj.preparedness_ids
                    default_data = []
                    for inst_id in inst_ids:
                        default_data.append((0, 0, {'preparedness_name': inst_id.preparedness_name, 'unit': inst_id.unit}))
                    return {
                        'value': {'preparedness_1_ids': default_data}
                    }
                else:
                    return
            else:
                return
        except:
            raise ValidationError('请检查系统配置中的预设交接班是否配置')

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
    good_people_good_deeds = fields.Char(string='好人好数量')

    #  票款收入
    tmv_booking_income = fields.Char(string='本日TVM收入')
    other_tickets_income = fields.Char(string='其他票款收入')

    driving_handover = fields.Text(string='行车有关事项交接')
    construction_handover = fields.Text(string='施工作业相关事项交')
    other_handover = fields.Text(string='其他事项交接')

    # 客运值班员
    # 基本北荣

    flight_ticket = fields.Char(string='本班票款')
    special_card_preset_id = fields.Many2many('funenc_xa_station.special_card_preset', 'production_card_rel',
                                              'production_id', 'card_id', string='特殊卡号')
    special_card_preset_no = fields.Char(string='特殊工作卡卡数', compute='compute_special_card_preset_no')
    spare_gold_notes = fields.Char(string='备用金本班结存(纸币)')
    spare_gold_coin = fields.Char(string='备用金本班结存(硬币)')
    spare_gold_total = fields.Char(string='备用金本班结存(总计)')
    day_15_situation = fields.Text(string='车站每月15日盘点情况')

    reserver_management_ids = fields.One2many('funenc_xa_station.reserver_management', 'production_change_shifts_id',
                                              string='车站备用金')

    # 票务钥匙情况
    ticketing_key_type_ids = fields.One2many('funenc_xa_station.ticketing_key_type', 'production_change_shifts_id',
                                             string='钥匙情况')
    train_working_1_id = fields.One2many('funenc_xa_station.train_working_1', 'production_change_shifts_id',
                                         string='运营前检查项目')
    # 特殊卡号
    special_card_preset_ids = fields.One2many('funenc_xa_station.special_card_preset', 'production_change_shifts_id',
                                              string='特殊卡号')

    remarks = fields.Text(string='备注')

    spare_gold_ids = fields.One2many('funenc_xa_station.spare_gold', 'production_change_shifts_id', string='备用金配出')
    tail_box_ids = fields.One2many('funenc_xa_station.tail_box', 'production_change_shifts_id', string='库包/尾箱交接')

    @get_domain
    def production_change_shifts_list(self, domain):
        context = dict(self.env.context or {})
        domain.append(('state', '!=', 'draft'))

        form_views = self.get_form_id()
        tree = self.env.ref('funenc_xa_station.production_change_shifts_train_working_list11').id

        return {
            'name': '交接班详情',
            'type': 'ir.actions.act_window',
            'views': [[tree, 'tree'], [form_views, 'from']],
            'res_model': 'funenc_xa_station.production_change_shifts',
            'context': context,
            'target': 'current',
            'domain': domain
        }

    @api.depends('special_card_preset_id')
    def compute_special_card_preset_no(self):
        for this in self:
            this.special_card_preset_no = len(this.special_card_preset_id.ids)



    @api.onchange('driving_my_change_ids')
    def onchange_driving_my_change_ids(self):
        if not self.driving_my_change_ids:
            try:
                obj = self.env['funenc_xa_station.car_line'].search([])[0]
                if obj:
                    inst_ids = obj.preparedness_ids
                    default_data = []
                    for inst_id in inst_ids:
                        default_data.append((0, 0, {'name': inst_id.preparedness_name, 'unit': inst_id.unit}))

                    return {
                        'value': {'driving_my_change_ids': default_data}
                    }

                else:
                    return

            except:
                raise ValidationError('请检查系统配置中的预设交接班是否配置')
        else:
            return


    @api.onchange('my_change_ids')
    def onchange_my_change_ids(self):
        if not self.my_change_ids:
            position = self.get_position()
            try:
                if position == 'station_master':
                    obj = self.env['funenc_xa_station.station_master'].search([])
                    station_master = obj[0] if obj else None
                    default_data = []
                    for inst_id in station_master.preparedness_ids:
                        default_data.append((0, 0, {'name': inst_id.preparedness_name, 'unit': inst_id.unit}))

                    return {
                        'value': {'my_change_ids': default_data}
                    }
                else:
                    obj = self.env['funenc_xa_station.car_line'].search([])[0]
                    if obj:
                        inst_ids = obj.preparedness_ids
                        default_data = []
                        for inst_id in inst_ids:
                            default_data.append((0, 0, {'name': inst_id.preparedness_name, 'unit': inst_id.unit}))

                        return {
                            'value': {'my_change_ids': default_data}
                        }
                    else:
                        return
            except:
                raise ValidationError('请检查系统配置中的预设交接班是否配置')
        else:
            return

    @api.model
    def default_production(self):
        obj = self.env['funenc_xa_station.car_line'].search([])[0]
        inst_ids = obj.check_project_ids.ids
        default_data = []
        for inst_id in inst_ids:
            default_data.append((0, 0, {'check_project_id': inst_id}))

    # @api.model
    # def create_production_change_shifts(self):
    #     context = dict(self.env.context or {})
    #
    #     if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
    #         # 值班站长
    #         view_form = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_form').id
    #         return {
    #             'name': '交接班创建',
    #             'type': 'ir.actions.act_window',
    #             "views": [[view_form, "form"]],
    #             'res_model': 'funenc_xa_station.production_change_shifts',
    #             'context': context,
    #             'target': 'new',
    #             'flags': {'initial_mode': 'edit'},
    #         }
    #     elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
    #         # 行车
    #         view_form = self.env.ref('funenc_xa_station.production_change_train_working_shifts_form11').id
    #         return {
    #             'name': '交接班创建',
    #             'type': 'ir.actions.act_window',
    #             "views": [[view_form, "form"]],
    #             'res_model': 'funenc_xa_station.production_change_shifts',
    #             'context': context,
    #             'target': 'new',
    #             'flags': {'initial_mode': 'edit'},
    #         }
    #     elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
    #         # 客运
    #         view_form = self.env.ref('funenc_xa_station.passenger_transport_train_working_shifts_form11').id
    #         return {
    #             'name': '交接班创建',
    #             'type': 'ir.actions.act_window',
    #             "views": [[view_form, "form"]],
    #             'res_model': 'funenc_xa_station.production_change_shifts',
    #             'context': context,
    #             'target': 'new',
    #             'flags': {'initial_mode': 'edit'},
    #         }
    #     elif self.env.user.has_group('funenc_xa_station.module_depot'):
    #         # 站务
    #         view_form = self.env.ref('funenc_xa_station.station_service_form').id
    #         return {
    #             'name': '交接班创建',
    #             'type': 'ir.actions.act_window',
    #             "views": [[view_form, "form"]],
    #             'res_model': 'funenc_xa_station.production_change_shifts',
    #             'context': context,
    #             'target': 'new',
    #             'flags': {'initial_mode': 'edit'},
    #         }
    #     else:
    #         # 票务
    #         view_form = self.env.ref('funenc_xa_station.station_service_form').id
    #         return {
    #             'name': '交接班创建',
    #             'type': 'ir.actions.act_window',
    #             "views": [[view_form, "form"]],
    #             'res_model': 'funenc_xa_station.production_change_shifts',
    #             'context': context,
    #             'target': 'new',
    #             'flags': {'initial_mode': 'edit'},
    #         }

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
        if self.state == 'draft':
            self.unlink()
        else:
            return False

    def production_change_shifts_save(self):
        return {
            'name': '交接班',
            'type': 'ir.actions.client',
            'tag': 'change_shifts_clint',
            'target': 'current',
        }

    def submit(self):
        self.state = 'change_shifts'  # 待接班
        self.change_shifts_time = datetime.datetime.now()
        return {
            'name': '交接班',
            'type': 'ir.actions.client',
            'tag': 'change_shifts_clint',
            'target': 'current',
        }

    def take_over(self):
        if self.env.user.id == 1:
            return
        else:
            #####
            self.state = 'take_over_from'  # 已接班
            self.take_over_from_user_id = self.env.user.dingtalk_user.id
            self.take_over_from_time = datetime.datetime.now()
            return {
                'name': '交接班',
                'type': 'ir.actions.client',
                'tag': 'change_shifts_clint',
                'target': 'current'
            }

    def get_position(self):
        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            position = 'station_master'
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车值班员
            position = 'train_working'
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            position = 'passenger_transport'
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            # 站台 站务
            position = 'station_service'
        else:
            # 票务
            position = 'ticket_booth'

        return position

    @get_line_id_domain
    @api.model
    def get_change_shifts_data(self,line_id_domain):

        position = self.get_position()
        user_dic = {
            'name': '', 'line_id': '', 'department_name': '', 'jobnumber': '', 'position': ''
        }

        if self.env.user.id == 1:
            return {
                'change_shifts_ids': '',
                'take_over_from_ids': '',
                'user': '',
                'domain': [('state', '=', 'change_shifts')],
                'views': '',
                'jb_form': ''
            }

        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        domain = [('site_id', 'in', department_ids.ids),
                  ('change_shifts_user_id', '!=', ding_user.id), ('state', '=', 'change_shifts')]
        position_domain = self.get_position_domain()
        domain.append(position_domain)

        line_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(line_id_domain)
        line_name = '' # 所属线路名
        for i,line in enumerate(line_ids):
            if i == 0:
                line_name = line_name + line.name
            else:
                line_name = line_name + ',' + line.name

        department_name = ''  # 站点名
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                if not department_name:
                    department_name = department_name + department_id.name
                else:
                    department_name = department_name + ',' + department_id.name

        user_dic['name'] = ding_user.name
        user_dic['line_id'] = line_name
        user_dic['department_name'] = department_name
        user_dic['jobnumber'] = ding_user.jobnumber
        user_dic['position'] = ding_user.position
        # ('state', 'in', ['change_shifts', 'draft']),
        change_shifts_ids = self.search_read(
            [('change_shifts_user_id', '=', ding_user.id)],
            ['id', 'change_shifts_time', 'take_over_from_user_id', 'job_no',
             'take_over_from_time', 'xml_id'], order='take_over_from_time desc')  # 待接班
        take_over_from_ids = self.search_read(
            [('take_over_from_user_id', '=', ding_user.id),
             ('state', '=', 'take_over_from')],
            ['id', 'change_shifts_time', 'take_over_from_user_id', 'job_no',
             'take_over_from_time', 'xml_id'], order='take_over_from_time desc')  # 已接班
        for change_shifts_id in change_shifts_ids:
            change_shifts_id['take_over_from_user_id'] = change_shifts_id.get('take_over_from_user_id')[
                1] if change_shifts_id.get('take_over_from_user_id') else ''
            if change_shifts_id.get('change_shifts_time'):
                change_shifts_id['change_shifts_time'] = get_add_8th_str_time(change_shifts_id['change_shifts_time'])

            if change_shifts_id.get('take_over_from_time'):
                change_shifts_id['take_over_from_time'] = get_add_8th_str_time(change_shifts_id['take_over_from_time'])

        for change_shifts_id_id in take_over_from_ids:
            change_shifts_id_id['take_over_from_user_id'] = change_shifts_id_id.get('take_over_from_user_id')[1] if change_shifts_id_id.get('take_over_from_user_id') else ''
            if change_shifts_id_id.get('change_shifts_time'):
                change_shifts_id_id['change_shifts_time'] = get_add_8th_str_time(change_shifts_id_id['change_shifts_time'])

            if change_shifts_id_id.get('take_over_from_time'):
                change_shifts_id_id['take_over_from_time'] = get_add_8th_str_time(change_shifts_id_id['take_over_from_time'])

        djb_tree = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list').id
        job_form = self.get_form_id()

        return {
            'change_shifts_ids': change_shifts_ids,
            'take_over_from_ids': take_over_from_ids,
            'user': user_dic,
            'domain': domain,
            'views': djb_tree,
            'position': position,
            'job_form':job_form
        }

    @api.model
    def get_job_form_xml_id(self,**kw):
        xml_id = kw.get('xml_id')
        view_xml_id = self.env.ref(xml_id).id

        return view_xml_id

    @api.model
    def create(self, vals):

        if self._context.get('xml_id'):
            vals['xml_id'] = self._context.get('xml_id')

        obj = super(production_change_shifts, self).create(vals)

        return obj

    def get_position_domain(self):
        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            position_domain = ('production_state', 'in',
                               ['station_master', 'train_working', 'passenger_transport', 'station_service',
                                'ticket_booth'])
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车值班员
            position_domain = ('production_state', 'in',
                               [ 'train_working', 'passenger_transport'])
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            position_domain = ('production_state', 'in',['passenger_transport'])
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            # 站台 站务
            position_domain = ('production_state', 'in',['ticket_booth','station_service'])
        else:
            # 票务
            position_domain = ('production_state', 'in',['ticket_booth'])

        return position_domain

    def get_form_id(self):
        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            form_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_form').id
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车
            form_views = self.env.ref('funenc_xa_station.production_change_train_working_shifts_form11').id
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            form_views = self.env.ref('funenc_xa_station.passenger_transport_train_working_shifts_form11').id
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            form_views = self.env.ref('funenc_xa_station.station_service_form').id
        else:
            # 票务
            form_views = self.env.ref('funenc_xa_station.station_service_form').id

        return form_views

    def station_detail(self):
        context = dict(self.env.context or {})

        form_views = self.xml_id

        return {
            'name': '操作说明',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.production_change_shifts",
            "res_id": self.id,
            "views": [[form_views, "form"]],
            # "domain": [()],
            'target': 'new',
            'context': context,
        }

        # return {
        #     'name': '交接班详情',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'funenc_xa_station.production_change_shifts',
        #     'views': [[form_views, 'from']],
        #     'context': context,
        #     'flags': {'initial_mode': 'edit'},
        #     'target': 'new',
        #     'res_id': self.id
        # }

    @api.model
    def handle_delete(self,id_delete):
        obj = self.search([('id', '=', id_delete)])
        if obj.state == 'draft' or self.env.user.id ==1:
            return obj.unlink()
        else:
            return False


class put_question(models.Model):
    _name = 'funenc_xa_station.put_question'
    _description = u'班前提问'

    put_question_name = fields.Char(string='提问姓名')
    examination_questions = fields.Char(string='题目')
    score = fields.Char(string='分数')
    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')


class preparedness_6(models.Model):
    _name = 'funenc_xa_station.preparedness_6'
    _description = u'备品交接班中间表'

    shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    name = fields.Char(string='备品名称')
    save_name = fields.Char('')
    unit = fields.Char(string='单位')
    save_unit = fields.Char('')
    # type = fields.Selection(selection=KEY,related='station_master_id.type' ,string='备品类型')
    count = fields.Integer(string='数量')
    state = fields.Selection(selection=[('fine', '良好'), ('abnormity', '异常')], default="fine")
    remarks = fields.Text(string='备注')
    list_situation = fields.Char(string='清单情况')
    exceptional_situation = fields.Char(string='异常情况')

class preparedness_7(models.Model):
    _name = 'funenc_xa_station.preparedness_7'
    _description = u'备品交接班中间表'

    shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    name = fields.Char(string='备品名称')
    save_name = fields.Char('')
    unit = fields.Char(string='单位')
    save_unit = fields.Char('')
    count = fields.Integer(string='数量')
    state = fields.Selection(selection=[('fine', '良好'), ('abnormity', '异常')], default="fine")
    remarks = fields.Char(string='备注')


class check_project_to_production_change_shifts(models.Model):
    _name = 'funenc_xa_station.check_project_to_production_change_shifts'
    _description = u'运营前检查交接班中间表'

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
    check_project_id = fields.Many2one('funenc_xa_station.check_project', string='运营前检查')

    check_situation = fields.Char(string='检查情况')
    check_time = fields.Datetime(string='检查时间')


class spare_gold(models.Model):
    _name = 'funenc_xa_station.spare_gold'
    _description = '备用金配出'

    obj = fields.Char(string='本班配出备用金(对象)')
    match_out = fields.Char(string='本班配出纸币')
    coin = fields.Char(string='本班配出硬币')
    be_on_duty = fields.Char(string='值班员')
    station_master = fields.Char(string='值班站长/售票员')
    recovery = fields.Char(string='本班回收纸币')
    recovery_coin = fields.Char(string='本班回收硬币')
    depot = fields.Char(string='站务人员/售票员')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')


class tail_box(models.Model):
    _name = 'funenc_xa_station.tail_box'
    _description = '库包/尾箱交接'

    tail_box = fields.Char(string='库包/尾箱送交时间')
    no = fields.Char(string='库包/尾箱送交编号')
    count = fields.Char(string='库包/尾箱送交数量')
    time = fields.Char(string='库包/尾箱接收时间')
    tail_box_no = fields.Char(string='库包/尾箱接收编号')
    tail_box_count = fields.Char(string='库包/尾箱接收数量')
    number = fields.Char(string='库包/尾箱结存数量')
    other = fields.Char(string='其他情况')

    production_change_shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')
