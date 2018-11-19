# -*- coding: utf-8 -*-

from odoo import  models, fields,api


class StationSummary(models.Model):
    _name = 'funenc_xa_station.station_summary'
    _inherit = 'fuenc_station.station_base'
    _rec_name = 'station_nature'

    # 车站详情
    station_nature = fields.Text(string='车站性质')
    station_position = fields.Text(string='车站位置')

    station_exit_information = fields.One2many('funenc_xa_station.station_exit_information', 'station_id',
                                               string='出口信息')
    station_map_images = fields.One2many('funenc_xa_station.station_map_images', 'station_detail_id', string='地面信息图',
                                         required=True)

    # 地面交通
    ground_environment_ids = fields.One2many('funenc_xa_station.ground_environment', 'ground_traffic_id', string='地面环境')
    bus_lines = fields.One2many('funenc_xa_station.bus_line', 'ground_traffic_id', string='交通线路表')

    # 土建结构
    essential_information_ids = fields.One2many('funenc_xa_station.essential_information', 'civil_engineering_id',
                                                string='基本信息')
    private_channel_ids = fields.One2many('funenc_xa_station.private_channel', 'civil_engineering_id', string='专用通道信息')

    # 道岔
    line_map_ids = fields.One2many('funenc_xa_station.line_map', 'line_turnout_id', string='车站线路平面图')
    turnout_ids = fields.One2many('funenc_xa_station.turnout', 'line_turnout_id', string='道岔')
    liaison_station_ids = fields.One2many('funenc_xa_station.liaison_station', 'line_turnout_id', string='联络站基本信息')
    operating_line_ids = fields.One2many('funenc_xa_station.operating_line', 'line_turnout_id', string='作业线路')

    # 消防逃生图
    exit_maps = fields.One2many('funenc_xa_station.station_exit','station_summary_id',string='消防逃生图')

    # 车站设备
    station_equipment_ids = fields.One2many('funenc_xa_station.station_equipment','station_summary_id',string='车站设备')

    # station_detail_act = fields.Selection([('one','显示'),('zero','不显示')],string='车站详情显示还是不显示',default='zero')
    # ground_traffic_act = fields.Selection([('one','显示'),('zero','不显示')],string='地面交通显示还是不显示',default='zero')
    # Civil_engineering_structure = fields.Selection([('one','显示'),('zero','不显示')],string='土建结构显示还是不显示',default='zero')
    # line_switch = fields.Selection([('one','显示'),('zero','不显示')],string='线路道岔显示还是不显示',default='zero')
    # station_equiment = fields.Selection([('one','显示'),('zero','不显示')],string='车站设备显示还是不显示',default='zero')
    # person_configuration = fields.Selection([('one','显示'),('zero','不显示')],string='人员配置显示还是不显示',default='zero')
    # Fire_escape_plan = fields.Selection([('one','显示'),('zero','不显示')],string='消防逃生图显示还是不显示',default='zero')

    @api.model
    def init_data(self):
        # station_detail_act = self.user_has_groups('funenc_xa_station.table_station_detail')
        # if station_detail_act:
        #     self.write({'station_detail_act': 'one'})
        # ground_traffic_act = self.user_has_groups('funenc_xa_station.table_ground_traffic')
        # if ground_traffic_act:
        #     self.write({'ground_traffic_act': 'one'})
        # civil_engineering_structure = self.user_has_groups('funenc_xa_station.table_civil_construction')
        # if civil_engineering_structure:
        #     self.write({'civil_engineering_structure': 'one'})
        # line_switch = self.user_has_groups('funenc_xa_station.table_line_and_turnout')
        # if line_switch:
        #     self.write({'line_switch': 'one'})
        # station_equiment = self.user_has_groups('funenc_xa_station.table_station_equipment')
        # if station_equiment:
        #     self.write({'station_equiment': 'one'})
        # person_configuration = self.user_has_groups('funenc_xa_station.table_staffing')
        # if person_configuration:
        #     self.write({'person_configuration': 'one'})
        # Fire_escape_plan = self.user_has_groups('funenc_xa_station.table_fire_escape')
        # if Fire_escape_plan:
        #     self.write({'Fire_escape_plan': 'one'})
        # print(self.search_read(),'ooooooooooooooooooooooooooooooooo')

        if self.env.user.id == 1:
            site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([
                ('department_hierarchy', '=', 3)
            ]).ids
        else:
            ding_user = self.env.user.dingtalk_user
            department_ids = ding_user.user_property_departments
            site_ids = []
            for department_id in department_ids:
                if department_id.department_hierarchy == 3:
                    site_ids.append(department_id.id)
            if len(site_ids) == 1:
                view_form = self.env.ref('funenc_xa_station.statio_summary_form').id
                res_id = self.search([('site_id', '=', site_ids[0])])
                return {
                    'name': '借用记录',
                    "type": "ir.actions.act_window",
                    "res_model": "funenc_xa_station.station_summary",
                    "views": [[view_form, "form"]],
                    'res_id': res_id.id or None
                }

        view_list = self.env.ref('funenc_xa_station.site_station_detail').id
        return {
            'name': '车站详情',
            "type": "ir.actions.act_window",
            "res_model": "cdtct_dingtalk.cdtct_dingtalk_department",
            "views": [[view_list, "tree"]],
            "domain": [('id', 'in', site_ids)],
        }
