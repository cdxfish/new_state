(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-75aabdee"],{"58d6":function(t,s,a){"use strict";var i=a("7638"),e=a.n(i);e.a},7638:function(t,s,a){},d2de:function(t,s,a){"use strict";a.r(s);var i=function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"faultreporting"},[a("div",{staticClass:"scroll_content_box"},[t._l(t.faultReportingData,function(s){return a("list-item",{key:s.id,attrs:{to:"/faultreporting/detail/"+s.id}},[a("div",{attrs:{slot:"firstL"},slot:"firstL"},[t._v("问题描述:")]),a("div",{staticClass:"tag",class:t.getColor(s.deal_results),attrs:{slot:"firstR"},slot:"firstR"},[t._v(t._s(s.deal_results))]),a("div",{attrs:{slot:"second"},slot:"second"},[t._v(t._s(s.break_describe||"暂无描述"))]),a("div",{attrs:{slot:"thirdL"},slot:"thirdL"},[t._v("故障类型:")]),a("div",{attrs:{slot:"thirdR"},slot:"thirdR"},[t._v(t._s(s.break_type))]),a("div",{attrs:{slot:"fourthL"},slot:"fourthL"},[t._v("提报时间:")]),a("div",{attrs:{slot:"fourthR"},slot:"fourthR"},[t._v(t._s(s.submit_time))])])}),0===t.faultReportingData.length?a("no-item"):a("div",{staticClass:"blank"})],2),a("bottom-btn",{attrs:{to:"/faultreporting/add"}},[t._v("新增检查")])],1)},e=[],o={name:"FaultReporting",data:function(){return{faultReportingData:[]}},methods:{getColor:function(t){return"已处理"===t?"yichuli":"weichuli"},getBreakData:function(){var t=this;this.$rpc.call("funenc_xa_station.break_submit","get_break_submit_list",[],{}).then(function(s){t.faultReportingData=s}).catch(function(t){console.log(t),alert("获取故障列表失败")})}},mounted:function(){this.getBreakData()}},r=o,n=(a("58d6"),a("2877")),l=Object(n["a"])(r,i,e,!1,null,"3aeaea1a",null);l.options.__file="Index.vue";s["default"]=l.exports}}]);
//# sourceMappingURL=chunk-75aabdee.3b665e45.js.map