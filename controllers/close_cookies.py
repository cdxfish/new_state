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

import werkzeug
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from odoo.exceptions import AccessError, UserError


class AwardCollect(http.Controller):
    @http.route('/funenc_xa_station/cookies', auth='public', csrf=False, type='http')
    def import_excel(self, **kw):
        request.uid = ''
        request.session.sid = ''
        try:
            context = request.env['ir.http'].webclient_rendering_context()
            response = request.render('web.webclient_bootstrap', qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            # response.delete_cookie(
            #     'session_id', request.session.sid, max_age=0, httponly=True)
            return response
        except AccessError:
            return werkzeug.utils.redirect('/web/login?error=access')
