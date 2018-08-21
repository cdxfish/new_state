odoo.define("week_tree_btns_func", function (require) {
	// 触发按钮响应
	function trigger(self, e) {
		self.trigger_up("button_clicked", {
			attrs: {
				type: $(e.currentTarget).attr("type"),
				name: $(e.currentTarget).attr("name")
			},
			record: self.record
		});
	}
	
	return {
		//查看流程
		"click button.process": function (e) {
			e.stopPropagation();
			console.log("click button.process");
		}
	};
});
