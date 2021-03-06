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


class BelongManagemnet(http.Controller):
    @http.route('/funenc_xa_station/good_deeds_summary', auth='public', csrf=False, type='http')
    def import_excel_belong_to_management(self, **kw):
        path = APP_DIR + '/static/excel/'
        # arr_data = kwargs['arr_data']
        json_data = json.loads(request.httprequest.data.decode())
        arr_data = json_data['reserves']
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'good_deeds_summary.xls')
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)

        # 表头
        row = 1
        if len(arr_data) > 0:
            for record in arr_data:
                worksheet.write(row, 0, record['good_deeds_type'])
                worksheet.write(row, 1, record['frequency'])
                row += 1

        name = str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + name
        wtbook.save(file)

        with open(file, 'rb') as f:
            data = f.read()
        os.remove(file)
        return data