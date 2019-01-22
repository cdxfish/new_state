# -*- coding: utf-8 -*-
import datetime

import odoo.exceptions as msg
from odoo import models, fields, api
from ..get_domain import get_domain

class arrange_order(models.Model):
    '''
     班次管理
    '''

    _name = 'funenc_xa_station.arrange_order'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _description = u'班次管理'
    _order = 'sort asc'

    name = fields.Char(string='班次名称', required= True, track_visibility='onchange')
    time = fields.Char(string='班次时间', track_visibility='onchange')
    work_time = fields.Char(string='工作时长', track_visibility='onchange')   # 用于显示
    save_work_time = fields.Float(string='工作时长') #用于计算储存
    start_work_time = fields.Datetime(string='上班时间', required= True, default= lambda self: self.default_start_work_time(), track_visibility='onchange')
    end_work_time = fields.Datetime(string='下班时间', required= True, track_visibility='onchange')
    end_time_select = fields.Selection(string='下班日期',selection=[('same_day','当日'),('next_day','次日')],default='same_day', track_visibility='onchange')
    sort = fields.Integer(string='排序', default=1)
    is_vacation = fields.Integer(string='是否是休班',default=0)

    order_to_arrange_ids = fields.One2many('arrange_order_to_arrange_class_manage', 'arrange_order_id',
                                           string='排班类型')

    @get_domain
    @api.model
    def init_data(self,domain):
        context = {}
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_arrange_order_list').id
        return {
            'name': '班次管理',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.arrange_order",
            "views": [[view_tree, "tree"]],
            "domain": domain,
            'target': 'current',
            'context': context,
        }

    @api.model
    def default_start_work_time(self):
        if self.env.user.id == 1:
            return

        site_id =  self.env.user.dingtalk_user.departments[0].id
        arrange_orders = self.search([('site_id', '=', site_id)])
        lens = len(arrange_orders)
        if lens > 1:
            start_work_time = arrange_orders[lens-2].end_work_time
            return start_work_time
        else:
            return


    @api.model
    def create(self, vals):
        if vals.get('site_id'):
            site_id = vals.get('site_id')
            line_id = vals.get('line_id')
            arrange_orders = self.search([('site_id', '=', site_id)])
            if not arrange_orders:
                values = {'name': '休',
                          'site_id': site_id,
                          'line_id': line_id,
                          'sort': 10000,
                          'start_work_time': datetime.datetime.strptime('1970-1-1', '%Y-%m-%d'),
                          'end_work_time': datetime.datetime.strptime('1970-1-1', '%Y-%m-%d'),
                          'time': '00:00-23:59(当日)',
                          'work_time': '0h',
                          'is_vacation': 1

                          }

                sql = "insert into funenc_xa_station_arrange_order" \
                      "(name,site_id,line_id,sort,start_work_time,end_work_time,time,work_time,is_vacation)  " \
                      "values('{name}',{site_id},{line_id},{sort},'{start_work_time}','{end_work_time}','{time}','{work_time}',{is_vacation})".format(
                       **values
                )
                self.env.cr.execute(sql)

            else:
                lens = len(arrange_orders)
                sort =arrange_orders[lens-2].sort
                vals['sort'] = sort + 1

        return super(arrange_order,self).create(vals)

    @api.constrains('start_work_time','end_work_time')
    def compute_work_time(self):
        start_work_time = datetime.datetime.strptime(self.start_work_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)
        end_work_time = datetime.datetime.strptime(self.end_work_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)

        # seconds
        if (end_work_time- start_work_time).days < 0:
            end_time_select = '次日'
            self.end_time_select = 'next_day'
        else:
            end_time_select = '当日'
            self.end_time_select = 'same_day'
        work_time = round( (end_work_time - start_work_time).seconds / (60 * 60), 2)
        self.work_time = str(work_time) + 'h'
        self.save_work_time = work_time

        self.time = '{}-{} ({})'.format(start_work_time.strftime('%Y-%m-%d %H:%M:%S')[11:-3], end_work_time.strftime('%Y-%m-%d %H:%M:%S')[11:-3], end_time_select)





    def create_arrange_order(self):
        return {
            'name': '新增班次',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.arrange_order',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def arrange_order_edit(self):
        return {
            'name': '班次详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.arrange_order',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def arrange_order_delete(self):
        sel_sql = "select * from arrange_class_manage_arrange_order_1_ref where arrange_order_id= {}".format(self.id)
        self.env.cr.execute(sel_sql)
        select_ids = self.env.cr.dictfetchall()
        if not select_ids:
            self.env['funenc_xa_station.arrange_order'].search([('id', '=', self.id)]).unlink()

        else:
            raise msg.Warning('此班次正在使用，若要删除请不要在排班规则中使用次班次')


