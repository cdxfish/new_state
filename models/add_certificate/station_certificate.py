from odoo import api, models, fields


class AddStationCertificate(models.Model):
    _name = 'station.certificate'

    name = fields.Char(string='证件名称')
    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    certificate_time = fields.Char(string='证件有效期')
    certificate_details = fields.Binary(string='证件详情')
    file_name = fields.Char(string="File Name")
    certificate_number = fields.Integer(string='证件号码')
    station_agent = fields.Char(string='站长')
    station_agent_phone = fields.Integer(string='站长电话')
    url = fields.Char(string='url')

    def station_cer_edit(self):
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'station.certificate',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def station_cer_delete(self):
        self.env['station.certificate'].search([('id', '=', self.id)]).unlink()

    @api.model
    def create(self, params):
        file_binary = params['certificate_details']
        if file_binary:
            url, key = self.env['qiniu_service.qiniu_upload_bucket'].upload_file(
                file_binary, 'pics')
            params['url'] = url
            params['file_name'] = key
        return super(AddStationCertificate, self).create(params)

    def station_details(self):
        url = self.url
        if url:
            url = 'http://' + url
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }

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
