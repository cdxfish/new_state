from odoo import models, fields, api
import odoo.exceptions as msg
import datetime
from ..get_domain import get_domain

KEY = [('send', '待确认'),
       ('refuse', '已拒绝'),
       ('approval_pending', '待审批'),
       ('pass', '已通过'),
       ('reject', '已驳回')
       ]


class ChangeShifts(models.Model):
    _name = 'funenc_xa_station.change_shifts'
    _description = '换班'
    _inherit = 'fuenc_station.station_base'

    application_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='申请人')
    jobnumber = fields.Char(related='application_user_id.jobnumber', string="工号")
    position = fields.Text(related='application_user_id.position', string="职位")
    application_time = fields.Datetime(string='申请时间')
    change_shifts_time = fields.Datetime(string='换班时间')
    personal_change_shifts = fields.Many2one('funenc_xa_station.arrange_order', string='个人班次')  # 个人班次
    personal_change_shifts_1 = fields.Many2one('funenc_xa_station.sheduling_record', string='个人班次')

    # show_personal_change_shifts = fields.Char(string='显示个人班次')  #显示个人班次

    change_shifts_group = fields.Many2one('funenc_xa_station.arrange_order', string='换班班次')  # 换班班次
    change_shifts_group_1 = fields.Many2one('funenc_xa_station.sheduling_record', string='换班班次')  # 换班班次

    # show_change_shifts_group = fields.Char(string='显示换班班次') # 显示换班班次

    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='换班对象')
    change_shifts_jobnumber = fields.Char(related='change_shifts_user_id.jobnumber', string="工号")
    is_agree = fields.Selection(selection=[('yes', '是'), ('no', '否')], string='换班对象是否同意', default='no')
    agree_time = fields.Datetime(string='同意时间')
    is_approve = fields.Selection(selection=[('yes', '是'), ('no', '否')], string='是否审批', default='no')
    approve_time = fields.Datetime(string='审批时间')
    reject_time = fields.Datetime(string='驳回时间')
    reason = fields.Text(string='换班原因')
    examine_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='审核人')

    # change_shifts_state = fields.Selection(selection=[('send', '发起的'), ('receive', '接收的')])
    #
    # parent_id = fields.Many2one('funenc_xa_station.change_shifts', string='父')  # 发起的
    # child_ids = fields.One2many('funenc_xa_station.change_shifts', 'parent_id', seing='子')  # 收到的

    state = fields.Selection(KEY, default='send')

    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.break_submit_tree').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.change_shifts',
            'context': self.env.context,
        }

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
        self.approve_time = datetime.datetime.now()
        self.is_approve = 'yes'
        self.state = 'pass'

        #   换班
        change_shifts_group = self.change_shifts_group_1.arrange_order_id.id  # 换班班次
        change_user_id = self.change_shifts_group_1.user.id
        personal_change_shifts = self.personal_change_shifts_1.arrange_order_id.id  # 个人班次
        personal_user_id = self.personal_change_shifts_1.user.id
        self.change_shifts_group_1.arrange_order_id = personal_change_shifts
        self.change_shifts_group_1.user_id = change_user_id
        self.personal_change_shifts_1.arrange_order_id = change_shifts_group
        self.personal_change_shifts_1.user_id = personal_user_id

    def retreat(self):

        self.is_agree = 'no'
        self.agree_time = None
        self.approve_time = None
        self.is_approve = 'no'
        self.state = 'reject'
        self.reject_time = datetime.datetime.now()

    @api.model
    def save_change_shifts(self, **kw):
        try:

            ding_user = self.env.user.dingtalk_user
            personal_change_shifts_1 = kw.get('personal_change_shifts_1')
            sheduling_record = self.env['funenc_xa_station.sheduling_record'].search(
                [('id', '=', personal_change_shifts_1)])
            if sheduling_record:
                kw['application_user_id'] = ding_user.id
                kw['state'] = 'send'
                kw['change_shifts_time'] = sheduling_record.sheduling_date or ''
                kw['application_time'] = datetime.datetime.now()
                self.create(kw)

                return True
            else:
                return False
        except Exception:

            return False

    @api.model
    def get_change_shifts_list(self, parameter):
        try:
            ding_user = self.env.user.dingtalk_user
            if parameter == 'send':
                change_shifts_ids = self.search([('application_user_id', '=', ding_user.id)])  # 发送的

            else:
                change_shifts_ids = self.search([('change_shifts_user_id', '=', ding_user.id)])  # 接收的
            data = []
            for change_shifts_id in change_shifts_ids:
                states = KEY
                tmp = ''
                for state in states:
                    if state[0] == change_shifts_id.state:
                        tmp = state[1]
                data.append({'id': change_shifts_id.id,
                             'originDate': change_shifts_id.change_shifts_time if change_shifts_id.change_shifts_time else '',
                             'originDON': change_shifts_id.change_shifts_group_1.arrange_order_id.name,
                             'originTime': change_shifts_id.change_shifts_group_1.time_interval[
                                           :-5] if change_shifts_id.change_shifts_group_1.time_interval else '',
                             'changeDate': change_shifts_id.personal_change_shifts_1.sheduling_date,
                             'changeDON': change_shifts_id.personal_change_shifts_1.arrange_order_id.name,
                             'changeTime': change_shifts_id.personal_change_shifts_1.time_interval[
                                           :-5] if change_shifts_id.personal_change_shifts_1.time_interval else '',
                             'status': tmp
                             })
            return data
        except Exception:
            return []

    @api.model
    def get_change_shifts_by_id(self, id):
        try:

            id = int(id)
            change_shifts = self.browse(id)
            states = KEY
            tmp = ''
            for state in states:
                if state[0] == change_shifts.state:
                    tmp = state[1]

            dic = {
                'id': change_shifts.id,
                'line': change_shifts.line_id.name,
                'station': change_shifts.site_id.name,
                'originDate': change_shifts.change_shifts_time,
                'originDON': change_shifts.personal_change_shifts_1.arrange_order_id.name,
                'originTime': change_shifts.personal_change_shifts_1.time_interval[
                              :-5] if change_shifts.personal_change_shifts_1.time_interval else '',
                'originUser': change_shifts.application_user_id.name,
                'originUserJobNum': change_shifts.application_user_id.jobnumber,
                'changeDate': change_shifts.change_shifts_group_1.sheduling_date,
                'changeDON': change_shifts.change_shifts_group_1.arrange_order_id.name,
                'changeTime': change_shifts.change_shifts_group_1.time_interval[
                              :-5] if change_shifts.change_shifts_group_1.time_interval else '',
                'changeUser': change_shifts.change_shifts_user_id.name,
                'changeUserJobNum': change_shifts.change_shifts_jobnumber,
                'changeReason': change_shifts.reason,
                'passUser': change_shifts.examine_user.name,
                'sendTime': change_shifts.application_time,
                'comfirmTime': change_shifts.agree_time,
                'passTime': change_shifts.approve_time,
                'status': tmp,

            }

            return dic
        except Exception:
            return []

    @api.model
    def save_state(self, id, states):
        try:
            id = int(id)
            ding_user = self.env.user.dingtalk_user
            change_shifts = self.browse([id])
            if change_shifts.change_shifts_user_id.id == ding_user.id:
                if states == '同意':
                    change_shifts.state = 'approval_pending'
                    change_shifts.personal_change_shifts_1.arrange_order_id = change_shifts.change_shifts_group_1.arrange_order_id.id

                    return True

                else:

                    change_shifts.state = 'refuse'

                    return True


            else:
                return False

        except Exception:

            return False


class ChangeShiftsTime(models.Model):
    _name = 'funenc_xa_station.change_shifts_time'
    _description = '换班时间间隔'
    # _inherit = 'fuenc_station.station_base'

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

        return dic
