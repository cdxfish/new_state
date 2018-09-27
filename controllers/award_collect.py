# -*- coding: utf-8 -*-
import json
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


class AwardCollect(http.Controller):
    @http.route('/fuenc_xa_station/award_collect_download', auth='public', csrf=False, type='http')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # arr_data = kwargs['arr_data']
        json_data = json.loads(request.httprequest.data.decode())
        arr_data = json_data['exl_data']
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'award_collect.xls')
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)

        # 表头
        row = 1
        if len(arr_data) > 0:
            for record in arr_data:
                worksheet.write(row, 0, record['line_id'])
                worksheet.write(row, 1, record['site_id'])
                worksheet.write(row, 2, record['jobnumber'])
                if record['position']:
                    worksheet.write(row, 3, record['position'])
                else:
                    worksheet.write(row, 3, "")
                worksheet.write(row, 4, record['award_money'])
                worksheet.write(row, 5, record['comment_count'])
                row += 1

        name = str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + name
        wtbook.save(file)

        with open(file, 'rb') as f:
            data = f.read()

        # response = request.make_response(data)
        # response.headers["Content-Disposition"] = "attachment; filename={}{}". \
        #     format(year.encode().decode('latin-1'), '年维修计划表.xls'.encode().decode('latin-1'))

        os.remove(file)

        # 直接返回byte[] 或 返回  str(data)、response
        return data