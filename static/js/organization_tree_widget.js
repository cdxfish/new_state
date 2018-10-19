odoo.define("organization_tree", function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var registry = require('web.field_registry');
    var relational_fields = require('web.relational_fields');

    /**
    * 树状的算法
    * @params list     代转化数组
    * @params parentId 起始节点
    */
    function getTrees(list, parentId) {
        let items = {};
        // 获取每个节点的直属子节点，*记住是直属，不是所有子节点
        for (let i = 0; i < list.length; i++) {
            let key = list[i].parent_id;
            if (items[key]) {
                items[key].push(list[i]);
            } else {
                items[key] = [];
                items[key].push(list[i]);
            }
        }
        return formatTree(items, parentId);
    }

    /**
     * 利用递归格式化每个节点
     */
    function formatTree(items, parentId) {
        let result = [];
        if (!items[parentId]) {
            return result;
        }
        for (let t of items[parentId]) {
            t.children = formatTree(items, t.id)
            result.push(t);
        }
        return result;
    }

    var organization_tree = relational_fields.FieldMany2One.extend({
        resetOnAnyFieldChange: true,

        init: function (parent, name, record, options) {
            console.log(options)
            this._super.apply(this, arguments);
            this.res_ids = record.data[name].res_ids
            this.operations = [];
            this.isReadonly = this.mode === 'readonly';
            this.view = this.attrs.views[this.attrs.mode];
            this.list_id = this.view.view_id;
            this.data_model = this.view.model
            this.activeActions = {};
            this.recordParams = { fieldName: this.name, viewType: this.viewType };
        },
        start: function () {
            return this._renderList();
        },
        _render: function () {
            var res_ids = this.recordData[this.name].res_ids;
            this._vue.$refs.tree.setCheckedKeys(res_ids)
        },
        _renderList: function () {
            var setTree = this._setTree()
            if (this.isReadonly) {
                setTree.then(this._reanonlyRender())
            } else {
                setTree.then(this._editRender())
            }
        },
        _setTree: function () {
            var self = this;
            var option = this.isReadonly ? 'show-checkbox :default-checked-keys=' + JSON.stringify(self.res_ids) : 'show-checkbox @check="handleCheckChange" :default-checked-keys=' + JSON.stringify(self.res_ids);
            if(this.attrs.check_strictly && this.attrs.check_strictly === '1'){
                option += ' check-strictly="true" default-expand-all'
            }
            var template =
                '<div id="tree_' +
                self.list_id +
                '" style="width:199px; top:0px; bottom: 0px;"><el-tree ref="tree" :data="data" node-key="id" highlight-current :props="defaultProps" ' + option + '></el-tree></div>';
            return $.when(
                self.$el.append(template)
            )
        },
        _reanonlyRender: function () {
            var self = this;
            self._rpc({
                model: self.data_model,
                method: 'get_tree_data',
                kwargs: { 'disabled': true }
            }).then(function (data) {
                setTimeout(function () {
                    self._vue = new Vue({
                        el: "#tree_" + self.list_id,
                        data() {
                            return {
                                defaultProps: {
                                    children: "children",
                                    label: "label",
                                    id: "id",
                                },
                                data: data.tree
                            };
                        },
                    })
                })
            })
        },
        _editRender: function () {
            var self = this;
            self._rpc({
                model: self.data_model,
                method: 'get_tree_data',
                kwargs: { 'disabled': false }
            }).then(function (data) {
                setTimeout(function () {
                    self._vue = new Vue({
                        el: "#tree_" + self.list_id,
                        data() {
                            return {
                                defaultProps: {
                                    children: "children",
                                    label: "label",
                                    id: "id",
                                },
                                data: data.tree
                            };
                        },
                        methods: {
                            handleCheckChange(data, checked) {
                                var this_vue = this;
                                var check_nodes = this_vue.$refs.tree.getCheckedNodes();

                                var values = check_nodes.map(function (item) {
                                    return item.id
                                });
                                self._setValue({
                                    operation: 'REPLACE_WITH',
                                    ids: values,
                                });
                            },

                        }
                    })
                })
            })
        }
    });

    registry.add('organization_tree', organization_tree);

    return { organization_tree: organization_tree }
});
