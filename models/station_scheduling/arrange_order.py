# -*- coding: utf-8 -*-
import datetime

import odoo.exceptions as msg
from odoo import models, fields, api


class arrange_order(models.Model):
    '''
     班次管理
    '''

    _name = 'funenc_xa_station.arrange_order'
    _inherit = 'fuenc_station.station_base'
    _description = u'班次管理'
    _order = 'sort asc'

    name = fields.Char(string='班次名称', required= True)
    time = fields.Char(string='班次时间')
    work_time = fields.Char(string='工作时长')
    start_work_time = fields.Datetime(string='上班时间', required= True, default= lambda self: self.default_start_work_time())
    end_work_time = fields.Datetime(string='下班时间', required= True)
    end_time_select = fields.Selection(string='下班日期',selection=[('same_day','当日'),('next_day','次日')],default='same_day')
    sort = fields.Integer(string='排序', default=1)

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
                          'work_time': '0h'

                          }

                sql = "insert into funenc_xa_station_arrange_order" \
                      "(name,site_id,line_id,sort,start_work_time,end_work_time,time,work_time)  " \
                      "values('{name}',{site_id},{line_id},{sort},'{start_work_time}','{end_work_time}','{time}','{work_time}')".format(
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
        # 还差在使用不能删除的判断
        sel_sql = "select * from arrange_class_manage_arrange_order_1_ref where arrange_order_id= {}".format(self.id)
        self.env.cr.execute(sel_sql)
        select_ids = self.env.cr.dictfetchall()
        if not select_ids:
            self.env['funenc_xa_station.arrange_order'].search([('id', '=', self.id)]).unlink()

        else:
            raise msg.Warning('此班次正在使用，若要删除请不要在排班规则中使用次班次')


