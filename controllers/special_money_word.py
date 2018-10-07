# # -*- coding: utf-8 -*-
# import time
# import os
# import xlrd
# import xlutils3.copy as xcopy
# import random
# from odoo import http
# from odoo.http import request
# import logging
# import base64
# import docx
# from docx import Document
#
# APP_DIR = os.path.dirname(os.path.dirname(__file__))
#
#
# class SpecialMoneyExcel(http.Controller):
#     @http.route('/funenc_xa_station/special_money_word', type='http', auth='public')
#     def import_excel(self, **kw):
#         path = APP_DIR + '/static/excel/'
#         # 打开模板excel文件进行读写操作
#         rdbook = Document(path + '处理表001.docx')
#         tab = Document.tables
#         print(tab[1])
#         print(rdbook)
#         # 复制模板
#         for i in rdbook.paragraphs:
#             print(i.text)
#         wtbook = xcopy.copy(rdbook)
#         name =  str(int(round(time.time() * 1000))) + str(random.randint(1, 1000)) + '.docx'
#         file = path + name
#         print(file)
#         wtbook.save(file)
#         with open(file, 'rb') as f:
#             data = f.read()
#         response = request.make_response(data)
#         response.headers['Content-Type'] = 'application/vnd.ms-excel'
#         response.headers["Content-Disposition"] = "attachment; filename={}". \
#             format(name.encode().decode('latin-1'))
#         os.remove(file)
#         return response
#         # os.remove(wtbook)
#
#         # 直接返回byte[] 或 返回  str(data)、response
#         # return data