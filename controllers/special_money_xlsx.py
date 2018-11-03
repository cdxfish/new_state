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
    @http.route('/funenc_xa_station/special_money_xlsx', type='http', auth='public')
    def import_excel(self, **kw):
        id_id = kw.get('id')
        record = request.env['funenc_xa_station.special_money'].search([('id','=',int(id_id))])
        event_details = record.event_details
        if record.deal_result=='one_audit':
            deal_result ='待初核'
        elif record.deal_result=='two_audit':
            deal_result = '待复审'
        elif record.deal_result=='through':
            deal_result = '通过'
        elif record.deal_result=='rejected':
            deal_result = '已驳回'
        apply_why = record.apply_why
        image = record.load_file_test
        money = record.involving_money

        name = '特殊赔偿金' + str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xlsx'
        path = APP_DIR + '/static/excel/' + name
        image_path = ''
        if image:
            image_path = APP_DIR + '/static/excel/' + str(random.randint(1, 1000000))+'.png'
            imgdata = base64.b64decode(image)
            print(imgdata)
            file = open(image_path, 'wb')
            file.write(imgdata)
            file.close()

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
        worksheet.merge_range(4, 3, 9, 12, event_details)
        worksheet.merge_range(10, 0, 15, 2, '处理结果')
        worksheet.merge_range(10, 3, 15, 12, deal_result)
        worksheet.merge_range(16, 0, 21, 2, '申请原因')
        worksheet.merge_range(16, 3, 21, 12, apply_why)
        worksheet.merge_range(22, 0, 27, 2, '乘客生份证')
        worksheet.merge_range(22, 3, 27, 12,'乘客生份证')
        worksheet.insert_image(22, 3, image_path, {'x_scale': 0.4, 'y_scale': 0.1})
        worksheet.merge_range(28, 0, 30, 2, '涉及金额')
        worksheet.merge_range(28, 3, 30, 4, money)
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
        os.remove(image_path)
        return response
        os.remove(wtbook)

        # 直接返回byte[] 或 返回  str(data)、response
        # return data