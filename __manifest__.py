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
	'depends': ['base', 'web', 'cdtct_dingtalk'],
	
	# always loaded
	'data': [
		# 'security/ir.model.access.csv',
		'views/menu.xml',
		'views/assets.xml',
		'views/opening_manage/keys_manage/key_manage.xml',
		'views/opening_manage/keys_manage/key_type.xml',
		'views/opening_manage/keys_manage/key_detail.xml',
		'views/opening_manage/keys_manage/change_record.xml',
		'views/opening_manage/keys_manage/borrow_record.xml',
	
	],
	# only loaded in demonstration mode
	# 'demo': [
	# 	'demo/demo.xml',
	# ],
	'qweb': [
		'static/xml/templates.xml',
		'static/xml/tree_btns.xml',
	],
	'installable': True,
	'auto_install': False,
	'application': True
}
