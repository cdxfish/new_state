/**
 * Created by artorias on 2018/7/13.
 */
odoo.define("one2many_image_read_widget", function(require) {
  "use strict";

  var registry = require("web.field_registry");
  var relational_fields = require("web.relational_fields");
  var AbstractField = require('web.AbstractField');

  var one2many_image_read_widget = AbstractField.extend({

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


       var img_id_list=[];
       for ( var i=0;i<self.record.data.load_file_test.data.length;i++){
         var img_id = self.record.data.load_file_test.data[i].data['id'];
         img_id_list.push(img_id)
       }

      var model = self.field.relation;
      if (mode == "edit") {
        this._super();
      } else {
        self
          ._rpc({
            model: model,
            method: "search_read",
            domain: [['id', "in", img_id_list]]
          })
          .then(function(data) {
//          console.log('二狗',img_id_list);
//          console.log(/web/content/' + attachment.id + '?download=true);
            if (img_id_list) {
              var $el = $(
                '<div class="one2many_image_read_widget" style="display: flex; flex-wrap: wrap; justify-content: flex-start"></div>'
              );
              for (var i in img_id_list) {
                $el.append(
                  '<img  height="80" width="80" style="margin:4px;background-color: rgba(185, 211, 238,.6)" class="img-rounded" src="/web/content/'+img_id_list[i]+'?download=true">'
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
