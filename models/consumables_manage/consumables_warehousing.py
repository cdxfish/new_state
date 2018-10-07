import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_warehousing'
    _inherit = 'fuenc_station.station_base'
    _description = u'耗材入库'

    name = fields.Char('耗材名称', required= True)
    consumables_type_id = fields.Many2one('funenc_xa_station.consumables_type',string='耗材类型', required= True)
    store_house_id = fields.Many2one('funenc_xa_station.store_house', string='入库名称', required= True)
    warehousing_count = fields.Integer(string='入库数量')
    warehousing_parent = fields.Selection(selection=[('purchase','采购'),('organize','组织')],string='采购方式')
    warehousing_line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='采购线路')
    warehousing_site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='采购站点')


