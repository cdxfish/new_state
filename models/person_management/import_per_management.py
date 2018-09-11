# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import base64
import xlrd

from datetime import datetime, date, time
from xlrd import xldate_as_tuple
from odoo import models, fields, api


class ImportManagement(models.Model):
    _name = 'import.management'

    c_time = fields.Datetime(string="导入日期", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    xls_file = fields.Binary('文件')
    count = fields.Integer(string='新增条数', help="新增条数", readonly=True)

    @api.model
    def import_xls_bill(self):
        try:
            records = self.env['import.management'].search([]).sorted(key=lambda r: r.c_time, reverse=False)
            print(records[0].xls_file)
            data = xlrd.open_workbook(file_contents=base64.decodebytes(records[0].xls_file))
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
            sheet_data = data.sheet_by_name('Sheet1')
            cols5 = sheet_data.col_values(5)
            end = sheet_data.nrows


            rows = sheet_data.nrows
            cols = sheet_data.ncols
            one_sheet_content = []

            keys = ('jobnumber', 'name', 'gender','department_load','department','team_or_group_station','position',
                    'nation','idcar', 'birth','join_work_time', 'begin_time', 'become_a_regular_worker_time','phone',
                    'First_degree_major','first_degree','school_of_graduation','major','second_degree_major',
                    'second_degree','second_school_of_graduation','second_major','politics_status','native_place',
                    'native_sition','new_site','emergency_contact','staff_source','shoe_size'
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

            print(one_sheet_content)

        try:
            for i, item in enumerate(one_sheet_content):
                # staff_basic_information=self.env['person.management.sys'].sudo().create(item)
                # staff_business_information=self.env['employee.business.information'].sudo().create(
                    # {'department': item['department']}
                # )
                # print('====')
                self.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().create(item)

        except ConnectionError as err:
            print(err)