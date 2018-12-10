odoo.define('many2manySearchable', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var Widget = require('web.Widget');
    var ControlPanel = require('web.ControlPanel');
    var Pager = require('web.Pager');
    var FieldMany2Many = relational_fields.FieldMany2Many
    var field_registry = require('web.field_registry');
    var widgetRegistry = require('web.widget_registry');

    var CustomControlPanel = ControlPanel.extend({

        _attach_content: function (content) {
            var self = this;
            _.each(content, function ($nodeset, $element) {
                if ($nodeset && self.nodes[$element]) {
                    self.nodes[$element].append($nodeset);
                }
            });

            if ('$custom_search_area' in content && content['$custom_search_area']) {
                this.$('.custom_search_area').append(content['$custom_search_area'])
            }
        },

        _detach_content: function (elements_to_detach) {
            _.each(elements_to_detach, function ($nodeset) {
                $nodeset.contents().detach();
            });
            this.$('.custom_search_area').empty()
        },
    })

    var Many2manySearchable = FieldMany2Many.extend({
        customSearch: undefined,
        _renderControlPanel: function () {
            if (!this.view) {
                return $.when();
            }
            var self = this;
            var defs = [];

            // 使用处定义搜索
            this.control_panel = new CustomControlPanel(this, "X2ManyControlPanelEx");

            // 自定义搜索扩展, 通过option进行配置
            if (this.nodeOptions.customSearch) {
                var CustomSearch = widgetRegistry.get(this.nodeOptions.customSearch);
                this.customSearch = new CustomSearch(this)
                this.customSearch.on('custom_search_apply', this, function (evt) {
                    var ids = self.value.res_ids
                    var domain = [['id', 'in', ids]];
                    domain = domain.concat(evt.data.domain)
                    self._rpc({
                        route: '/web/dataset/search_read',
                        model: self.value.model,
                        fields: ['id'],
                        context: self.value.context,
                        domain: domain,
                        orderBy: self.value.orderBy
                    }).then(function (result) {
                        var records = result.records
                        var ids = _.pluck(records, 'id');
                        var controller = self.getParent().getParent()
                        var model = controller.model
                        model.SetVisibleIds(self.value.id, ids)
                        // 重新加载然后刷新页面
                        self.trigger_up('load', {
                            id: self.value.id,
                            on_success: function (value) {
                                self.value = value;
                                self.pager.updateState({
                                    'size': self.value.visible_ids.length,
                                    'current_min': self.value.offset + 1,
                                    'limit': self.value.limit
                                })
                                self._render();
                            },
                        });
                    })
                })
            }

            // 分页

            this.pager = new Pager(this, this.value.visible_ids.length, this.value.offset + 1, this.value.limit, {
                single_page_hidden: true,
                withAccessKey: false,
                validate: function () {
                    var isList = self.view.arch.tag === 'tree';
                    // TODO: we should have some common method in the basic renderer...
                    return isList ? self.renderer.unselectRow() : $.when();
                },
            });

            this.pager.on('pager_changed', this, function (new_state) {
                self.trigger_up('load', {
                    id: self.value.id,
                    limit: new_state.limit,
                    offset: new_state.current_min - 1,
                    on_success: function (value) {
                        self.value = value;
                        self._render();
                    },
                });
            });

            this._renderButtons();

            defs.push(this.pager.appendTo($('<div>')));
            if (this.nodeOptions.customSearch) {
                defs.push(this.customSearch.appendTo($('<div>')));
            }
            defs.push(this.control_panel.prependTo(this.$el));
            return $.when.apply($, defs).then(function () {
                self.control_panel.update({
                    cp_content: {
                        $buttons: self.$buttons,
                        $pager: self.pager.$el,
                        $custom_search_area: self.nodeOptions.customSearch? self.customSearch.$el : undefined
                    }
                });
            });
        }
    });

    // 注册搜索
    field_registry.add('Many2manySearchable', Many2manySearchable)

    return {
        Many2manySearchable: Many2manySearchable
    }
});