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
    @http.route('/funenc_xa_station/test_test', type='http', auth='public')
    def import_excel(self, **kw):
        id_id = kw.get('id')
        record = request.env['xian_metro.xian_metro'].search([('id','=',int(id_id))])
        image = record.details
        if image:
            image_path = APP_DIR + '/static/excel/' + str(random.randint(1, 1000000))+'.pdf'
            imgdata = base64.b64decode(image)
            file = open(image_path, 'wb')
            file.write(imgdata)
            file.close()

        with open(image_path, 'rb') as f:
            data = f.read()
        name = '规章制度'+str(random.randint(1, 1000000))+str(id_id)+'.pdf'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        os.remove(image_path)
        return response

        # 直接返回byte[] 或 返回  str(data)、response
        # return data