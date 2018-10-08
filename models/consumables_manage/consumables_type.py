import odoo.exceptions as msg
from odoo import models, fields, api


class ConsumablesType(models.Model):
    _name = 'funenc_xa_station.consumables_type'
    # _inherit = 'fuenc_station.station_base'
    _description = u'耗材分类'
    _rec_name = 'consumables_type'

    consumables_type = fields.Char('耗材分类',required= True)
    prent_id = fields.Many2one('funenc_xa_station.consumables_type',string='父耗材分类')
    child_ids = fields.One2many('funenc_xa_station.consumables_type', 'prent_id', string='子耗材分类')


    @api.model
    def create_consumables_type(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材类型创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_type',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '钥匙类型编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_type',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }
    def delete(self):
        self.unlink()
