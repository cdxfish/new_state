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
            'target':'current',
        }

    @api.model
    def return_tab_with_group(self, tab_data, action_id):
        self._cr.execute('''SELECT module, name FROM ir_model_data WHERE 
        (module = 'funenc_xa_station' AND model = 'ir.actions.server' AND res_id = %s) OR
        (module = 'funenc_xa_station' AND model = 'ir.actions.act_window' AND res_id = %s)''' % (action_id, action_id))
        results = self._cr.fetchall()
        for tab in tab_data:
            if len(results) == 0:
                tab['is_this'] = 'false'
            else:
                for result in results:
                    if (tab.get('action', '') == '{}.{}'.format(result[0], result[1]) or
                            tab.get('action2', '') == '{}.{}'.format(result[0], result[1])):
                        tab['is_this'] = 'true'
                        break
                else:
                    tab['is_this'] = 'false'
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
        self._cr.execute("""SELECT module ||'.'|| name FROM ir_model_data WHERE module='funenc_xa_station' AND 
        res_id IN %s""" % str(group_ids))
        result = [i[0] for i in self._cr.fetchall()]
        return {self._uid: result}
