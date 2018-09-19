# -*- coding: utf-8 -*-
{
	'name': "funenc_xa_station",
	
	'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
	
	'description': """
        Long description of module's purpose
    """,
	
	'author': "My Company",
	'website': "http://www.yourcompany.com",
	
	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
	# for the full list
	'category': 'Uncategorized',
	'version': '0.1',
	
	# any module necessary for this one to work correctly
	'depends': ['base', 'web', 'base_import', 'cdtct_dingtalk', 'layui_theme', 'vue_template_manager'],
	
	# always loaded
	'data': [
        'security/fuenc_exam_group.xml',
		'security/ir.model.access.csv',
        'views/depot_manage/person_account_mgmt.xml',
		'views/assets.xml',
		'views/opening_manage/keys_manage/key_manage.xml',
		'views/opening_manage/keys_manage/key_type.xml',
		'views/opening_manage/keys_manage/key_detail.xml',
		'views/opening_manage/keys_manage/change_record.xml',
		'views/opening_manage/keys_manage/borrow_record.xml',
		'views/integrated_management/station_detail.xml',
		'views/add_management/add_kind.xml',
		'views/add_management/add_kind_two.xml',
		'views/add_management/views.xml',
		'views/add_certificate/add_station_certificate.xml',
		'views/add_certificate/add_per_certificate.xml',
		'views/person_management/person_information.xml',
		'views/person_management/per_management.xml',
		'views/person_management/person_second.xml',
		'views/person_management/import_file.xml',
        'views/integrated_management/ground_traffic.xml',
		'views/integrated_management/civil_engineering.xml',
        'views/integrated_management/line_turnout.xml',
        'views/integrated_management/signal_system.xml',
		'views/integrated_management/station_staffing.xml',
        'views/integrated_management/station_exit.xml',
		'views/add_management/add_kind.xml',
		'views/add_management/views.xml',
		'views/add_certificate/add_station_certificate.xml',
		'views/add_certificate/add_per_certificate.xml',
		'views/station_scheduling/arrange_order.xml',
		'views/station_scheduling/class_group.xml',
		'views/station_scheduling/arrange_class_manage.xml',
		'views/station_scheduling/motorized_user.xml',
		'views/station_scheduling/conflict_rule.xml',
		'views/check_evaluate/check_evaluate.xml',
		'views/check_evaluate/award_standard.xml',
		'views/check_evaluate/check_record.xml',
		'views/check_evaluate/check_collect.xml',
		'views/check_evaluate/award_collect.xml',
		'views/check_evaluate/award_record.xml',
        'views/menu.xml',

	
	],
	# only loaded in demonstration mode
	# 'demo': [
	# 	'demo/demo.xml',
	# ],
	'qweb': [
		'static/xml/templates.xml',
		'static/xml/tree_btns.xml',
		'static/xml/add_management.xml',
		'static/xml/add_certificate.xml',
		'static/xml/add_major_class.xml',
		'static/xml/plan_method_btn.xml',
        'static/xml/integrated_management.xml',
        'static/xml/person_info_management.xml',
        'static/xml/check_evaluate.xml',
	],
	'installable': True,
	'auto_install': False,
	'application': True
}
