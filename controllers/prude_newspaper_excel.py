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


class CheckRecord(http.Controller):
    @http.route('/funenc_xa_station/prude_newspaper', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'prode_newpaper_exel.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        ding_user = request.env.user.dingtalk_user
        site = ding_user.user_property_departments.id
        records = request.env['funenc_xa_station.prude_newspaper'].search([('site_id','=',site)]) #获取当前线路的日报记录
        if len(records) > 0:
            for record in records:
                if record.line_id.name:
                    worksheet.write(row, 0, record.line_id.name)
                else:
                    worksheet.write(row, 0, '')
                if record.site_id.name:
                    worksheet.write(row, 1, record.site_id.name)
                else:
                    worksheet.write(row, 1, "")
                if record.event_stype:
                    if record.event_stype == 'enter_come':
                        event_stype = '边门进出情况'
                    elif record.event_stype == 'ticket_acf':
                        event_stype = '票务、AFC故障及异常情况'
                    elif record.event_stype == 'ticket_sales':
                        event_stype = '日票、预制单程票售卖情况'
                    elif record.event_stype == 'other_brenk':
                        event_stype = '其他设备故障情况'
                    elif record.event_stype == 'normal':
                        event_stype = '普通事件'
                    worksheet.write(row, 2, record.event_stype.prude_event_type)
                else:
                    worksheet.write(row, 2, "")
                if record.event_content:
                    worksheet.write(row, 3, record.event_content)
                else:
                    worksheet.write(row, 3, "")
                if record.open_time:
                    d = datetime.datetime.strptime(record.open_time, '%Y-%m-%d %H:%M:%S')
                    delta = datetime.timedelta(hours=8)
                    open_time = d +delta
                    worksheet.write(row, 4,open_time.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    worksheet.write(row, 4, "")
                if record.write_time:
                    worksheet.write(row, 5, record.write_time)
                else:
                    worksheet.write(row, 5, '')
                if record.write_name:
                    worksheet.write(row, 6, record.write_name)
                else:
                    worksheet.write(row, 6, "")
                if record.iobnumber:
                    worksheet.write(row, 7, record.iobnumber)
                else:
                    worksheet.write(row, 7, "")
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