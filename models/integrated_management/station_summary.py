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

    @api.model
    def init_data(self):

        if self.env.user.id == 1:
            site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([
                ('department_hierarchy', '=', 3)
            ]).ids
        else:
            ding_user = self.env.user.dingtalk_user
            department_id = ding_user.departments[0]
            if department_id.department_hierarchy == 1:
                site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([
                    ('department_hierarchy', '=', 3)
                ]).ids
            elif department_id.department_hierarchy == 2:
                site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('parentid', '=', department_id.departmentId)]).ids
            else:
                view_form = self.env.ref('funenc_xa_station.statio_summary_form').id
                res_id = self.search([('site_id', '=', department_id.id)])
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