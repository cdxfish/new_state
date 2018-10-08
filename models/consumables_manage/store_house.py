import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.store_house'
    _inherit = 'fuenc_station.station_base'
    _description = u'仓库管理'

    name = fields.Char('仓库名称', required= True)
