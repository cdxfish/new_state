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
        'security/rule_group/fuenc_exam_group.xml',
        'security/rule_group/view_groups.xml',
        'security/rule_group/button_groups.xml',
        'security/rule_group/position_groups.xml',
        'security/ir.model.access.csv',
        'security/init_data.xml',
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
        'views/station_scheduling/sheduling_manage.xml',
        'views/station_scheduling/sheduling_record.xml',
        'views/check_attendance/leave.xml',
        'views/check_attendance/clock_record.xml',
        'views/check_attendance/change_shifts.xml',
        'views/check_evaluate/check_evaluate.xml',
        'views/check_evaluate/award_standard.xml',
        'views/check_evaluate/check_record.xml',
        'views/check_evaluate/check_collect.xml',
        'views/check_evaluate/award_collect.xml',
        'views/check_evaluate/award_record.xml',
        'views/check_evaluate/award_standard_import.xml',
        'views/check_evaluate/check_evaluate_import.xml',
        'views/meeting_details/meet_details.xml',
        'views/reserves_management/reserves_money.xml',
        'views/Good_deeds/suggestion_box.xml',
        'views/Good_deeds/Good_deeds.xml',
        'views/Good_deeds/guests_hurt.xml',
        'views/Good_deeds/special_money.xml',
        'views/Good_deeds/Good_deeds_type.xml',
        'views/Good_deeds/add_guests_hurt.xml',
        'views/Good_deeds/video_voice.xml',
        'views/Good_deeds/suggestion_box_type.xml',
        'views/consumables_manage/consumables_type.xml',
        'views/consumables_manage/store_house.xml',
        'views/consumables_manage/consumables_warehousing.xml',
        'views/prude_newspaper/prude_newspaper.xml',
        'views/prude_newspaper/prude_newspaper_type.xml',
        'views/prude_newspaper/prude_newpaper_write.xml',
        'views/consumables_manage/consumables_apply.xml',
        'views/consumables_manage/delivery_storage.xml',
        'views/consumables_manage/consumables_inventory.xml',
        'views/staffiong/position_settings.xml',

        'views/break_logo/break_logo_management.xml',
        'views/break_logo/break_submit.xml',
        'views/break_logo/break_type_increase.xml',
        'views/transceiver_settings/transceiver_settings.xml',
        'views/transceiver_settings/transient_break_management.xml',

        'views/production_manage/production_change_shifts.xml',
        'views/production_manage/change_shifts_setting.xml',
        'views/belong_to_management/belong_to_management.xml',
        'views/belong_to_management/belong_to_summary.xml',
        'views/work_kanban/work_kanban.xml',

        'views/work_kanban/task_type.xml',
        'views/integrated_management/station_summary.xml',
        'views/index.xml',
        'views/menu.xml',
        'views/opening_manage/train/training_plan.xml',
        'views/opening_manage/drill_plan/drill_plan.xml',
        'views/opening_manage/drill_plan/site_drill_plan.xml',


    ],
    # only loaded in demonstration mode
    # 'demo': [
    # 	'demo/demo.xml',
    # ],
    'qweb': [
        'static/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
