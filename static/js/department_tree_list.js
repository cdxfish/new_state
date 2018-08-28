odoo.define("department_tree_list", function (require) {
  "use strict";

  var ListView = require("web.ListView");
  var data = require("web.data");
  var view_registry = require("web.view_registry");
  var ListRenderer = require("web.ListRenderer");
  var ListController = require("web.ListController");

  var list_id = 9527;

  var departMentRender = ListRenderer.extend({
    app: undefined,
    options: {},
    list_id: "department_tree_list_0",
    data_model: undefined,
    data_load_func: undefined,

    init: function (parent, state, params) {
      this._super(parent, state, params);
      this.options = JSON.parse(params.arch.attrs.options || "{}");
      this.list_id = "department_tree_list_" + list_id++;
      this.data_model = this.options.data_model;
      this.data_load_func = this.options.data_load_func;
    },

    _renderView: function () {
      var self = this;

      return this._super().then(function () {
        if (self.app) {
          return;
        }
        self.$el.css("margin-left", "305px");
        self.$el.css("postion", "relative");

        // 添加树形控件
        self.$el.parent().css("position", "relative");
        var template =
          '<div id="' +
          self.list_id +
          '"style="width:299px; border: 1px solid rgb(204, 204, 204); padding: 5px; overflow-x: auto; float:left"><el-tree :load="loadNode" lazy :props="defaultProps" @node-click="handleNodeClick"></el-tree></div>';
        $(template).insertBefore(self.$el);

        setTimeout(function () {
          // 实例化tree
          self.app = new Vue({
            el: "#" + self.list_id,
            data() {
              return {
                defaultProps: {
                  children: "sub",
                  label: "name",
                  id: "id"
                }
              };
            },

            methods: {
              handleNodeClick(data) {
                var id = data.id < 2 ? 0 : data.id;
                if (id == 0) {
                  self.trigger_up("search", {
                    domains: [],
                    contexts: [],
                    groupbys: []
                  });
                } else {
                  self.trigger_up("search", {
                    domains: [[["departments", "=", id]]],
                    contexts: [],
                    groupbys: []
                  });
                }
              },

              loadNode(node, resolve) {
                var id = (node.data && node.data.departmentId) || 0;
                self
                  ._rpc({
                    model: self.data_model,
                    method: self.data_load_func,
                    kwargs: { pid: id }
                  })
                  .then(function (data) {
                    for (var id = 0; id < data.length; id++) {
                      if (data.isLeaf) {
                        data.leaf = true;
                      } else {
                        data.leaf = false;
                      }
                    }
                    return resolve(data);
                  });
              }
            }
          });
        }, 0);
      });
    },

    _renderHeaderCell: function (node) {
      var name = node.attrs.name;
      var order = this.state.orderedBy;
      var isNodeSorted = order[0] && order[0].name === name;
      var field = this.state.fields[name];
      var $th = $("<th>");
      if (!field) {
        return $th;
      }
      var description;
      if (node.attrs.widget) {
        description = this.state.fieldsInfo.list[name].Widget.prototype
          .description;
      }
      if (description === undefined) {
        description = node.attrs.string || field.string;
      }
      $th
        .text(description)
        .data("name", name)
        .toggleClass("o-sort-down", isNodeSorted ? !order[0].asc : false)
        .toggleClass("o-sort-up", isNodeSorted ? order[0].asc : false)
        .addClass(field.sortable && "o_column_sortable");

      if (
        field.type === "float" ||
        field.type === "integer" ||
        field.type === "monetary"
      ) {
        $th.css({ textAlign: "right" });
      }
      return $th;
    }
  });

  var department_tree_list = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
      Renderer: departMentRender,
      Controller: ListController
    }),
    viewType: "list"
  });

  view_registry.add("department_tree_list", department_tree_list);
});
