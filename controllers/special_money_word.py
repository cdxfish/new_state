# !user/bin/env python3
# -*- coding: utf-8 -*-

import os, base64, time, codecs, shutil
from odoo import http, fields, exceptions
from datetime import datetime, timedelta
from jinja2 import FileSystemLoader, Environment

from odoo.http import request
from addons.web.controllers.main import Home, ensure_db
import logging
import werkzeug.utils
from odoo.exceptions import AccessError
import requests, re

class ModelToTable:
    tableId = 1
    id = ''
    date = ''
    rId = ''
    cx = '0'
    cy = '0'
    pic_count = 1



class SpecialMoney(http.Controller):

    @http.route('/funenc_xa_station/special_money_word', type="http", auth='public', cors="*")
    def download_excel(self, **kw):
        base_dir = os.path.dirname(__file__)
        mtdocx = ModelToTable()
        mediarelsxml = (base_dir + "/special_money_excel/word/document.xml")
        src_mediarelsxml = (base_dir + '/special_money_model/document.xml')
        if os.path.exists(mediarelsxml):
            os.remove(mediarelsxml)
        shutil.copyfile(src_mediarelsxml, mediarelsxml)
        try:
            # 开始写入模版数据
            global hellotxt
            template_xml = (base_dir + "/" + "special_money_excel/word/")
            env = Environment(loader=FileSystemLoader(template_xml), keep_trailing_newline=True)  # 创建一个包加载器对象
            template = env.get_template('document.xml')  # 获取一个模板文件
            hellotxt = template.render(object=mtdocx)  # 渲染

            f = codecs.open(mediarelsxml, 'a', 'utf-8')
            f.seek(0)
            f.truncate()
            f.write(hellotxt)
            f.close()

            str_datetime = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
            docx_name = (str(str_datetime) + 'study' + '.docx')

            shutil.make_archive((base_dir + '/' + docx_name), 'zip', (base_dir + '/special_money_excel'))
            # 修改为docx，删除media文件夹
            en_directory = (base_dir + '/' + docx_name)
            en_directory_zip_name = (en_directory + '.zip')
            with open(en_directory, 'rb') as tmp_file:
                data = tmp_file.read()
            response = http.request.make_response(data)
            response.headers["Content-Disposition"] = \
                "attachment; filename={}".format('学习记录表.docx'.encode().decode('latin-1'))
            if os.path.exists(en_directory):
                # 删除文件，可使用以下两种方法。
                os.remove(en_directory)
            return response

        except Exception as err:
            print(err)