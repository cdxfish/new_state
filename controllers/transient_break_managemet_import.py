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
    @http.route('/funenc_xa_station/transient_break_management', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'instruments.xls')
        # print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        records = request.env['funenc_xa_station.transient_break_management'].search([])
        if len(records) > 0:
            for record in records:
                if record.transceiver_type:
                    worksheet.write(row, 0, record.transceiver_type.consumables_type)
                else:
                    worksheet.write(row, 0, '')
                if record.transceive_name:
                    worksheet.write(row, 1, record.transceive_name)
                else:
                    worksheet.write(row, 1, "")
                if record.transceive_number:
                    worksheet.write(row, 2, record.transceive_number)
                else:
                    worksheet.write(row, 2, "")
                if record.line_id:
                    worksheet.write(row, 3, record.line_id.name)
                else:
                    worksheet.write(row, 3, "")
                if record.site_id:
                    worksheet.write(row, 4, record.site_id.name)
                else:
                    worksheet.write(row, 4, "")
                if record.post:
                    worksheet.write(row, 5, record.post)
                else:
                    worksheet.write(row, 5, '')
                if record.apply_time:
                    d = datetime.datetime.strptime(record.apply_time, '%Y-%m-%d %H:%M:%S')
                    delta = datetime.timedelta(hours=8)
                    open_time = d +delta
                    worksheet.write(row, 6,open_time.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    worksheet.write(row, 6, "")
                if record.break_describe:
                    worksheet.write(row, 7, record.break_describe)
                else:
                    worksheet.write(row, 7, "")
                if record.state:
                    if record.state == 'zero':
                        kind = '未处理'
                    elif record.state == 'one':
                        kind = '已修复'
                    worksheet.write(row, 8, kind)
                else:
                    worksheet.write(row, 8, "")
                if record.repair_time:
                    d = datetime.datetime.strptime(record.repair_time, '%Y-%m-%d %H:%M:%S')
                    delta = datetime.timedelta(hours=8)
                    open_time = d +delta
                    worksheet.write(row, 9,open_time.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    worksheet.write(row, 9, "")
                if record.repair_manufacturer:
                    worksheet.write(row, 10, record.repair_manufacturer)
                else:
                    worksheet.write(row, 10, "")
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