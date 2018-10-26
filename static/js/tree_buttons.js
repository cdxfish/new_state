odoo.define("treebtns", function (require) {
	"use strict";
	
	var Widget = require("web.Widget");
	var registry = require("web.widget_registry");
	var listRenderer = require("web.ListRenderer");
	var config = require("web.config")
	var core = require('web.core')

	var treebtns = Widget.extend({
		events: _.extend(Widget.prototype.events, require("week_tree_btns_func")),

		init: function (parent, record, node) {
			this._super(parent);
			this.record = record;
			this.attrs = node.attrs;
			this.template = this.attrs.template;
			if (!this.template) {
				console.log(
						"the template for template widget is undfined, please set the template attrs"
				);
			}
		},

		// 触发按钮响应
		trigger_button: function (e) {
			e.stopPropagation();
			this.trigger_up("button_clicked", {
				attrs: {
					type: $(e.currentTarget).attr("type"),
					name: $(e.currentTarget).attr("name")
				},
				record: this.record
			});
		},

		confirmClick: function (e) {
			var self = this;
			e.stopPropagation();
			layer.confirm(
					$(e.currentTarget).attr("confirm"),
					{title: "提示"},
					function () {
						self.trigger_button(e);
						layui.layer.closeAll();
					}
			);
		},
		promptClick: function (e) {
			var self = this;
			e.stopPropagation();
			layer.prompt({
				formType: 0,
				value: '',
				title: '请输入操作内容！'
			}, function (value, index) {
				if (value) {
					self.trigger_button(e,value);
					layui.layer.closeAll();
				}
			});
		},
        renderElement: function(){
            var $el;
            if (this.template) {
                $el = $(core.qweb.render(this.template, {widget: this}).trim());
            } else {
                $el = this._make_descriptive();
            }
            this.replaceElement($el);
        },

		start: function () {
			this._super();
			var self = this;

            self._rpc({
                model: 'funenc_xa_station.return.view.function',
                method: 'get_groups_with_id'
            }).then(function(data){
                console.log(data)
            })

			var serverbtns = [];
			var confirmBtns = [];
			self.$("button").each(function (index, item) {
				if (!$(item).attr("js_func")) {
					if ($(item).attr("confirm")) {
						confirmBtns.push(item);
					}else {
						serverbtns.push(item);
					}
				}
			});
			$(serverbtns).on("click", this.trigger_button.bind(this));
			$(confirmBtns).on("click", this.confirmClick.bind(this));
		},

	});
	
	registry.add("treebtns", treebtns);
	
	return {
		treebtns: treebtns
	};
});
