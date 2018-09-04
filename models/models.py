# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class fuenc_station(models.Model):
#     _name = 'fuenc_station.fuenc_station'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


list = [
    {
        's': 1,
        'e': 2
    }, {
        's': 2,
        'e': 3
    }, {
        's': 3,
        'e': 4
    }, {
        's': 2,
        'e': 4
    }, {
        's': 4,
        'e': 5
    }, {
        's': 5,
        'e': 6
    },
]
# 123456    12456
start = [
    {
        's': 1,
        'e': 2,


    }
]
# child:[{'e': 3,'e': '4'}]
new_list = []
list_1 = [el['s'] for el in list]

length = len(start)

def func1(res,start_1):
    if not res:
        res = []
    if not start_1:
        start_1 = start
    for i in list:
        if start_1[length-1]['e'] in list_1:
            res.append(i)
    start[length-1]['child'] = res
    print(start)
    if res and len(res)!=1:
        func1(res=[],start_1=start_1)
func1(res=[],start_1=[])
