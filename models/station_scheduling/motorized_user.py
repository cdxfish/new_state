# -*- coding: utf-8 -*-

from odoo import models, api
class UserInherit(models.Model):
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_users'


    @api.model
    def get_motorized_users(self):
        res_user = self.env.user
        if res_user.id == 1:
            sel_sql = "select ding_talk_user_id from class_group_dingtalk_user_1_ref where 1=1"
            self.env.cr.execute(sel_sql)
            select_user_ids = [select_user_id.get('ding_talk_user_id')for select_user_id in self.env.cr.dictfetchall()]
            motorized_user_ids = self.search_read([('id','in',select_user_ids)])
            for motorized_user_id in motorized_user_ids:
                motorized_user_id['user_property'] = '本站'
            person_second_ids = self.env['person_management.person_second'].search([])
            second_user_ids= [person_second_id.user_id.id for person_second_id in person_second_ids]
            person_second_user_ids = self.search_read([('id', 'in', second_user_ids)])
            for second_user_id in person_second_user_ids:
                second_user_id['user_property'] = '借调'
            user_ids = motorized_user_ids + person_second_user_ids
            for user_id in user_ids:
                if user_id.get('certificate_status') == 'one':
                    user_id['certificate_status'] = '正常'
                else:
                    user_id['certificate_status'] = '丢失'
            return user_ids
        else:
            ding_user = res_user.dingtalk_user[0]
            department_id = ding_user.departments[0]
            if department_id.department_hierarchy == 2:
                line_id = ding_user.line_id.id
                class_groups = self.env['funenc_xa_station.class_group'].search([('line_id','=', line_id)])
                centrality_motorized_user_ids = [] # 中心级别任务 机动人员
                for class_group in class_groups:
                    for user_id in class_group.group_user_ids:
                        centrality_motorized_user_ids.append(user_id.id)

                centrality_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search_read([('id','in',centrality_motorized_user_ids)])
                for centrality_user_id in centrality_user_ids:
                    centrality_user_id['user_property'] = '本站'
                    if centrality_user_id.get('certificate_status') == 'one':
                        centrality_user_id['certificate_status'] = '正常'
                    else:
                        centrality_user_id['certificate_status'] = '丢失'
                person_second_ids = self.env['person_management.person_second'].search_read([('line_id', '=', line_id)],['user_id'])

                person_second_user_ids = self.search_read([ ('id','in', [person_second_id.get('user_id') for person_second_id in person_second_ids]) ])
                for person_second_user_id in person_second_user_ids:
                    person_second_user_id['user_property'] = '借调'
                    if person_second_user_id.get('certificate_status') == 'one':
                        person_second_user_id['certificate_status'] = '正常'
                    else:
                        person_second_user_id['certificate_status'] = '丢失'

                return centrality_user_ids + person_second_user_ids

            else:
                department_id = department_id.id
                class_groups = self.env['funenc_xa_station.class_group'].search([('site_id', '=', department_id)])
                centrality_motorized_user_ids = []  # 车站级别 在组内人员
                for class_group in class_groups:
                    for user_id in class_group.group_user_ids:
                        centrality_motorized_user_ids.append(user_id.id)

                site_groups_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search([('departments','=',department_id)]).ids
                not_in_groups_user_ids = list( set(site_groups_user_ids) - set(centrality_motorized_user_ids) )   # 未在组内人员
                centrality_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search_read(
                    [('id', 'in', not_in_groups_user_ids)])
                for centrality_user_id in centrality_user_ids:
                    centrality_user_id['user_property'] = '本站'
                person_second_ids = self.env['person_management.person_second'].search_read(
                    [('second_station', '=', department_id)], ['user_id'])

                person_second_user_ids = self.search_read(
                    [('id', 'in', [person_second_id.get('user_id')[0] for person_second_id in person_second_ids])])
                for person_second_user_id in person_second_user_ids:
                    person_second_user_id['user_property'] = '借调'
                    if person_second_user_id.get('certificate_status') == 'one':
                        person_second_user_id['certificate_status'] = '正常'
                    else:
                        person_second_user_id['certificate_status'] = '丢失'

                return centrality_user_ids + person_second_user_ids

    @api.model
    def get_motorized_users_by_site_id(self,site_id):
        #  机动人员过滤

        department_id = site_id
        class_groups = self.env['funenc_xa_station.class_group'].search([('site_id', '=', department_id)])
        centrality_motorized_user_ids = []  # 车站级别 在组内人员
        for class_group in class_groups:
            for user_id in class_group.group_user_ids:
                centrality_motorized_user_ids.append(user_id.id)

        site_groups_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search(
            [('departments', '=', department_id)]).ids
        not_in_groups_user_ids = list(set(site_groups_user_ids) - set(centrality_motorized_user_ids))  # 未在组内人员
        centrality_user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search_read(
            [('id', 'in', not_in_groups_user_ids)],['id'])

        person_second_ids = self.env['person_management.person_second'].search_read(
            [('second_station', '=', department_id)], ['user_id'])

        person_second_user_ids = self.search_read(
            [('id', 'in', [person_second_id.get('user_id')[0] for person_second_id in person_second_ids])],['id'])

        return [centrality_user_id ['id']for centrality_user_id in centrality_user_ids] + [person_second_user_id ['id'] for person_second_user_id in person_second_user_ids]
