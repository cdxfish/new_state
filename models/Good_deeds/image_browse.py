from datetime import datetime
from odoo import api,models,fields
import requests
import urllib
import base64


class ImageBrowse(models.Model):
    _name = 'image_browse_model'

    image_browse = fields.Binary(string='文件')
    blong_to_manage = fields.Many2one('funenc_xa_station2.belong_to_management',string='对应属地管理的图片')
