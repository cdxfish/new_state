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


class CheckAward(http.Controller):
    @http.route('/funenc_xa_station/award_record_excel', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'award_record.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        records = request.env['funenc_xa_station.award_record'].search([])
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
                if record.jobnumber:
                    worksheet.write(row, 2, record.jobnumber)
                else:
                    worksheet.write(row, 2, "")
                if record.staff.name:
                    worksheet.write(row, 3, record.staff.name)
                else:
                    worksheet.write(row, 3, "")
                if record.position:
                    worksheet.write(row, 4, record.position)
                else:
                    worksheet.write(row, 4, "")
                if record.award_money:
                    worksheet.write(row, 5, record.award_money)
                else:
                    worksheet.write(row, 5, 0)
                if record.award_target_kind:
                    worksheet.write(row, 6, record.award_target_kind)
                else:
                    worksheet.write(row, 6, "")
                if record.award_project:
                    worksheet.write(row, 7, record.award_project)
                else:
                    worksheet.write(row, 7, "")
                if record.check_project:
                    worksheet.write(row, 8, record.check_project)
                else:
                    worksheet.write(row, 8, "")
                if record.incident_describe:
                    worksheet.write(row, 9, record.incident_describe)
                else:
                    worksheet.write(row, 9, "")
                if record.check_person:
                    worksheet.write(row, 10, record.check_person)
                else:
                    worksheet.write(row, 10, "")
                if record.check_time:
                    worksheet.write(row, 11, record.check_time)
                else:
                    worksheet.write(row, 11, "")
                row += 1
        name = str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
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