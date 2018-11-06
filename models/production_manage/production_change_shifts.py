# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api
import datetime
from ..get_domain import get_domain

KEY = [('station_master', '站长'),
       ('train_working', '行车'),
       ('station_service', '站务'),
       ('ticket_booth', '票亭'),
       ('passenger_transport', '客运'),
       ]


class production_change_shifts(models.Model):
    _name = 'funenc_xa_station.production_change_shifts'
    _inherit = 'fuenc_station.station_base'
    _description = u'生产管理交接班'

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

    @api.model
    def get_views(self):
        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            list_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list')
            form_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_form')
            domain = [('production_state', '=', 'station_master')]
            # 值班站长
            return {
                'list_views': list_views,
                'form_views': form_views,
                'domain': domain
            }
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车
            list_views = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list')
            form_views = self.env.ref('funenc_xa_station.production_change_train_working_shifts_form11')
            domain = [('production_state', '=', 'train_working')]
            return {
                'list_views': list_views,
                'form_views': form_views,
                'domain': domain
            }
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
            form_views = self.env.ref('funenc_xa_station.station_service_form')
            domain = [('production_state', '=', 'station_service')]
            return {
                'list_views': list_views,
                'form_views': form_views,
                'domain': domain
            }
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
            form_views = self.env.ref('funenc_xa_station.passenger_transport_train_working_shifts_form11')
            domain = [('production_state', '=', 'passenger_transport')]
            return {
                'list_views': list_views,
                'form_views': form_views,
                'domain': domain
            }
        else:
            # 票务
            list_views = self.env.ref('funenc_xa_station._production_change_shifts_list')
            form_views = self.env.ref('funenc_xa_station.station_service_form')
            domain = [('production_state', '=', 'ticket_booth')]
            return {
                'list_views': list_views,
                'form_views': form_views,
                'domain': domain
            }

    @api.onchange('preparedness_2_ids')
    def onchange_preparedness_2_ids(self):
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

    @api.onchange('prefabricate_ticket_type_2_ids')
    def onchange_prefabricate_ticket_type_2_ids(self):
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

    @api.onchange('ticketing_key_type_2_ids')
    def onchange_ticketing_key_type_2_ids(self):
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

    ticketing_key_type_2_ids = fields.One2many('funenc_xa_station.ticketing_key_type_2', 'production_change_shifts_id',
                                               string='票务钥匙使用情况')

    prefabricate_ticket_type_2_ids = fields.One2many('funenc_xa_station.prefabricate_ticket_type_2',
                                                     'production_change_shifts_id', string='车票使用情况')
    preparedness_2_ids = fields.One2many('funenc_xa_station.preparedness_2', 'production_change_shifts_id')

    production_state = fields.Selection(selection=KEY, string='记录状态',
                                        default=lambda self: self.default_production_state())  #
    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', stirng='交班人',
                                            default=lambda self: self.default_user())
    take_over_from_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', stirng='接班人')
    job_no = fields.Char("工号", related='take_over_from_user_id.jobnumber')
    position = fields.Text("职位", related='take_over_from_user_id.position')
    on_duty_time = fields.Datetime(string='当班时间')
    change_shifts_time = fields.Datetime(string='交班时间')
    #####
    take_over_from_time = fields.Datetime(string='接班时间')
    state = fields.Selection(selection=[('draft', '草稿'), ('change_shifts', '待接班'), ('take_over_from', '已接班')],
                             default="draft")

    # 值班站长
    # 工作情况字段
    anticipation_security = fields.Text(string='安全预想')
    before_on_duty = fields.Text(string='班前情况')
    put_question_ids = fields.One2many('funenc_xa_station.put_question', 'production_change_shifts_id', string='班前提问')
    meeting_ids = fields.One2many("funenc_xa_station.meeting_dateils", 'shifts_id', string='会议记录')
    my_change_ids = fields.One2many('funenc_xa_station.preparedness_6',
                                    'shifts_id', string='备品',
                                    )

    ## 票务和站务备品
    preparedness_1_ids = fields.One2many('funenc_xa_station.preparedness_1', 'production_change_shifts_id',
                                         string='票务和站务备品')

    # 班中工
    complete_task = fields.Text(stirng='当前工作完成情况')
    equipment_problem = fields.Text(string='设备设施存在的问题')
    handover = fields.Text(string='交接事项')
    after_work = fields.Text(string='班后总结')

    focus_of_handover = fields.Text(string='交接重点')

    # 行车值班员
    in_the_rough = fields.Text(string='未完成')
    production_to_train_working_ids = fields.One2many('funenc_xa_station.check_project_to_production_change_shifts',
                                                      'production_change_shifts_id',
                                                      string='运营前检查',
                                                      # default=lambda self: self.default_production()
                                                      )

    check_project_ids = fields.One2many('funenc_xa_station.train_working_2', 'production_change_shifts1_id',
                                        string='运营前检查',
                                        # default=lambda self:self.default_check_project_ids()
                                        )

    preparedness_state = fields.Selection(selection=[('正常', '正常'), ('异常', '异常')], default="正常", string='备品状态')  # 备品状态

    @api.onchange('check_project_ids')
    def onchange_check_project_ids(self):
        # 预设行车
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
        if not self.preparedness_1_ids:
            if self.env.user.has_group('funenc_xa_station.module_depot'):
                # 站务
                obj = self.env['funenc_xa_station.station_service'].search([])[0]
            else:
                # 票务
                obj = self.env['funenc_xa_station.ticket_booth'].search([])[0]
            inst_ids = obj.preparedness_ids
            default_data = []
            for inst_id in inst_ids:
                default_data.append((0, 0, {'preparedness_name': inst_id.preparedness_name, 'unit': inst_id.unit}))
            return {
                'value': {'preparedness_1_ids': default_data}
            }
        else:
            return

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

    @api.onchange('my_change_ids')
    def onchange_my_change_ids(self):
        if not self.my_change_ids:
            position = self.get_position()
            if position == 'station_master':
                station_master = self.env['funenc_xa_station.station_master'].search([])[0]
                default_data = []
                for inst_id in station_master.preparedness_ids:
                    default_data.append((0, 0, {'name': inst_id.preparedness_name, 'unit': inst_id.unit}))

                return {
                    'value': {'my_change_ids': default_data}
                }
            else:
                obj = self.env['funenc_xa_station.car_line'].search([])[0]
                inst_ids = obj.preparedness_ids
                default_data = []
                for inst_id in inst_ids:
                    default_data.append((0, 0, {'name': inst_id.preparedness_name, 'unit': inst_id.unit}))

                return {
                    'value': {'my_change_ids': default_data}
                }
        else:
            return

    @api.model
    def default_production(self):
        obj = self.env['funenc_xa_station.car_line'].search([])[0]
        inst_ids = obj.check_project_ids.ids
        default_data = []
        for inst_id in inst_ids:
            default_data.append((0, 0, {'check_project_id': inst_id}))

    @api.model
    def create_production_change_shifts(self):
        context = dict(self.env.context or {})

        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            view_form = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_form').id
            return {
                'name': '交接班创建',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.production_change_shifts',
                'context': context,
                'target': 'new',
                'flags': {'initial_mode': 'edit'},
            }
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车
            view_form = self.env.ref('funenc_xa_station.production_change_train_working_shifts_form11').id
            return {
                'name': '交接班创建',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.production_change_shifts',
                'context': context,
                'target': 'new',
                'flags': {'initial_mode': 'edit'},
            }
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            view_form = self.env.ref('funenc_xa_station.passenger_transport_train_working_shifts_form11').id
            return {
                'name': '交接班创建',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.production_change_shifts',
                'context': context,
                'target': 'new',
                'flags': {'initial_mode': 'edit'},
            }
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            # 站务
            view_form = self.env.ref('funenc_xa_station.station_service_form').id
            return {
                'name': '交接班创建',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.production_change_shifts',
                'context': context,
                'target': 'new',
                'flags': {'initial_mode': 'edit'},
            }
        else:
            # 票务
            view_form = self.env.ref('funenc_xa_station.station_service_form').id
            return {
                'name': '交接班创建',
                'type': 'ir.actions.act_window',
                "views": [[view_form, "form"]],
                'res_model': 'funenc_xa_station.production_change_shifts',
                'context': context,
                'target': 'new',
                'flags': {'initial_mode': 'edit'},
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
            take_over_from_time = fields.Datetime(string='接班时间')
            self.state = 'take_over_from'  # 已接班
            self.take_over_from_user_id = self.env.user.dingtalk_user.line_id.id
            self.take_over_from_time = datetime.datetime.now()

    def get_position(self):
        if self.env.user.has_group('funenc_xa_station.module_cstatio_nmaster'):
            # 值班站长
            position = 'station_master'
        elif self.env.user.has_group('funenc_xa_station.module_man_on_duty'):
            # 行车
            position = 'train_working'
        elif self.env.user.has_group('funenc_xa_station.module_passenger_transport'):
            # 客运
            position = 'passenger_transport'
        elif self.env.user.has_group('funenc_xa_station.module_depot'):
            # 站务
            position = 'station_service'
        else:
            # 票务
            position = 'ticket_booth'

        return position

    @api.model
    def get_change_shifts_data(self):

        position = self.get_position()
        user_dic = {
            'name': '', 'line_id': '', 'department_name': '', 'jobnumber': '', 'position': ''
        }
        if self.env.user.id == 1:
            return {
                'change_shifts_ids': '',
                'take_over_from_ids': '',
                'user': '',
                'domain': [('state','=','change_shifts')],
                'views': '',
                'jb_form': ''
            }

        ding_user = self.env.user.dingtalk_user
        department = ding_user.departments[0]
        domain = [('site_id', '=', department.id), ('production_state', '=', position),
                  ('change_shifts_user_id', '!=', ding_user.id),('state','=','change_shifts')]
        user_dic['name'] = ding_user.name
        user_dic['line_id'] = ding_user.line_id.name
        user_dic['department_name'] = ding_user.department_name
        user_dic['jobnumber'] = ding_user.jobnumber
        user_dic['position'] = ding_user.position

        change_shifts_ids = self.search_read(
            [('production_state', '=', position), ('state', 'in', ['change_shifts', 'draft']),
             ('change_shifts_user_id', '=', ding_user.id)],
            ['id', 'change_shifts_time', 'take_over_from_user_id', 'job_no',
             'take_over_from_time'])  # 待接班
        take_over_from_ids = self.search_read([('change_shifts_user_id', '=', ding_user.id),('production_state', '=', position), ('state', '=', 'take_over_from')],
                                              ['id', 'change_shifts_time', 'take_over_from_user_id', 'job_no',
                                               'take_over_from_time'])  # 已接班
        djb_tree = self.env.ref('funenc_xa_station.funenc_xa_station_production_change_shifts_list').id
        jb_form = self.get_form_id()
        return {
            'change_shifts_ids': change_shifts_ids,
            'take_over_from_ids': take_over_from_ids,
            'user': user_dic,
            'domain': domain,
            'views': djb_tree,
            'jb_form': jb_form
        }

    @api.model
    def create(self, vals):

        obj = super(production_change_shifts, self).create(vals)

        return obj

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

        form_views = self.get_form_id()

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
