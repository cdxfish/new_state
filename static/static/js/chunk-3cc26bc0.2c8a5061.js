(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3cc26bc0"],{4946:function(a,t,s){"use strict";var i=s("d1d3"),e=s.n(i);e.a},"7dfe":function(a,t,s){"use strict";s.r(t);var i=function(){var a=this,t=a.$createElement,s=a._self._c||t;return s("div",{staticClass:"apanage_detail"},[s("div",{staticClass:"box first"},[s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[a._v("\n        设备位置:\n      ")]),s("div",{staticClass:"right"},[a._v("\n        "+a._s(a.apanageDetail.devicePosition)+"\n      ")])])]),s("div",{staticClass:"box second"},[s("div",{staticClass:"row"},[a._v("\n      检查情况:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[a._v("\n      "+a._s(a.apanageDetail.check_state||"暂无")+"\n    ")])]),s("div",{staticClass:"box third"},[s("div",{staticClass:"row"},[a._v("\n      发现问题:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[a._v("\n      "+a._s(a.apanageDetail.find_problem||"暂无")+"\n    ")])]),s("div",{staticClass:"box fourth"},[s("div",{staticClass:"row"},[a._v("\n      备注:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[a._v("\n      "+a._s(a.apanageDetail.note||"暂无")+"\n    ")])]),s("div",{staticClass:"box fifth"},[s("div",{staticClass:"row"},[a._v("\n      现场图片:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},a._l(a.apanageDetail.imgs,function(a){return s("div",{key:a.url,staticClass:"img_box"},[s("img",{directives:[{name:"preview",rawName:"v-preview",value:a.url,expression:"item.url"}],attrs:{src:a.url,alt:""}})])}))]),s("div",{staticClass:"box sixth"},[s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[a._v("\n        检查岗位:\n      ")]),s("div",{staticClass:"right"},[a._v("\n        "+a._s(a.apanageDetail.post_check)+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[a._v("\n        参考依据:\n      ")]),s("div",{staticClass:"right"},[a._v("\n        "+a._s(a.apanageDetail.reference_according)+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[a._v("\n        考核分值:\n      ")]),s("div",{staticClass:"right"},[a._v("\n        "+a._s(a.apanageDetail.summary_score)+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[a._v("\n        检查时间:\n      ")]),s("div",{staticClass:"right"},[a._v("\n        "+a._s(a.apanageDetail.check_time)+"\n      ")])])]),s("div",{staticClass:"blank"})])},e=[],n={name:"ApanageDetail",data:function(){return{id:"",apanageDetail:{id:1,check_state:"",find_problem:"",note:"",post_check:"",reference_according:"",summary_score:"",check_time:"",imgs:[]}}},methods:{getApanageData:function(a){var t=this;this.$rpc.call("funenc_xa_station.belong_to_management","get_belong_to_management_by_id",[],{id:a}).then(function(a){t.apanageDetail=a,t.apanageDetail.imgs&&(t.apanageDetail.imgs=JSON.parse(t.apanageDetail.imgs))}).catch(function(a){console.log(a),alert("获取规章制度失败")})}},computed:{},mounted:function(){this.id=this.$route.params.id,this.getApanageData(this.id)}},c=n,l=(s("4946"),s("2877")),r=Object(l["a"])(c,i,e,!1,null,"44556f4c",null);r.options.__file="Detail.vue";t["default"]=r.exports},d1d3:function(a,t,s){}}]);
//# sourceMappingURL=chunk-3cc26bc0.2c8a5061.js.map