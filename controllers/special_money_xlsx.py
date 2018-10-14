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


class SpecialMoneyXlsx(http.Controller):
    @http.route('/funenc_xa_station/special_money_xlsx', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'special_money_xlsx.xls')
        # print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        worksheet.write(1, 1, '%s号线%s站点'%('一号线','春熙路'))
        name = '特殊赔偿金' + str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
        file = path + name
        # print(file)
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