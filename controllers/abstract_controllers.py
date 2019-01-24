# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import os

class AbstractControllers(http.Controller):

    @http.route('/funenc_xa_station/abstract/export_excel', type='http', auth='public')

    def export_excel(self, **kw):
        file = kw.get('file')
        name = kw.get('name')
        with open(file, 'rb') as f:
            data = f.read()
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        os.remove(file)

        return response
