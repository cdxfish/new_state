# -*- coding: utf-8 -*-
from odoo import models, api
from .get_domain import get_domain


class ReturnViewFunction(models.AbstractModel):
    _name = 'funenc_xa_station.return.view.function'
    _description = '返回视图数据表'

    @api.model
    @get_domain
    def return_act_window(self, domain, name, model, tree_xml_id, form_xml_id):
        view_tree_id = self.env.ref(tree_xml_id).id
        form_tree_id = self.env.ref(form_xml_id).id
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree_id, "tree"], [form_tree_id, 'form']],
            'res_model': model,
            'context': self.env.context,
        }