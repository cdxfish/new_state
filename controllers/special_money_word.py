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

class SpecialMoney(http.Controller):

    @http.route('/funenc_xa_station/special_money_word', type="http", auth='public', cors="*")
    def index(self, **kw):
        params = http.request.params
        code = params['code']
        url = http.request.env['ir.config_parameter'].sudo().get_param('funenc_xa_station.special_money', default='')
        return http.redirect_with_hash(url + '?code=' + code)

    # 查看学习情况报表
    @http.route('/learn_history/objects/<model("cdtct.learn_tasks"):obj>/', auth='public')
    def viewLearNote(self, obj, **kw):
        xml_id = 'funenc_xa_station.special_money'
        return http.request.render(xml_id, {
            'object': obj,
        })

    @http.route('/learn_history/download_note/<model("cdtct.learn_tasks"):obj>/', type='http', auth='user')
    def download_excel(self, obj, **kw):

        learn_task_id = obj.id
        request = http.request
        department_name = kw['departmentName']

        # tid = kw["tid"]
        # record = http.request.env["cdtct.download_his"].search([('id', '=', tid)])
        # data = record.read()
        # departments = data[0]["departments"]
        # departments = departmentName
        # records = http.request.env["cdtct.learn_note"].search([('task_id', '=', learn_task_id),('departments', 'in', departments)])
        records = http.request.env["cdtct.learn_note"].search([('task_id', '=', learn_task_id)])
        if len(records) == 0:
            raise exceptions.Warning("没有可导入的内容")

        base_dir = os.path.dirname(__file__)
        mtdocx = ModelToDocx()
        # mtdocx.docx_list = []
        # task = http.request.env['cdtct.learn_tasks'].sudo().browse(learn_task_id)
        # # 给对象属性赋值
        # mtdocx.docx_filename = task.excel_file_name
        # mtdocx.docx_filenum = task.excel_fil_num
        # mtdocx.docx_department = department_name
        # cur_type_name = task.type.name
        # mtdocx.docx_summary = ''
        # # types = http.request.env['cdtct.learn_type'].sudo().search_read(domain=[], fields=['name'])
        # if cur_type_name == '传阅':
        #     mtdocx.chuanyue = '☑传阅'
        #     mtdocx.taolun = '□讨论'
        #     mtdocx.huiyi = '□会议宣贯'
        #     mtdocx.qita = '□其它'
        # elif cur_type_name == '讨论':
        #     mtdocx.chuanyue = '□传阅'
        #     mtdocx.taolun = '☑讨论'
        #     mtdocx.huiyi = '□会议宣贯'
        #     mtdocx.qita = '□其它'
        # elif cur_type_name == '会议宣贯':
        #     mtdocx.chuanyue = '□传阅'
        #     mtdocx.taolun = '□讨论'
        #     mtdocx.huiyi = '☑会议宣贯'
        #     mtdocx.qita = '□其它'
        # elif cur_type_name == '其他（请注明）':
        #     mtdocx.chuanyue = '□传阅'
        #     mtdocx.taolun = '□讨论'
        #     mtdocx.huiyi = '□会议宣贯'
        #     mtdocx.qita = '☑其它'
        #     mtdocx.docx_summary = task.summary
        # # □传阅 □讨论  □会议宣贯  □其它
        #
        # try:
        #     # media文件夹存放图片资源,每次导出前生先删除文件夹里的内容，再创建空的文件夹
        #     media = base_dir + '/studydocx/word/media'
        #     if os.path.isdir(media) is True:
        #         shutil.rmtree(media)
        #         os.mkdir(media)
        #     else:
        #         os.mkdir(media)
        #     mediarels = (base_dir + "/studydocx/word/_rels/document.xml.rels")
        #     src_mediarels = (base_dir + '/studymoban/document.xml.rels')
        #
        #     # 存放图片引用地址的xml文件，还是先删除再复制新的模版
        #     if os.path.exists(mediarels):
        #         os.remove(mediarels)
        #     shutil.copyfile(src_mediarels, mediarels)
        #
        #     # 删除原始document.xml，再复制新的模版
        mediarelsxml = (base_dir + "/special_money_excel/word/document.xml")
        src_mediarelsxml = (base_dir + '/special_money_model/document.xml')
        #     if os.path.exists(mediarelsxml):
        #         os.remove(mediarelsxml)
        #     shutil.copyfile(src_mediarelsxml, mediarelsxml)
        # except IOError:
        #     print('tao:文件可能被占用')
        # png_names = []
        # cx = "579500"
        # cy = "167640"
        # count = 1
        # rId = ''
        media = base_dir + '/studydocx/word/media'
        #
        # fs = open(base_dir + '/text.txt', 'a')
        # fs.write('loops record\n')
        # fs.close()
        # for record in records:
        #     if record.status != 2:
        #         continue
        #     job_id = str(record.user_id.job_no)
        #     date = datetime.strptime(record.end_tm, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        #
        #     modeltotables = ModelToTable()
        #     modeltotables.tableId = count
        #     modeltotables.id = job_id
        #     modeltotables.date = date
        #     modeltotables.cx = cx
        #     modeltotables.cy = cy
        #     modeltotables.rId = rId
        #     modeltotables.pic_count = count
        #     if record.user_id.user_sign:
        #         png_path = media + '/rId' + str(record.id) + '0' + ".png"
        #         data = record.user_id.user_sign
        #         tmp_data = str(data).split('base64,')[1].rstrip("'")
        #         bin_data = base64.b64decode(tmp_data)
        #         file_object = open(png_path, 'wb')
        #         file_object.write(bin_data)
        #         file_object.close()
        #         rId = 'rId' + str(record.id) + '0'
        #         png_names.append(rId)
        #         modeltotables.rId = rId
        #     mtdocx.docx_list.append(modeltotables)
        #     count += 1
        # # 修改图片引用的xml文件
        # mediarels = (base_dir + "/studydocx/word/_rels/document.xml.rels")
        # fp = open(mediarels, 'a')
        # for iser in range(len(png_names)):
        #     str_line = '<Relationship Id="' + png_names[
        #         iser] + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/' + \
        #                png_names[iser] + '.png"/>' + '\n'
        #     fp.flush()
        #     fp.seek(0)
        #     fp.write(str_line)
        # str_end_line = '\n</Relationships>'
        # fp.write(str_end_line)
        # fp.close()
        # # 表格总计40个数据，补充完善
        # ex_len = 40 - len(mtdocx.docx_list)
        # while ex_len > 0:
        #     modeltotables = ModelToTable()
        #     modeltotables.tableId = count
        #     modeltotables.id = ''
        #     modeltotables.date = ''
        #     modeltotables.rId = ''
        #     modeltotables.cx = 0
        #     modeltotables.cy = 0
        #     modeltotables.pic_count = count
        #     mtdocx.docx_list.append(modeltotables)
        #     ex_len -= 1
        #     count += 1
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
            # 下面的代码是传统压缩方式
            # print('zip go')
            # output_filename = (base_dir+'\\'+docx_name)
            # source_dir = base_dir+'\\studydocx\\'
            # zipf = zipfile.ZipFile(output_filename, 'w')
            # pre_len = len(os.path.dirname(source_dir))
            # print('zip for go')
            # for parent, dirnames, filenames in os.walk(source_dir):
            #     print('filenames for')
            #     for filename in filenames:
            #         pathfile = os.path.join(parent, filename)
            #         arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            #         print('zip write')
            #         zipf.write(pathfile, arcname)
            #         print('zip wirte close')
            # zipf.close()
            # print('zip cloes')

            shutil.make_archive((base_dir + '/' + docx_name), 'zip', (base_dir + '/studydocx'))
            # 修改为docx，删除media文件夹
            en_directory = (base_dir + '/' + docx_name)
            en_directory_zip_name = (en_directory + '.zip')

            # os.rename(en_directory_zip_name, en_directory)
            shutil.move(en_directory_zip_name, en_directory)
            # os.removedirs(media)  文件夹不为空，无法删除

            shutil.rmtree(media)
            # 把docx输出到浏览器
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