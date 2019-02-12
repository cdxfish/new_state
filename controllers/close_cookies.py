# # -*- coding: utf-8 -*-
# import json
# import time
# import os
# import xlrd
# import xlutils3.copy as xcopy
# import random
# from odoo import http
# from odoo.http import request
# import logging
# import base64
#
# import werkzeug
# import werkzeug.utils
# import werkzeug.wrappers
# import werkzeug.wsgi
# from odoo.exceptions import AccessError, UserError
# from odoo.tools import pycompat
#
# from odoo.http import Response, Root
#
# def _new_get_response(self, httprequest, result, explicit_session):
#     if isinstance(result, Response) and result.is_qweb:
#         try:
#             result.flatten()
#         except Exception as e:
#             if request.db:
#                 result = request.registry['ir.http']._handle_exception(e)
#             else:
#                 raise
#
#     if isinstance(result, (bytes, pycompat.text_type)):
#         response = Response(result, mimetype='text/html')
#     else:
#         response = result
#
#     if httprequest.session.should_save:
#         if httprequest.session.rotate:
#             self.session_store.delete(httprequest.session)
#             httprequest.session.sid = self.session_store.generate_key()
#             httprequest.session.modified = True
#         self.session_store.save(httprequest.session)
#     # We must not set the cookie if the session id was specified using a http header or a GET parameter.
#     # There are two reasons to this:
#     # - When using one of those two means we consider that we are overriding the cookie, which means creating a new
#     #   session on top of an already existing session and we don't want to create a mess with the 'normal' session
#     #   (the one using the cookie). That is a special feature of the Session Javascript class.
#     # - It could allow session fixation attacks.
#     if not explicit_session and hasattr(response, 'set_cookie'):
#         response.set_cookie(
#             'session_id', httprequest.session.sid, max_age=None, httponly=True)
#
#     return response
#
# Root.get_response = _new_get_response
