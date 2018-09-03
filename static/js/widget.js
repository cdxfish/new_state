/**
 * Created by artorias on 2018/7/13.
 */
odoo.define("one2many_image_read_widget", function(require) {
  "use strict";

  var registry = require("web.field_registry");
  var relational_fields = require("web.relational_fields");

  var one2many_image_read_widget = relational_fields.FieldOne2Many.extend({
    _render: function() {
      var self = this;
      var id = self.record.data.id;
      var mode = self.mode;
      var relation_field = self.field.relation_field;
      var model = self.field.relation;
      if (mode == "edit") {
        this._super();
      } else {
        self
          ._rpc({
            model: model,
            method: "search_read",
            domain: [[relation_field, "=", id]]
          })
          .then(function(data) {
            if (data.length > 0) {
              var $el = $(
                '<div class="one2many_image_read_widget" style="display: flex; flex-wrap: wrap; justify-content: flex-start"></div>'
              );
              for (var i in data) {
                $el.append(
                  '<img src="data:image/png;base64,' + data[i].datas + '">'
                );
              }
              self.replaceElement($el);
              $el.find("img").on("click", function() {
                layui.layer.photos({
                  photos: self.$el,
                  anim: 0,
                  tab: function() {
                    $(".layui-layer-phimg img").on({
                      mousewheel: MouseWheelHandler,
                      DOMMouseScroll: MouseWheelHandler
                    });
                  }
                });
                function MouseWheelHandler(e) {
                  // cross-browser wheel delta
                  var e = window.event || e; // old IE support
                  var delta = Math.max(
                    -1,
                    Math.min(1, e.wheelDelta || -e.detail)
                  );
                  var layer = $(".layui-layer")[0];
                  var photos = $("#layui-layer-photos")[0];

                  layer.style.width =
                    Math.max(
                      50,
                      Math.min(
                        2200,
                        Number(layer.style.width.replace("px", "")) + 30 * delta
                      )
                    ) + "px";
                  photos.style.height =
                    Math.max(
                      50,
                      Math.min(
                        1200,
                        Number(photos.style.height.replace("px", "")) +
                          30 * delta
                      )
                    ) + "px";
                  return false;
                }
              });
            }
          });
      }
    }
  });
  registry.add("one2many_image_read_widget", one2many_image_read_widget);
  return { one2many_image_read_widget: one2many_image_read_widget };
});
