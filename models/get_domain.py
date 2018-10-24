import functools
from odoo import api,models,fields

def get_domain(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        if len(ding_user.departments) == 0:
            return func(self, [('id', '=', None)], *args, **kwargs)
        department = ding_user.departments[0]
        if department.department_hierarchy == 1:
            return func(self, [], *args, **kwargs)
        elif department.department_hierarchy == 2:
            ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department.departmentId)]).ids
            return func(self, [('site_id', 'in', ids)], *args, **kwargs)
        else:
            return func(self, [('site_id', '=', department.id)], *args, **kwargs)
    return wrapper