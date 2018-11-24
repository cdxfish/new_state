import functools
import logging
_logger = logging.getLogger(__name__)

def get_domain(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.env.user.id == 1:
            return func(self, [], *args, **kwargs)
        ding_user = self.env.user.dingtalk_user
        ids = ding_user.user_property_departments.ids

        return func(self, [('site_id', 'in', ids)], *args, **kwargs)
    return wrapper


def get_site_id_domain(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        if len(ding_user.departments) == 0:
            return func(self, [], *args, **kwargs)
        department = ding_user.departments[0]
        if department.department_hierarchy == 1:
            return func(self, [], *args, **kwargs)
        elif department.department_hierarchy == 2:
            ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                [('parentid', '=', department.departmentId)]).ids
            return func(self, [('id', 'in', ids)], *args, **kwargs)
        else:
            return func(self, [('id', '=', department.id)], *args, **kwargs)
    return wrapper


def get_line_id_domain(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        line_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=',department_id.parentid)]).id

                line_ids.append(id)

        return func(self, [('id', 'in', line_ids)], *args, **kwargs)

    return wrapper

def get_line_id(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        line_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=',department_id.parentid)]).id

                line_ids.append(id)

        return func(self, line_ids[0] if line_ids else None, *args, **kwargs)

    return wrapper

def get_line_site_id(func):
    '''
    获取用户默认线路和站点
    :param func:
    :return: (line_id,site_id)
    '''
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        line_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=', department_id.parentid)]).id

                line_ids.append(id)
        line_id = line_ids[0] if line_ids else None
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].browse(line_id)
        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department.departmentId)]).ids
        site_ids = list(set(department_ids.ids) & set(child_department_ids))
        line_site_id = (line_id,site_ids[0] if site_ids else None)

        return func(self, line_site_id, *args, **kwargs)


    return wrapper

def get_site_ids(func):
    '''
    :param func:
    :return:  返回用户所在属性 list 站点id
    '''

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        site_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                site_ids.append(department_id.id)

        return func(self, site_ids, *args, **kwargs)

    return wrapper

def get_line_ids(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ding_user = self.env.user.dingtalk_user
        department_ids = ding_user.user_property_departments
        line_ids = []
        for department_id in department_ids:
            if department_id.department_hierarchy == 3:
                id = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
                    [('departmentId', '=', department_id.parentid)]).id

                line_ids.append(id)

        return func(self,  line_ids, *args, **kwargs)

    return wrapper