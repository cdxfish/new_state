from odoo import api,models,fields


class AddPersonCertificate(models.Model):
    _name = 'person.certificate'

    name = fields.Char(string='证件名称')
    line_road = fields.Many2one('train_line.train_line',string='线路')
    station_site = fields.Many2one('train_station.train_station',string='站点')
    person_name = fields.Char(string='姓名')
    work_number = fields.Char(string='工号')
    phone = fields.Integer(string='电话')
    site = fields.Char(string='职位')
    book_number = fields.Char(string='证书编码')
    licence_issuing_authority = fields.Char(string='发证机关')
    get_certificate_time =fields.Datetime(string='初领日期')
    period_of_validity = fields.Datetime(string='有效期')
    certificate_money = fields.Float(string='领证费用')
    one_recheck_time = fields.Datetime(string='初次复审时间')
    two_recheck_time = fields.Datetime(string='二次复审时间')
    one_recheck_money = fields.Integer(string='初次复审的费用')
    two_recheck_money = fields.Integer(string='二次复审的费用')
    book_details = fields.Binary(string='上传证件照片')
    file_name = fields.Char(string="File Name")
    gender = fields.Char(string='员工性别')
    train_time = fields.Char(string='培训时间')
    url = fields.Char(string='url')

    def person_cer_edit(self):
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'person.certificate',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def person_cer_delete(self):
        self.env['person.certificate'].search([('id', '=', self.id)]).unlink()

    @api.model
    def create(self, params):
        file_binary = params['book_details']
        url, key = self.env['qiniu_service.qiniu_upload_bucket'].upload_file(
            file_binary, 'pics')
        params['url'] = url
        params['file_name'] = key
        return super(AddPersonCertificate, self).create(params)

    def person_details(self):
        url = self.url
        url = 'http://' + url
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    def book_details_load(self):
        view_form = self.env.ref('funenc_xa_station.person_certificate_form_load').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'person.certificate',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            'target': 'new',
        }


