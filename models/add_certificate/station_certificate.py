from odoo import api, models, fields


class AddStationCertificate(models.Model):
    _name = 'station.certificate'

    name = fields.Char(string='证件名称')
    line_road = fields.Many2one('train_line.train_line',string='线路')
    station_site = fields.Many2one('train_station.train_station',string='站点')
    certificate_time = fields.Char(string='证件有效期')
    certificate_details = fields.Binary(string='证件详情')
    file_name = fields.Char(string="File Name")
    certificate_number = fields.Integer(string='证件号码')
    station_agent = fields.Char(string='站长')
    station_agent_phone = fields.Integer(string='站长电话')
    url = fields.Char(string='url')
    load_file_test = fields.One2many('ir.attachment','res_id', string='图片上传')

    @api.model
    def station_certificate_type(self):
        return {
            'name': '新增专业类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'station.certificate',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def station_cer_edit(self):
        self.new_ = {'name': '证件名称', 'type': 'ir.actions.act_window', 'view_type': 'form', 'view_mode': 'form',
                     'res_model': 'station.certificate', 'context': self.env.context, 'flags': {'initial_mode': 'edit'},
                     'res_id': self.id, 'target': 'new', }
        return self.new_

    def station_cer_delete(self):
        self.env['station.certificate'].search([('id', '=', self.id)]).unlink()

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
