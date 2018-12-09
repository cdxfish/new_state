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
    signal_machine_ids = fields.One2many('funenc_xa_station.signal_machine','station_summary_id', string='信号机位置')

    # 消防逃生图
    exit_maps = fields.One2many('funenc_xa_station.station_exit','station_summary_id',string='消防逃生图')

    # 车站设备
    station_equipment_ids = fields.One2many('funenc_xa_station.station_equipment','station_summary_id',string='车站设备')

    # 人员配置
    station_summary_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'station_summary_ding_user_rel_10_20',
                                           'station_summary_id', 'ding_user_id', string='人员配置')


    @api.model
    def init_data(self):

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
                self_department_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(site_ids[0])
                site_users = self_department_id.department_property_users.ids
                view_form = self.env.ref('funenc_xa_station.statio_summary_form').id
                res_id = self.search_read([('site_id', '=', site_ids[0])],['id'])
                sql_data = []
                if res_id:
                    # 有车站详情
                    station_summary_id = res_id[0].get('id')


                else:
                    # 无车站详情
                    department_obj = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(site_ids[0])
                    line_id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('departmentId','=',department_obj.parentid)]
                    ).id
                    obj = self.create(
                        {'line_id': line_id,
                         'site_id': site_ids[0],
                         }
                    )
                    obj_read = obj.read(['id'])
                    station_summary_id = obj_read[0].get('id')
                # 车站人员
                for site_user_id in site_users:
                    user_data = []  # (station_summary_id,ding_user_id)
                    user_data.append(station_summary_id)
                    user_data.append(site_user_id)
                    sql_data.append(tuple(user_data))
                del_sql = "delete from station_summary_ding_user_rel_10_20 " \
                          "where station_summary_id = {}" \
                    .format(station_summary_id)
                self.env.cr.execute(del_sql)
                if str(sql_data)[1:-1]:
                    insert_sql = "insert into station_summary_ding_user_rel_10_20(station_summary_id,ding_user_id)" \
                                 "values{}".format(str(sql_data)[1:-1])
                    self.env.cr.execute(insert_sql)

                return {
                    'name': '车站详情',
                    "type": "ir.actions.act_window",
                    "res_model": "funenc_xa_station.station_summary",
                    "views": [[view_form, "form"]],
                    'res_id':station_summary_id
                }

        view_list = self.env.ref('funenc_xa_station.site_station_detail').id
        return {
            'name': '车站详情',
            "type": "ir.actions.act_window",
            "res_model": "cdtct_dingtalk.cdtct_dingtalk_department",
            "views": [[view_list, "tree"]],
            "domain": [('id', 'in', site_ids)],
        }

    @api.model
    def clint_search(self,**kw):
        '''
        clint 搜索方法
        :param kw:
        :return:
        '''
        if kw:
            dic_department_id = {}
            # 构建搜索domain
            if kw.get('department'):
                dic_department_id[1] = kw.get('department')  #部门
            if kw.get('line'):
                dic_department_id.clear()
                dic_department_id[2] = kw.get('line')  # 线路
            if kw.get('site'):
                dic_department_id.clear()
                dic_department_id[3] = kw.get('site') # 站点
            if dic_department_id:
                department_hierarchy = list(dic_department_id.keys())[0]

                if department_hierarchy == 1:
                    department_tmp = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(dic_department_id[1])
                    line_ids =self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('parentid', '=', department_tmp.departmentId)])
                    tmp_site_ids = []
                    for line_id in line_ids:
                        site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                            [('parentid', '=', line_id.departmentId)]).ids
                        tmp_site_ids = tmp_site_ids +site_ids

                    domain_ids = [department_tmp.id] + line_ids.ids + tmp_site_ids
                    domain = [('site_id', 'in', domain_ids)]
                elif department_hierarchy == 2: #搜索为线路
                    department_tmp = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(dic_department_id[2])
                    site_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                        [('parentid', '=', department_tmp.departmentId)]).ids
                    domain_ids = [department_tmp.id] + site_ids
                    domain = [('site_id', 'in', domain_ids)]
                else: #搜索为站点

                    domain_ids = [dic_department_id[3]]
                    domain = [('site_id', 'in', domain_ids)]



            else:
                search_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('department_hierarchy', '=',3)]).ids
                domain = [('site_id','in',search_department_ids)]


            station_summary_ids = self.search(domain).ids
            station_equipments = self.nev['unenc_xa_station.station_equipment'].search_read([('station_summary_id','in',station_summary_ids)],['id','count','name'])
            # 构建测站设备数据
            station_equipment_dic = {}
            for station_equipment in station_equipments:
                station_equipment_dic[station_equipment.get('id')] = station_equipment
            table_data = []
            for key in station_equipment_dic:
                count = 0
                for station_equipment in station_equipments:
                    if key == station_equipment.get('id'):
                        count = count + station_equipment.get('count')
                table_data.append({
                    'equipment_fname':station_equipment_dic[key].get('name')
                    'equipment_count':count
                }
                )

            return table_data
        else:
            return []

