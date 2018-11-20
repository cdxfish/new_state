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


class ModelToDocx:
    event_details = ''
    deal_result = ''
    apply_reason = ''
    id_card = ''
    money =''

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
        id_id = kw.get('id')
        record = request.env['funenc_xa_station.special_money'].search([('id','=',int(id_id))])
        base_dir = os.path.dirname(__file__)
        mtdocx = ModelToDocx()
        mtdocx.event_details = record.event_details
        if record.deal_result=='one_audit':
            mtdocx.deal_result ='待初核'
        elif record.deal_result=='two_audit':
            mtdocx.deal_result = '待复审'
        elif record.deal_result=='through':
            mtdocx.deal_result = '通过'
        elif record.deal_result=='rejected':
            mtdocx.deal_result = '已驳回'
        mtdocx.money = record.involving_money
        mtdocx.apply_reason = record.apply_why
        media = base_dir + '/special_money_excel/word/media'
        shutil.rmtree(media)
        os.mkdir(media)
        png_path = media + '/image1' + ".png"
        bin_data = base64.b64decode(record.load_file_test)
        file_object = open(png_path, 'wb')
        file_object.write(bin_data)
        file_object.close()
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
            with open(en_directory_zip_name, 'rb') as tmp_file:
                data = tmp_file.read()
            response = http.request.make_response(data)
            response.headers["Content-Disposition"] = \
                "attachment; filename={}".format('特殊赔偿金退款单.docx'.encode().decode('latin-1'))
            if os.path.exists(en_directory_zip_name):
                # 删除文件，可使用以下两种方法。
                os.remove(en_directory_zip_name)
            return response

        except Exception as err:
            print(err)