# -*- coding: utf-8 -*-
from odoo import http

# class FuencStation(http.Controller):
#     @http.route('/fuenc_station/fuenc_station/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fuenc_station/fuenc_station/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fuenc_station.listing', {
#             'root': '/fuenc_station/fuenc_station',
#             'objects': http.request.env['fuenc_station.fuenc_station'].search([]),
#         })

#     @http.route('/fuenc_station/fuenc_station/objects/<model("fuenc_station.fuenc_station"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fuenc_station.object', {
#             'object': obj
#         })