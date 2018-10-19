# !user/bin/env python3
# -*- coding: utf-8 -*-
#
# from odoo import api,models,fields
#
#
# class PersonModel(models.Model):
#     _name = 'funenc_xa_station.person_model'
#
#     default_name = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点', default=lambda self: self.default_name_id())
#
#     @api.model
#     def default_name_id(self):
#         if self.env.user.id ==1:
#             return
#
#         return self.env.user.dingtalk_user.name[0].id


