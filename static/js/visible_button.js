
odoo.define('visible_button', function (require) {
    "use strict";

    var core = require('web.core');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');

    ListView.include({

        init: function () {
            this._super.apply(this, arguments);
            console.log('11',$('#id_1'))
            $('#id_1').css('dispaly','none')
        },

//        render_buttons: function ($node) {
//            var self = this;
//            this._super($node);
//            self.$buttons.find('#id_1').hide()
//
//            /*
//             * 隐藏客户列表 创建按钮
//             * */
////            if (!tester_has_right && !region_customer_create) {
////                self.$buttons.find('#res_partner_list').hide();
////            }
//
//
//
//        },
        start: function () {
            var self = this;
            self._super();
            alert(33);
//            var Users = new Model("res.users");
//            Users.call('has_group', ['group_sobey.sale_sobey_leader']).done(function (has) {
//                console.log("has_right: " + has);
//                leader_has_right = has;
//            });


        }
        ,
    })
    ;
    FormView.include({
        render_buttons: function ($node) {
            var self = this;
            this._super($node);
            /*
             * 隐藏现金流任务 创建按钮
             * */
            if (!tester_has_right && !cash_flow_management_create) {
                self.$buttons.find('#cash_flow_mge_1').hide();
            }



        },
    });

});


