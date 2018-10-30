# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import base64
import xlrd

from datetime import datetime, date, time
from xlrd import xldate_as_tuple
from odoo import models, fields, api


class ImportManagement(models.Model):
    _name = 'evaluate_import'

    c_time = fields.Datetime(string="导入日期", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    xls_file = fields.Binary('文件')
    count = fields.Integer(string='新增条数', help="新增条数", readonly=True)

    @api.model
    def import_xls_bill(self):
        try:
            records = self.env['evaluate_import'].search([]).sorted(key=lambda r: r.c_time, reverse=False)
            print(records[-1].xls_file)
            data = xlrd.open_workbook(file_contents=base64.decodebytes(records[-1].xls_file))
        except IOError as err:
            print('异常: ' + err)
        except ConnectionError as err:
            print('异常:' + err)
        else:
            if len(records) == 0:
                start = 1
            else:
                # start = records[0].count + 1
                start = records[0].count + 1
            sheet_data = data.sheet_by_name(data.sheet_names()[0])
            cols5 = sheet_data.col_values(5)
            end = sheet_data.nrows


            rows = sheet_data.nrows
            cols = sheet_data.ncols
            one_sheet_content = []

            keys = ('check_standard', 'problem_kind', 'check_project','check_parment','loca_per_score',
                    'relate_per_score','station_per_score',
                    'technology_score','technology_serve', 'duty_partment',
                    'management_score', 'technology_serve_director', 'duty_director','comment'
                    )
            for i in range(1, rows):
                row_content = []
                for j in range(cols):
                    ctype = sheet_data.cell(i, j).ctype  # 表格的数据类型
                    cell = sheet_data.cell_value(i, j)
                    if ctype == 3 :
                     cell =  sheet_data.cell_value(i, j)
                    if ctype == 2 and cell % 1 == 0:  # 如果是整形
                        cell = int(cell)
                        if cell > 200 and j > 1:
                            cell = int(cell)
                    elif ctype == 3:
                        # 转成datetime对象
                        if j == 9 or 10 or 12: #转化时间格式
                            f_date = datetime(*xldate_as_tuple(cell, 0))
                            cell = f_date.strftime('%Y/%m/%d')

                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    elif ctype == 0:  # 如果是空字符串，全部赋值为0，否则无法插入float类型的字段
                        cell = ''
                    row_content.append(cell)
                    one_dict = dict(zip(keys, row_content))
                one_sheet_content.append(one_dict)

            # print(one_sheet_content)

        try:
            for i, item in enumerate(one_sheet_content):
                if item['check_standard']  == '安全管理':
                    item['check_standard'] = 'safety'
                elif item['check_standard']  == '技术管理':
                    item['check_standard'] =='technology'
                elif item['check_standard']  == '施工管理':
                    item['check_standard'] =='road'
                elif item['check_standard']  == '票务管理':
                    item['check_standard'] =='ticket'
                elif item['check_standard']  == '服务管理':
                    item['check_standard'] =='server'
                elif item['check_standard']  == '培训管理':
                    item['check_standard'] =='train'
                elif item['check_standard']  == '物资管理':
                    item['check_standard'] =='goods'
                elif item['check_standard']  == '人事绩效管理':
                    item['check_standard'] =='personnel'
                elif item['check_standard']  == '党务管理':
                    item['check_standard'] =='party'
                elif item['check_standard']  == '综合管理':
                    item['check_standard'] =='integrated'
                self.env['funenc_xa_station.check_standard'].sudo().create(item)
                self.env['evaluate_import'].search([]).unlink()

        except ConnectionError as err:
            print(err)