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

APP_DIR = os.path.dirname(os.path.dirname(__file__))


class BelongToManageImport(http.Controller):
    @http.route('/funenc_xa_station/belong_to_management_import', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'belong_to_management.xls')
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        records = request.env['funenc_xa_station.belong_to_management'].search([])
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
                if record.post_check:
                    if record.post_check == 'guard':
                        post_check = '保安'
                    elif record.post_check == 'check':
                        post_check = '安检'
                    elif record.post_check == 'clean':
                        post_check = '保洁'
                    worksheet.write(row, 2, post_check)
                else:
                    worksheet.write(row, 2, "")
                if record.check_time:
                    worksheet.write(row, 3, record.check_time)
                else:
                    worksheet.write(row, 3, "")
                if record.check_state:
                    worksheet.write(row, 4, record.check_state)
                else:
                    worksheet.write(row, 4, "")
                if record.find_problem:
                    worksheet.write(row, 5, record.find_problem)
                else:
                    worksheet.write(row, 5, 0)
                if record.reference_according:
                    worksheet.write(row, 6, record.reference_according)
                else:
                    worksheet.write(row, 6, "")
                if record.local_image:
                    worksheet.write(row, 7, record.local_image)
                else:
                    worksheet.write(row, 7, "")
                if record.check_score:
                    worksheet.write(row, 8, record.check_score)
                else:
                    worksheet.write(row, 8, "")
                if record.note:
                    worksheet.write(row, 9, record.note)
                else:
                    worksheet.write(row, 9, "")
                if record.write_person:
                    worksheet.write(row, 10, record.write_person)
                else:
                    worksheet.write(row, 10, "")
                row += 1
        name = str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + name
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