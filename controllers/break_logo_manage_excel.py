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
import xlsxwriter
import urllib3

APP_DIR = os.path.dirname(os.path.dirname(__file__))


class BreakLogo(http.Controller):
    @http.route('/funenc_xa_station/break_logo', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'break_logo_excel.xlsx')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        book = xlsxwriter.Workbook(path +'break_logo_excel.xlsx')
        wtbook = xcopy.copy(book)
        sheet = wtbook.add_worksheet()
        row = 1
        records = request.env['funenc_xa_station.break_log_manage'].search([])
        if len(records) > 0:
            for record in records:
                if record.line_id.name:
                    sheet.write(row, 0, record.line_id.name)
                else:
                    sheet.write(row, 0, '')
                if record.site_id.name:
                    sheet.write(row, 1, record.site_id.name)
                else:
                    sheet.write(row, 1, "")
                if record.position:
                    sheet.write(row, 2, record.position)
                else:
                    sheet.write(row, 2, "")
                if record.apply_time:
                    sheet.write(row, 3, record.apply_time)
                else:
                    sheet.write(row, 3, "")
                if record.break_details:
                    sheet.write(row, 4, record.break_details)
                else:
                    sheet.write(row, 4, "")
                if record.before_break_img:
                    # f = open(str(1) + '.jpg', "wb")  # 打开文件
                    # f.write(record.before_break_img)  # 写入文件
                    # f.close()
                    sheet.insert_image(row, 5, '/Users/wangliang666/odoo11/xa_station/funenc_xa_station/static/images/timg.jpeg')
                else:
                    sheet.write(row, 5, 0)
                if record.state:
                    if record.state == 'one':
                        target = '已修复'
                    elif record.state == 'zero':
                        target = '未处理'
                        sheet.write(row, 6, target)
                else:
                    sheet.write(row, 6, "")
                if record.repair_time:
                    sheet.write(row, 7, record.repair_time)
                else:
                    sheet.write(row, 7, "")
                if record.repair_manufacturer:
                    sheet.write(row, 8, record.repair_manufacturer)
                else:
                    sheet.write(row, 8, "")
                if record.after_break_img:
                    sheet.write(row, 9, record.after_break_img)
                else:
                    sheet.write(row, 9, "")
                row += 1
        name =  str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xlsx'
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