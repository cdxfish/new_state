
odoo.define('visible_button', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var Sidebar = require('web.Sidebar');
    var SidebarEx = require('layui_theme_sidebar_ext');
    var searchExt = require('layui_theme.search_extend');
    var _t = core._t;


   ListController.include({
        sidebar_ext: undefined,
        custom_tool_bars: [],
        customSearch: undefined,
        action_inited: false,



        renderSidebar: function ($node) {
            // 添加扩展按扭 屏蔽动作删除按钮
            if (!this.sidebar_ext) {
                this.sidebar_ext = new SidebarEx(this, {
                    env: {
                        context: this.model.get(this.handle, { raw: true }).getContext(),
                        activeIds: this.getSelectedIds(),
                        model: this.modelName,
                    },
                    actions: this.custom_tool_bars || []
                });
                this.sidebar_ext.appendTo($node);
            }

            // 添加侧边栏
            if (this.hasSidebar && !this.sidebar) {
                var other = [{
                    label: _t("Export"),
                    callback: this._onExportData.bind(this)
                }];

                if (this.archiveEnabled) {
                    other.push({
                        label: _t("Archive"),
                        callback: this._onToggleArchiveState.bind(this, true)
                    });
                    other.push({
                        label: _t("Unarchive"),
                        callback: this._onToggleArchiveState.bind(this, false)
                    });
                }

//                if (this.is_action_enabled('delete')) {
//                    other.push({
//                        label: _t('Delete'),
//                        callback: this._onDeleteSelectedRecords.bind(this)
//                    });
//                }

                this.sidebar = new Sidebar(this, {
                    editable: this.is_action_enabled('edit'),
                    env: {
                        context: this.model.get(this.handle, { raw: true }).getContext(),
                        activeIds: this.getSelectedIds(),
                        model: this.modelName,
                    },
                    actions: _.extend(this.toolbarActions.action || [].filter(function (action) {
                        if (action.binding_type != "action_button" &&
                            action.binding_type != "action_button_form" &&
                            action.binding_type != "action_button_tree") {
                            return true
                        } else {
                            return false
                        }
                    }), { other: other }),
                });

                this.sidebar.appendTo($node);
                this._toggleSidebar();
            }

        }



    });

});


