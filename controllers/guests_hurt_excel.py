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


class GuestsHurt(http.Controller):
    @http.route('/funenc_xa_station/guests_hurt', type='http', auth='public')
    def import_excel(self, **kw):
        path = APP_DIR + '/static/excel/'
        # 打开模板excel文件进行读写操作
        rdbook = xlrd.open_workbook(path + 'guests_hurt.xls')
        print(rdbook)
        # 复制模板
        wtbook = xcopy.copy(rdbook)
        worksheet = wtbook.get_sheet(0)
        row = 1
        site = request.env['cdtct_dingtalk.cdtct_dingtalk_department'].get_line_or_def_site()
        site_id_self = [sites.get('id') for sites in site.get('site_options')]
        records = request.env['fuenc_xa_station.guests_hurt'].search([('site_id','=',site_id_self)])
        if len(records) > 0:
            for record in records:
                if record.id:
                    worksheet.write(row, 0, record.id)
                else:
                    worksheet.write(row, 0, '')
                if record.line_id.name:
                    worksheet.write(row, 1, record.line_id.name)
                else:
                    worksheet.write(row, 1, '')
                if record.site_id.name:
                    worksheet.write(row, 2, record.site_id.name)
                else:
                    worksheet.write(row, 2, "")
                if record.open_time:
                    worksheet.write(row, 3, record.open_time)
                else:
                    worksheet.write(row, 3, "")
                if record.write_person:
                    worksheet.write(row, 4, record.write_person)
                else:
                    worksheet.write(row, 4, "")
                if record.guests_name:
                    worksheet.write(row, 5, record.guests_name)
                else:
                    worksheet.write(row, 5, "")
                if record.write_time:
                    worksheet.write(row, 6, record.write_time)
                else:
                    worksheet.write(row, 6, "")
                if record.claim:
                    worksheet.write(row, 7, record.claim)
                else:
                    worksheet.write(row, 7, "")
                if record.claim_money:
                    worksheet.write(row, 8, record.claim_money)
                else:
                    worksheet.write(row, 8, "")

                if record.claim_state:
                    if record.claim_state == 'one':
                        claim_state = '是'
                    elif record.claim_state == 'zero':
                        claim_state = '否'
                    worksheet.write(row, 9, claim_state)
                else:
                    worksheet.write(row, 9, "")
                if record.audit_state:
                    if record.audit_state == 'one_audit':
                        kind = '待初核'
                    elif record.audit_state == 'two_audit':
                        kind = '待复核'
                    elif record.audit_state == 'through':
                        kind = '已通过'
                    elif record.audit_state == 'rejected':
                        kind = '已驳回'
                    worksheet.write(row, 10, kind)
                else:
                    worksheet.write(row, 10, "")
                row += 1
        name =  str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.xls'
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