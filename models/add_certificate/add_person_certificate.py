from odoo import api,models,fields
from ..get_domain import get_domain

class AddPersonCertificate(models.Model):
    _name = 'person.certificate'
    _inherit = 'fuenc_station.station_base'
    _description = ''

    def _default_associated(self):
        if self._context.get('active_id', False):
            return self._context['active_id']

    name = fields.Char(string='证件名称',track_visibility='onchange')
    # line_road = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='线路')
    # station_site = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='站点')
    person_name = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='姓名')
    # person_name = fields.Char(string='姓名')
    work_number = fields.Char(string='工号',related='person_name.jobnumber')
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
    gender = fields.Selection([('man','男'),('woman','女')],string='员工性别')
    train_time = fields.Datetime(string='培训时间')
    url = fields.Char(string='url')
    load_file_test = fields.Many2many('ir.attachment','person_certificate_ir_attachment_rel','person_certificate_id','ir_attachment_id', string='图片上传')
    relevance = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='关联字段没有实际意义',default=_default_associated)
    station_certificate_to_conflict_rule = fields.One2many('conflict_rule_station_certificate_ref',
                                                           'station_certificate_id', string='')
    person_certificate_browse = fields.Selection([('one','显示图片'),('zero','图片不显示')],default='zero')
    relevance_staff = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='关联字段没有实际意义', default=_default_associated)

    @get_domain
    @api.model
    def get_day_plan_publish_action(self, domain):
        tree_id = self.env.ref('funenc_xa_station.person_certificate_tree').id
        form_id = self.env.ref('funenc_xa_station.person_certificate_form').id
        return {
            'name': '人员证件管理',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[tree_id, "tree"], [form_id, 'form']],
            'res_model': 'person.certificate',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                            [
                                    {
                                        'title': '车站证件管理',
                                        'action':  'funenc_xa_station.station_certificate_button_server',
                                        'group':'funenc_xa_station.table_car_certificates',
                                    },
                                    {
                                        'title': '人员证件管理',
                                        'action2' : 'funenc_xa_station.person_certificate_server',
                                        'group' : 'funenc_xa_station.table_people_certificates',
                                    },
                            ]
                        }''',
            'context': self.env.context,
        }


    @api.model
    def create(self, vals):
        vals['relevance_staff'] = vals['person_name']
        if vals.get('load_file_test')[0][2]:
            vals['person_certificate_browse']='one'
        return super(AddPersonCertificate, self).create(vals)

    #新增一条记录
    @api.model
    def person_certificate_type(self):
        view_form = self.env.ref('funenc_xa_station.person_certificate_form').id
        return {
            'name': '新增',
            'type': 'ir.actions.act_window',
            'res_model': 'person.certificate',
            "views": [[view_form, "form"]],
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }


    def person_cer_edit(self):
        view_form = self.env.ref('funenc_xa_station.person_certificate_form').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'person.certificate',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def person_cer_delete(self):
        self.env['person.certificate'].search([('id', '=', self.id)]).unlink()

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

    def person_details(self):
        view_form = self.env.ref('funenc_xa_station.person_certificate_details').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'person.certificate',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            'target':'new',
        }
