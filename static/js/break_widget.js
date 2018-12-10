/**
 * Created by artorias on 2018/7/13.
 */
odoo.define("break_widget", function(require) {
  "use strict";

  var registry = require("web.field_registry");
  var relational_fields = require("web.relational_fields");
  var AbstractField = require('web.AbstractField');

  var break_widget = AbstractField.extend({

    init: function(parent, name, record, options){
        console.log(parent)
        console.log(name)
        console.log(record)
        console.log(options)
        this._super(parent, name, record, options)
    },

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
            domain: [['break_submit_image', "=", self.res_id]]
          })
          .then(function(data) {
            if (data) {
            console.log(data);
              var $el = $(
                '<div class="break_widget" style="display: flex; flex-wrap: wrap; justify-content: flex-start"></div>'
              );
              for (var i in data) {

                $el.append(
                  '<img  height="80" width="80" style="margin:4px;background-color: rgba(185, 211, 238,.6)" class="img-rounded" src=' + data[i].url + '>'
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
  registry.add("break_widget", break_widget);
  return { break_widget: break_widget };
});