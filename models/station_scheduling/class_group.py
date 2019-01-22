# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

from ..get_domain import get_domain


class ClassGroup(models.Model):
    '''
        班组管理
    '''

    _name = 'funenc_xa_station.class_group'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _description = u'班组管理'

    name = fields.Char(string='班组名称', required=True)
    group_user_ids = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users', 'class_group_dingtalk_user_1_ref',
                                      'class_group_id', 'ding_talk_user_id', string='班组人员')

    # arrange_class_manage_ids =  fields.One2many('funenc_xa_station.arrange_class_manage', 'arrange_class_obj', string='排班规则对应')

    @get_domain
    @api.model
    def init_data(self, domain):
        context = {}
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_class_group_list').id
        return {
            'name': '班组管理',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.class_group",
            "views": [[view_tree, "tree"]],
            "domain": domain,
            'target': 'current',
            'context': context,
        }

    def create_class_group(self):
        context = dict(self.env.context or {})
        return {
            'name': '新增班组',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.class_group',
            'context': context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def class_group_edit(self):
        context = dict(self.env.context or {})
        unselected_user_ids = self.unselected_user_ids(self.site_id.id)
        context['unselected_user_ids'] = unselected_user_ids
        return {
            'name': '班组详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.class_group',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
            'domain': {'group_user_ids': [('id', 'in', unselected_user_ids)]}
        }

    @api.onchange('site_id')
    def onchange_site_id(self):
        if not self.site_id:
            domain = [('id', '<', 0)]
        else:
            unselected_user_ids = self.unselected_user_ids(self.site_id.id)
            domain = [('id', 'in', unselected_user_ids)]

        return {
            'domain': {'group_user_ids': domain}
        }

    def class_group_delete(self):
        self.unlink()

    # def unselected_user_ids(self):
    #     # 班组可选人员过滤
    #     res_user = self.env.user
    #     if res_user.id == 1:
    #         sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where 1=1"
    #         self.env.cr.execute(sel_sql)
    #         select_user_ids = self.env.cr.dictfetchall()
    #         select_user_ids_list = [select_user_id.get('ding_talk_user_id') for select_user_id in select_user_ids]
    #         user_ids_sql = "select id from cdtct_dingtalk_cdtct_dingtalk_users where 1=1"
    #         self.env.cr.execute(user_ids_sql)
    #         user_ids = self.env.cr.dictfetchall()
    #         user_ids_list = [user_id.get('id') for user_id in  user_ids]
    #
    #         return list(set(user_ids_list) - set(select_user_ids_list))
    #     else:
    #         ding_user = self.env.user.dingtalk_user[0]
    #         department_id = ding_user.departments[0]
    #
    #         if department_id.department_hierarchy == 1:
    #             sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where 1=1"
    #             self.env.cr.execute(sel_sql)
    #             select_user_ids = self.env.cr.dictfetchall()
    #             select_user_ids_list = [select_user_id.get('ding_talk_user_id') for select_user_id in select_user_ids]
    #             user_ids_sql = "select id from cdtct_dingtalk_cdtct_dingtalk_users where 1=1"
    #             self.env.cr.execute(user_ids_sql)
    #             user_ids = self.env.cr.dictfetchall()
    #             user_ids_list = [user_id.get('id') for user_id in user_ids]
    #
    #             return list(set(user_ids_list) - set(select_user_ids_list))
    #         else:
    #             if department_id.department_hierarchy == 3:
    #                 department_sql = 'select user_id from cdtct_dingtalk_user_department_rel where department_id = {}'.format(department_id.id)
    #                 self.env.cr.execute(department_sql)
    #                 department_user_ids = [department_user_id.get('user_id') for department_user_id in self.env.cr.dictfetchall()]
    #                 if len(department_user_ids) > 1:
    #                     sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where ding_talk_user_id in {}".format(tuple(department_user_ids))
    #                     self.env.cr.execute(sel_sql)
    #                     select_user_ids = self.env.cr.dictfetchall()
    #                 elif len(department_user_ids) == 1 :
    #                     sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where ding_talk_user_id = {}".format(
    #                         tuple(department_user_ids[0]))
    #                     self.env.cr.execute(sel_sql)
    #                     select_user_ids = self.env.cr.dictfetchall()
    #                 else:
    #                     select_user_ids = []
    #                 select_user_ids_list = [select_user_id.get('ding_talk_user_id') for select_user_id in select_user_ids]
    #                 return list(set(department_user_ids) - set(select_user_ids_list))
    #             else:
    #                 return []

    def unselected_user_ids(self, site_id):
        # 班组可选人员过滤
        department_sql = 'select ding_user_id as user_id from dingtalk_users_to_departments where department_id = {}'.format(
            site_id)
        self.env.cr.execute(department_sql)
        department_user_ids = [department_user_id.get('user_id') for department_user_id in self.env.cr.dictfetchall()]
        if len(department_user_ids) > 1:
            sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where ding_talk_user_id in {}".format(
                tuple(department_user_ids))
            self.env.cr.execute(sel_sql)
            select_user_ids = self.env.cr.dictfetchall()
        elif len(department_user_ids) == 1:
            sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where ding_talk_user_id = {}".format(
                department_user_ids[0])
            self.env.cr.execute(sel_sql)
            select_user_ids = self.env.cr.dictfetchall()
        else:
            select_user_ids = []
        select_user_ids_list = [select_user_id.get('ding_talk_user_id') for select_user_id in select_user_ids]

        return list(set(department_user_ids) - set(select_user_ids_list))
