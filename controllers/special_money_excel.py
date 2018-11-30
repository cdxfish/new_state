# -*- coding: utf-8 -*-
import time
import os
import xlrd
import xlutils3.copy as xcopy
import random
from odoo import http
from odoo.http import request
import logging
import base64
import datetime

APP_DIR = os.path.dirname(os.path.dirname(__file__))


class SpecialMoneyExcel(http.Controller):
    @http.route('/funenc_xa_station/special_money', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'special_money_excel.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        site = request.env['cdtct_dingtalk.cdtct_dingtalk_department'].get_line_or_def_site()
        site_id_self = [sites.get('id') for sites in site.get('site_options')]
        records = request.env['funenc_xa_station.special_money'].search([('site_id','=',site_id_self)])
        if len(records) > 0:
            for record in records:
                if record.id:
                    worksheet.write(row, 0, record.id)
                else:
                    worksheet.write(row, 0, '')
                if record.line_id.name:
                    worksheet.write(row, 1, record.line_id.name)
                else:
                    worksheet.write(row, 1, '')
                if record.site_id.name:
                    worksheet.write(row, 2, record.site_id.name)
                else:
                    worksheet.write(row, 2, "")
                if record.open_time:
                    d = datetime.datetime.strptime(record.open_time, '%Y-%m-%d %H:%M:%S')
                    delta = datetime.timedelta(hours=8)
                    open_time = d + delta
                    worksheet.write(row, 3, open_time.strftime('%Y-%m-%d %H:%M:%S'))
                    # worksheet.write(row, 3, record.open_time)
                else:
                    worksheet.write(row, 3, "")
                if record.event_type:
                    if record.event_type == 'money':
                        event_type = '非及时退款'
                    elif record.event_type == 'deal':
                        event_type = '事务处理'
                    worksheet.write(row, 4, event_type)
                else:
                    worksheet.write(row, 4, "")
                if record.involving_money:
                    worksheet.write(row, 5, record.involving_money)
                else:
                    worksheet.write(row, 5, 0)
                if record.passengers_name:
                    worksheet.write(row, 6, record.passengers_name)
                else:
                    worksheet.write(row, 6, "")
                if record.webmaster:
                    worksheet.write(row, 7, record.webmaster)
                else:
                    worksheet.write(row, 7, "")
                if record.write_time:
                    d = datetime.datetime.strptime(record.write_time, '%Y-%m-%d %H:%M:%S')
                    delta = datetime.timedelta(hours=8)
                    open_time = d + delta
                    worksheet.write(row, 8, open_time.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    worksheet.write(row, 8, "")
                if record.deal_result:
                    if record.deal_result == 'one_audit':
                        kind = '待初核'
                    elif record.deal_result == 'two_audit':
                        kind = '待复核'
                    elif record.deal_result == 'through':
                        kind = '已通过'
                    elif record.deal_result == 'rejected':
                        kind = '已驳回'
                    worksheet.write(row, 9, kind)
                else:
                    worksheet.write(row, 9, "")
                row += 1
        name =  str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + name
        print(file)
        wtbook.save(file)
        with open(file, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        os.remove(file)
        return response
        # os.remove(wtbook)

        # 直接返回byte[] 或 返回  str(data)、response
        # return data