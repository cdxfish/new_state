# -*- coding: utf-8 -*-
from odoo import models, api
from .get_domain import get_domain


class ReturnViewFunction(models.AbstractModel):
    _name = 'funenc_xa_station2.return.view.function'
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

    @api.model
    def return_tab_with_group(self, tab_data):
        for tab in tab_data:
            if tab.get('group', '') != '':
                if self.user_has_groups(tab['group']) is True:
                    tab['display'] = 'true'
                else:
                    tab['display'] = 'false'
            else:
                tab['display'] = 'true'
        return tab_data

    @api.model
    def get_groups_with_id(self):
        group_ids = tuple(self.env.user.groups_id.ids)
        self._cr.execute("""SELECT module ||'.'|| name FROM ir_model_data WHERE module='funenc_xa_station2' AND 
        res_id IN %s""" % str(group_ids))
        result = [i[0] for i in self._cr.fetchall()]
        return {self._uid: result}
