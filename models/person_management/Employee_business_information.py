from odoo import api, models, fields


class EmployeeBusinessInformation(models.Model):
    _name = 'employee.business.information'

    department = fields.Many2one('main.information',string='所属部门')
    department_load = fields.Char(string='所属线网')
    team_or_group_station = fields.Char(string='班主车站')
    post = fields.Char(string='岗位')
    begin_time = fields.Date(string='入司时间')
    become_a_regular_worker_time = fields.Date(string='转正时间')
    join_work_time = fields.Date(string='参加工作时间')
    staff_source = fields.Char(string='员工来源')