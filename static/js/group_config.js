odoo.define('construct_dispatch.group_config', function (require) {
  "use strict";

  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 12345

  var construct_group_config = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'group_config' + construct_id++,
    init: function (parent, action) {
      this._super.apply(this, arguments)
      this.group_id = action.context.group_id
      if (this.group_id) {
        this.is_update = true
      }
    },
    start: function () {
      this._super.apply(this, arguments)

      var self = this;
      this._rpc({
        model: 'res.groups',
        method: 'get_group_data',
        args: [self.group_id],
      }).then(function (res) {

        var template = res.template
        self.replaceElement($(template));
        self.$el.attr('id', self.dom_id)

        setTimeout(function () {

          new Vue({
            el: "#" + self.dom_id,
            data() {
              return {
                cats: res.cats,
                group_name: '',
                group_id: self.group_id,
                is_update: self.is_update
              };
            },

            methods: {
              handleCheckAllChange: function (cat) {
                if (cat.checkAll) {
                  cat.checkedGroups = _.pluck(cat.groups, 'id');
                } else {
                  cat.checkedGroups = []
                }
                cat.isIndeterminate = false
              },

              handleCheckedCitiesChange: function (cat) {
                var checkedCount = cat.checkedGroups.length;
                cat.checkAll = checkedCount === cat.groups.length;
                cat.isIndeterminate = checkedCount > 0 && checkedCount < cat.groups.length;
              },

              save_group: function () {

                if (!this.group_id && this.group_name == '') {
                  this.$notify({
                    title: '警告',
                    message: '名称不能为空',
                    type: 'warning'
                  });
                  return
                }

                self._rpc({
                  model: 'res.groups',
                  method: 'add_construction_group',
                  args: [this.group_id, this.group_name, this.cats],
                }).then(function () {
                  self.do_action({
                    type: 'ir.actions.act_window_close'
                  })
                })
              }
            }
          }, 0)
        })
      })
    }
  });

  core.action_registry.add('construct_group_config', construct_group_config);
  return construct_group_config;
});
