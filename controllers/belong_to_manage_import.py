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


APP_DIR = os.path.dirname(os.path.dirname(__file__))


class SpecialMoneyXlsx(http.Controller):
    @http.route('/funenc_xa_station/break_logo', type='http', auth='public')
    def import_excel(self, **kw):
        name = '特殊赔偿金' + str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xlsx'
        path = APP_DIR + '/static/excel/' + name

        # 打开模板excel文件进行读写操作
        rdbook = xlsxwriter.Workbook(path)
        worksheet = rdbook.add_worksheet()
        # print(rdbook)
        # 复制模板
        # wtbook = xcopy.copy(rdbook)
        # worksheet = wtbook.get_sheet(0)

        worksheet.merge_range(0,0,1,12,'特殊赔偿金')
        worksheet.merge_range(2,0,3,12,'_____线路______站______班次  _____年____月____日')
        worksheet.merge_range(4, 0, 9, 2,'事件详情' )
        worksheet.merge_range(4, 3, 9, 12, '')
        worksheet.merge_range(10, 0, 15, 2, '处理结果')
        worksheet.merge_range(10, 3, 15, 12, '')
        worksheet.merge_range(16, 0, 21, 2, '申请原因')
        worksheet.merge_range(16, 3, 21, 12, '')
        worksheet.merge_range(22, 0, 27, 2, '乘客生份证')
        worksheet.merge_range(22, 3, 27, 12,'乘客生份证')
        worksheet.insert_image(22, 3, '', {'x_scale': 0.4, 'y_scale': 0.1})
        worksheet.merge_range(28, 0, 30, 2, '涉及金额')
        worksheet.merge_range(28, 3, 30, 4, '')
        worksheet.merge_range(28, 5, 30, 6, '乘客姓名')
        worksheet.merge_range(28, 7, 30, 8, '')
        worksheet.merge_range(28, 9, 30, 10, '乘客电话')
        worksheet.merge_range(28, 11, 30, 12, '')
        worksheet.merge_range(31, 0, 33, 2, '站长')
        worksheet.merge_range(31, 3, 33, 4, '')
        worksheet.merge_range(31, 5, 33, 6, '分部主任')
        worksheet.merge_range(31, 7, 33, 8, '')
        worksheet.merge_range(31, 9, 33, 10, '部门领导')
        worksheet.merge_range(31, 11, 33, 12, '')
        rdbook.close()
        with open(path, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(path.encode().decode('latin-1'))
        os.remove(path)
        return response
        os.remove(wtbook)

        # 直接返回byte[] 或 返回  str(data)、response
        # return data