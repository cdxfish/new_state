odoo.define("browse_image_in_tree", function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');

    var browse_image_in_tree = basic_fields.FieldBinaryImage.extend({

        _render: function(){
            var self = this;
            this._super()
            setTimeout(function(){
                var $dom = self.$el.find('img');
                $dom.hover(function(){
                    $(this).css("cursor","help")
                })
                $dom.on('click', function(){
                        layui.layer.photos({
                          photos: {
                            "data": [{"src": "data:image/png;base64," + self.value}]
                          }
                          ,anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机（请注意，3.0之前的版本用shift参数）
                        });
                    })
                })


        }

    })
    registry.add('browse_image_in_tree', browse_image_in_tree);

    return {browse_image_in_tree: browse_image_in_tree}


})