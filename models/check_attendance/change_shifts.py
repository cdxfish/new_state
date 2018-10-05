from odoo import models, fields, api

class ChangeShifts(models.Model):
    _name = 'funenc_xa_station.change_shifts'
    _description = '换班'
    _inherit = 'fuenc_station.station_base'

    application_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='申请人')
    jobnumber = fields.Char(related='application_user_id.jobnumber', string="工号")
    position = fields.Text(related='application_user_id.position', string="职位")
    application_time = fields.Datetime(string='申请时间')
    change_shifts_time = fields.Datetime(string='换班时间')
    change_shifts_group = fields.Many2one('funenc_xa_station.arrange_order',string='换班班次')
    change_shifts_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='换班对象')
    change_shifts_jobnumber = fields.Char(related='change_shifts_user_id.jobnumber', string="工号")
    is_agree = fields.Selection(selection=[('yes','是'),('no','否')],string='是否同意')
    agree_time = fields.Datetime(string='同意时间')
    is_approve = fields.Selection(selection=[('yes','是'),('no','否')],string='是否审批')
    approve_time = fields.Datetime(string='审批时间')


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
            "views": [[False, "tree"],[False, "form"]],
            'res_model': 'funenc_xa_station.change_shifts_time',
            'context': context,
            'target': 'current',
        }
        if self.env.user.has_group('funenc_xa_station.system_fuenc_site'):
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            obj = self.search([('site_id', '=', department.id)])
            if not obj:
                self.create({'site_id':department.id,
                             'line_id':ding_user.line_id.id,
                             'context':'换班需提前申请时间（天）',
                             'time': 1
                             })
                dic['domain']= [('site_id','=',department.id)]

        return dic

