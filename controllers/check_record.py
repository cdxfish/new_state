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
    @http.route('/fuenc_xa_station/check_download', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'check_record.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        records = request.env['funenc_xa_station.check_record'].search([])
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
                if record.job_number:
                    worksheet.write(row, 2, record.job_number)
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
                if record.sure_grede:
                    worksheet.write(row, 5, record.sure_grede)
                else:
                    worksheet.write(row, 5, 0)
                if record.check_target:
                    if record.check_target == 'safety':
                        target = '安全管理'
                    elif record.check_target == 'technology':
                        target = '技术管理'
                    elif record.check_target == 'road':
                        target = '施工管理'
                    elif record.check_target == 'ticket':
                        target = '票务管理'
                    elif record.check_target == 'server':
                        target = '服务管理'
                    elif record.check_target == 'train':
                        target = '培训管理'
                    elif record.check_target == 'goods':
                        target = '物资管理'
                    elif record.check_target == 'personnel':
                        target = '人事绩效管理'
                    elif record.check_target == 'party':
                        target = '党务管理'
                    elif record.check_target == 'integrated':
                        target = '综合管理'
                    worksheet.write(row, 6, target)
                else:
                    worksheet.write(row, 6, "")
                if record.problem_kind:
                    worksheet.write(row, 7, record.problem_kind)
                else:
                    worksheet.write(row, 7, "")
                if record.check_kind:
                    if record.check_kind == 'check_parment':
                        kind = '考核分部（室）分值'
                    elif record.check_kind == 'relate_per_score':
                        kind = '相关负责人考核分值'
                    elif record.check_kind == 'station_per_score':
                        kind = '车站站长考核分值'
                    elif record.check_kind == 'technology_score':
                        kind = '技术/职能岗考核分值'
                    elif record.check_kind == 'management_score':
                        kind = '管理岗考核分值'
                    elif record.check_kind == 'loca_per_score':
                        kind = '当事人考核分值'
                    worksheet.write(row, 8, kind)
                else:
                    worksheet.write(row, 8, "")
                if record.check_project.check_project:
                    worksheet.write(row, 9, record.check_project.check_project)
                else:
                    worksheet.write(row, 9, "")
                if record.incident_describe:
                    worksheet.write(row, 10, record.incident_describe)
                else:
                    worksheet.write(row, 10, "")
                if record.check_person:
                    worksheet.write(row, 11, record.check_person)
                else:
                    worksheet.write(row, 11, "")
                if record.check_number:
                    worksheet.write(row, 12, record.check_number)
                else:
                    worksheet.write(row, 12, "")
                if record.check_time:
                    worksheet.write(row, 13, record.check_time)
                else:
                    worksheet.write(row, 13, "")
                row += 1
        file = path + 'check_record.xls'
        print(file)
        with open(file, 'rb') as f:
            data = f.read()

        wtbook.save(file)
        with open(file, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format('考评记录.xls'.encode().decode('latin-1'))
        # os.remove(file)
        return response
        # os.remove(wtbook)

        # 直接返回byte[] 或 返回  str(data)、response
        # return data