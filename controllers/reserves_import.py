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


class CheckCollect(http.Controller):
    @http.route('/fuenc_xa_station/reserves_download', auth='public', csrf=False, type='http')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # arr_data = kwargs['arr_data']
        json_data = json.loads(request.httprequest.data.decode())
        arr_data = json_data['reserves']
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'reserves_management.xls')
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)

        # 表头
        row = 1
        if len(arr_data) > 0:
            for record in arr_data:
                worksheet.write(row, 0, record['line_id'][1])
                worksheet.write(row, 1, record['site_id'][1])
                worksheet.write(row, 2, record['r_date'])
                worksheet.write(row, 3, record['traffic_money'])
                worksheet.write(row, 4, record['bank_Paper'])
                worksheet.write(row, 5, record['bank_COINS'])
                worksheet.write(row, 6, record['day_standby_money'])
                worksheet.write(row, 7, record['temporary_standby_money'])
                worksheet.write(row, 8, record['financial_temporary_money'])
                worksheet.write(row, 9, record['machine_money'])
                worksheet.write(row, 10, record['counterfeit'])
                worksheet.write(row, 11, record['imperfect_money'])
                worksheet.write(row, 12, record['Foreign_currency'])
                worksheet.write(row, 13, record['less_money'])
                worksheet.write(row, 14, record['subtotal'])
                worksheet.write(row, 15, record['more_money'])
                worksheet.write(row, 16, record['return_money'])
                worksheet.write(row, 17, record['return_money_date'])
                worksheet.write(row, 18, record['bank_return_money'])
                worksheet.write(row, 19, record['bank_return_date'])
                worksheet.write(row, 20, record['day_day_standby'])
                worksheet.write(row, 21, record['day_day_standby_subtraction'])
                worksheet.write(row, 22, record['note'])
                worksheet.write(row, 23, record['Person_charge_account'])
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