from odoo import models, fields, api
import odoo.exceptions as msg
import datetime


class ChangeShifts(models.Model):
    _name = 'funenc_xa_station.change_shifts'
    _description = '换班'
    _inherit = 'fuenc_station.station_base'

    application_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='申请人')
    jobnumber = fields.Char(related='application_user_id.jobnumber', string="工号")
    position = fields.Text(related='application_user_id.position', string="职位")
    application_time = fields.Datetime(string='申请时间')
    change_shifts_time = fields.Datetime(string='换班时间')
    change_shifts_group = fields.Many2one('funenc_xa_station.arrange_order', string='换班班次')  # 换班班次
    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='换班对象')
    change_shifts_jobnumber = fields.Char(related='change_shifts_user_id.jobnumber', string="工号")
    is_agree = fields.Selection(selection=[('yes', '是'), ('no', '否')], string='换班对象是否同意', default='no')
    agree_time = fields.Datetime(string='同意时间')
    is_approve = fields.Selection(selection=[('yes', '是'), ('no', '否')], string='是否审批', default='no')
    approve_time = fields.Datetime(string='审批时间')

    state = fields.Selection([('draft', '草稿'),
                              ('application', '申请'),
                              ('agree', '本人同意'),
                              ('site_agree', '站长同意')
                              ], default='draft')

    def apply(self):
        if not self.application_user_id:
            raise msg.Warning('申请人必填')
        if not self.application_time:
            raise msg.Warning('申请时间必填')
        if not self.change_shifts_time:
            raise msg.Warning('换班时间必填')
        if not self.change_shifts_group:
            raise msg.Warning('换班班次必填')
        if not self.change_shifts_user_id:
            raise msg.Warning('换班对象')

        self.state = 'application'

    def agree(self):
        if not self.application_user_id:
            raise msg.Warning('申请人必填')
        if not self.application_time:
            raise msg.Warning('申请时间必填')
        if not self.change_shifts_time:
            raise msg.Warning('换班时间必填')
        if not self.change_shifts_group:
            raise msg.Warning('换班班次必填')
        if not self.change_shifts_user_id:
            raise msg.Warning('换班对象')
        self.is_agree = 'yes'
        self.agree_time = datetime.datetime.now()
        self.state = 'agree'

    def site_agree(self):
        if not self.application_user_id:
            raise msg.Warning('申请人必填')
        if not self.application_time:
            raise msg.Warning('申请时间必填')
        if not self.change_shifts_time:
            raise msg.Warning('换班时间必填')
        if not self.change_shifts_group:
            raise msg.Warning('换班班次必填')
        if not self.change_shifts_user_id:
            raise msg.Warning('换班对象')
        self.approve_time = datetime.datetime.now()
        self.is_approve = 'yes'
        self.state = 'site_agree'

    def retreat(self):

        self.is_agree = 'no'
        self.agree_time = None
        self.approve_time = None
        self.is_approve = 'no'
        self.state = 'draft'


class ChangeShiftsTime(models.Model):
    _name = 'funenc_xa_station.change_shifts_time'
    _description = '换班时间间隔'
    _inherit = 'fuenc_station.station_base'

    context = fields.Char('内容')
    time = fields.Integer(string='天')

    def init_data(self):
        context = dict(self.env.context or {})
        dic = {
            'name': '换班时间间隔设置',
            'type': 'ir.actions.act_window',
            "views": [[False, "tree"], [False, "form"]],
            'res_model': 'funenc_xa_station.change_shifts_time',
            'context': context,
            'target': 'current',
        }
        if self.env.user.has_group('funenc_xa_station.system_fuenc_site'):
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            obj = self.search([('site_id', '=', department.id)])
            if not obj:
                self.create({'site_id': department.id,
                             'line_id': ding_user.line_id.id,
                             'context': '换班需提前申请时间（天）',
                             'time': 1
                             })
                dic['domain'] = [('site_id', '=', department.id)]

        return dic

    @api.model
    def get_change_shifts_list(self, parameter):
        ding_user = self.env.user.dingtalk_user
        if parameter == 'send':
            change_shifts_ids =  self.search_read([('application_user_id', '=', ding_user.id)])


        else:
            pass
