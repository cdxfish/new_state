from odoo import api, models, fields
from ..get_domain import get_domain

class AddStationCertificate(models.Model):
    _name = 'station.certificate'
    _inherit = 'fuenc_station.station_base'

    name = fields.Char(string='证件名称')
    # line_road = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='线路')
    # station_site = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='站点')
    certificate_time = fields.Char(string='证件有效期')
    file_name = fields.Char(string="File Name")
    certificate_number = fields.Char(string='证件号码')
    station_agent = fields.Char(string='站长')
    station_agent_phone = fields.Integer(string='站长电话')
    load_file_test= fields.Many2many('ir.attachment','station_certificate_ir_attachment_rel','ir_attachment_id',
                                   'station_id', string='图片上传')

    @get_domain
    @api.model
    def get_day_plan_publish_action(self,domain):
        tree_id = self.env.ref('funenc_xa_station.add_station_certificate_tree').id
        form_id = self.env.ref('funenc_xa_station.add_station_certificate_form').id
        return {
            'name': '车站证件管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[tree_id, "tree"], [form_id, 'form']],
            'res_model': 'station.certificate',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                        [
                            {'title': '车站证件管理',
                            'action':  'funenc_xa_station.station_certificate_act_id_3'},
                            {
                                'title': '人员证件管理',
                                'action2':  'funenc_xa_station.person_certificate_act'},

                            {'title': '', 'domains': [['id', '=', '1']]}
                        ]
                    }''',
            'context': self.env.context,
        }

    @api.model
    def station_certificate_type(self):
        view_form = self.env.ref('funenc_xa_station.add_station_certificate_form').id
        return {
            'name': '车站证件',
            'type': 'ir.actions.act_window',
            'res_model': 'station.certificate',
            "views": [[view_form, "form"]],
            'context': self.env.context,
        }

    def station_cer_edit(self):
        view_form = self.env.ref('funenc_xa_station.add_station_certificate_form').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_id': self.id,
            'res_model': 'station.certificate',
            'context': self.env.context,
            'target': 'new',

        }



    def station_details(self):
        view_form = self.env.ref('funenc_xa_station.add_station_certificate_details').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'station.certificate',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }

    def station_cer_delete(self):
        self.env['station.certificate'].search([('id', '=', self.id)]).unlink()

    def station_load(self):
        view_form = self.env.ref('funenc_xa_station.add_station_certificate_form_load').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'station.certificate',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }
