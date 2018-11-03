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


#获取到当前文件夹的目录
APP_DIR = os.path.dirname(os.path.dirname(__file__))


class SpecialMoneyXlsx(http.Controller):
    @http.route('/funenc_xa_station/break_logo', type='http', auth='public')
    def import_excel(self, **kw):

        #创建一个目录文件
        name = '标识管理' + str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xlsx'
        path = APP_DIR + '/static/excel/' + name

        # 打开模板excel文件进行读写操作
        rdbook = xlsxwriter.Workbook(path)
        worksheet = rdbook.add_worksheet()

        #创建excel表的表头
        worksheet.write(0,0,'线路')
        worksheet.write(0,1,'站点')
        worksheet.write(0,2,'位置')
        worksheet.write(0,3,'申请原因')
        worksheet.write(0,4,'故障描述')
        worksheet.merge_range(0,5,0,8,'故障图片')
        worksheet.write(0,9,'状态')
        worksheet.write(0,10,'修复时间')
        worksheet.write(0,11,'修复厂家')
        worksheet.merge_range(0,12,0,15,'修复后照片')

        #获取当前的记录内容
        record = request.env['funenc_xa_station.break_log_manage'].search([])
        row = 0
        column = 1

        #创建一个列表来存放图片
        lis = []
        for re in record:

            #获取故障图片的编码吗
            brfore_image = re.before_break_img

            #获取修复故障图片的编码
            after_image = re.after_break_img

            # 解码故障图片
            brefor_image_path = APP_DIR + '/static/excel/' + str(random.randint(1, 1000000000))+'.png'
            imgdata = base64.b64decode(brfore_image)
            file = open(brefor_image_path, 'wb')
            file.write(imgdata)
            file.close()

            #解码修复后的图片
            after_image_path = APP_DIR + '/static/excel/' + str(random.randint(1, 10000000000))+'.png'
            imgdata = base64.b64decode(after_image)
            file = open(after_image_path, 'wb')
            file.write(imgdata)
            file.close()

            #将xlsx表创建内容
            worksheet.merge_range(column,0,row+14,0,re.line_id.name)
            worksheet.merge_range(column,1,row+14,1,re.site_id.name)
            worksheet.merge_range(column,2,row+14,2,re.position)
            worksheet.merge_range(column,3,row+14,3,re.apply_time)
            worksheet.merge_range(column,4,row+14,4,re.break_details)
            worksheet.merge_range(column,5,row+14,8,'')
            worksheet.insert_image(column, 5, brefor_image_path, {'x_scale': 0.2, 'y_scale': 0.3})

            #图片存放到列表
            lis.append(brefor_image_path)

            #将审核状态转化成为汉字
            if re.state =='one':
                state = '已修复'
            else:
                state = '未修复'
            worksheet.merge_range(column,9,row+14,9,state)
            worksheet.merge_range(column,10,row+14,10,re.repair_time)
            worksheet.merge_range(column,11,row+14,11,re.repair_manufacturer)
            worksheet.merge_range(column,12,row+14,15,'')
            worksheet.insert_image(column,12,after_image_path,{'x_scale': 0.2, 'y_scale': 0.3})

            # 图片存放到列表
            lis.append(after_image_path)
            row += 15
            column += 15

        rdbook.close()
        with open(path, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(path.encode().decode('latin-1'))

        #删除表
        os.remove(path)

        #删除列表中的图片
        for li in lis:
            os.remove(li)
        return response