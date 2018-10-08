import odoo.exceptions as msg
from odoo import models, fields, api


class ConsumablesType(models.Model):
    _name = 'funenc_xa_station.consumables_type'
    _inherit = 'fuenc_station.station_base'
    _description = u'耗材分类'
    _rec_name = 'consumables_type'

    consumables_type = fields.Char('耗材分类',required= True)
    prent_id = fields.Many2one('funenc_xa_station.consumables_type',string='父耗材分类')
    child_ids = fields.One2many('funenc_xa_station.consumables_type', 'prent_id', string='子耗材分类')
