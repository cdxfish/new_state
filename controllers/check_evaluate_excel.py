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


class CheckRecord(http.Controller):
    @http.route('/funenc_xa_station/check_evaluate', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'check_evaluta.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        name = '考评指标' + str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + 'check_record.xls'
        print(file)
        wtbook.save(file)
        with open(file, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        # os.remove(file)
        return response
        # os.remove(wtbook)

        # 直接返回byte[] 或 返回  str(data)、response
        # return data