# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from ..get_domain import get_domain

class PrudeNewpaper(models.Model):
    _name = 'funenc_xa_station.prude_newpaper_type'
    _rec_name = 'prude_event_type'
    prude_event_type = fields.Char(string='生产事件类型')
    c_type=fields.Char(string='区分')
    note = fields.Char(string='备注')


    def prude_newpaper_type_selete(self):
        self.env['funenc_xa_station.prude_newpaper_type'].search([('id','=',self.id)]).unlink()


    def prude_newpaper_type_onchange(self):
        return {
            'name': '生产事件类型设置',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.prude_newpaper_type',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    @get_domain
    @api.model
    def fixed_model(self, domain):
        print(domain)
        value =[
            {'prude_event_type':'边门进出情况','note':'','c_type':'1'},
            {'prude_event_type':'票务、AFC故障及异常情况','note':'','c_type':'2'},
            {'prude_event_type':'日票、预制单程票售卖情况','note':'','c_type':'3'},
            {'prude_event_type':'其他设备故障情况','note':'','c_type':'4'}
            ]
        for i in value:
            if not self.env['funenc_xa_station.prude_newpaper_type'].search_read([('prude_event_type','=',i['prude_event_type'])]):
                self.env['funenc_xa_station.prude_newpaper_type'].sudo().create(i)

        return {
            'name': '换班时间间隔设置',
            'type': 'ir.actions.act_window',
            "views": [[False, "tree"], [False, "form"]],
            "domain": domain,
            'res_model': 'funenc_xa_station.prude_newpaper_type',
            'target': 'current',
        }

