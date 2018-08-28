# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GroupManage(models.Model):
    '''
    权限组配置
    '''
    _inherit = 'res.groups'

    xml_id = fields.Char(related='category_id.xml_id')

    @api.model
    def get_sub_groups(self):
        pass

    @api.model
    def get_group_data(self, group_id):
        rst = {
            "cats": [{
                "groups": [],
                "checkedGroups": [],
                "name": "月计划",
                "checkAll": False,
                "isIndeterminate": False,
                'xml_id': 'construction_dispatch.module_category_month_plan'
            }, {
                "groups": [],
                "name": "周计划",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.module_category_week_plan'
            }, {
                "groups": [],
                "name": "日计划",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.module_category_day_extra_plan'
            }, {
                "groups": [],
                "name": "临时补修计划",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.module_category_temp_plan'
            }, {
                "groups": [],
                "name": "抢修作业补登",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.urgent_replair_lazy_record'
            }, {
                "groups": [],
                "name": "施工作业配合",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.construction_cooperate'
            }, {
                "groups": [],
                "name": "计划变更/调整",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.construction_plan_ajust_or_change'
            }, {
                "groups": [],
                "name": "外单位管理",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.external_unit_manage'
            }, {
                "groups": [],
                "name": "施工负责人管理",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.construct_master_manage'
            }, {
                "groups": [],
                "name": "施工控制",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.construct_control'
            }, {
                "groups": [],
                "name": "调度命令",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.dispatch_cmd'
            }, {
                "groups": [],
                "name": "供电工作票",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.electric_ticket'
            }, {
                "groups": [],
                "name": "动火令",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.fire_cmd'
            }, {
                "groups": [],
                "name": "停送电通知单",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.fire_cmd'
            }, {
                "groups": [],
                "name": "运营前检查",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.pre_business_check'
            }, {
                "groups": [],
                "name": "运营日报",
                "checkedGroups": [],
                "isIndeterminate": False,
                'xml_id': 'construction_dispatch.business_day_report'
            }, {
                "groups": [],
                "checkedGroups": [],
                "name": "系统配置",
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.dispatch_system_config',
            }, {
                "groups": [],
                "name": "查看",
                "checkedGroups": [],
                "isIndeterminate": False,
                "checkAll": False,
                'xml_id': 'construction_dispatch.view_infos'
            }]
        }
        # get the template
        template = self.env['vue_template_manager.template_manage'] \
            .get_template_content('construction_dispatch', 'group_config')
        rst['template'] = template

        implied_ids = []
        if group_id:
            record = self.browse(group_id)
            implied_ids += record.implied_ids

        # get the keys
        index_cache = {}
        for index, cat in enumerate(rst['cats']):
            index_cache[cat['xml_id']] = index

        keys = index_cache.keys()
        groups = self.search_read(domain=[], fields=['id', 'name', 'xml_id'])
        for group in groups:
            key = group['xml_id']
            if key in keys:
                index = index_cache[key]
                rst["cats"][index]["groups"].append(group)
                if group['id'] in implied_ids:
                    rst["cats"][index]["checkedGroups"].append(group['id'])

        return rst

    @api.model
    def add_construct_group(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'construct_group_config',
            'context': {'group_id': 0},
            'target': 'new'
        }

    @api.model
    def add_construction_group(self, group_id, group_name, cats):
        '''
        添加权限组
        :param groups:
        :return:
        '''
        val = {
            "name": group_name,
            "category_id": self.env.ref('construction_dispatch.module_category_construction_dispatch').id
        }
        implied_ids = []
        for cat in cats:
            implied_ids += cat['checkedGroups']
        val['implied_ids'] = [(6, 0, implied_ids)]

        if not group_id:
            self.create(val)
        else:
            del val['name']
            record = self.browse(group_id)
            record.write(val)

    @api.multi
    def load_set_group_action(self):
        '''
        加载action
        :return:
        '''
        return {
            'type': 'ir.actions.client',
            'tag': 'construct_group_config',
            'context': {'group_id': self.id},
            'target': 'new'
        }


