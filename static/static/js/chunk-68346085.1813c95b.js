(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-68346085"],{"2c45":function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAwCAYAAADgvwGgAAACYklEQVRYR73YP4jTYBjH8d/TJG1PNC4FpVUQ6tbNTt06FVNICkLd3FS4U+gkuvhvUjcF18Opa0MDbUcHhUPBG8RDELoWFxGcpOn5yFuuR9peat7kjdmahveT99umeRsCAMuyzFwudwWA5vv+/mAw+Cn2q96oXq+fNk3zFYAbAAjAW03T7rqu+005ZlnWBcMwvgA4ezT4IRF98n2/NRwOv6sEqdlsntd1fQ/ApZWBP/u+f200Go1VgVStVo1isXiLiJ4DOBMY+A+Ad5qm3VaVVHxGaLfbW9PptMPMz1ZmcQhgfzabOSqSzrHF1mq1HjDzQwCn0ki6hFmWlTMM4w6AJ2kkXcLSTrqGpZk0FEsjaSiWRtKNmOqkkTBVSSNhYoa1Wm2rUCh0iCj2hR8ZWyS1bfs+ET2Kc+FLY0mSSmNJksbC4iZNhMkmTYTJJk2M/SspM++Zpnm12+3+UoaFJWXm30R0z/O818qwsKTMzAB2J5PJjlKsUqlky+XyNoCXi7wCI6I34/F4WxkWyPgYgBnA1Gd0HKcD4Glg/Tn3mPmjrutN13V/JJ7ZSemOZiWWgl8BNDzPm4h9iTCRLpvN7jCzWCAdpwNw4pozERaWDsABEV3v9/tiZuLbON9iYTLpgutPaUz29zARJpsuFhY3nTSWJJ00liRdZExFukiYqnSRMFXpNmKq04ViaaQLxdJIt4almW4JE48mSqXSTQAv0vgfvYQ5jnMOwHsAl4NvhN0mVo6RekmNRuNiPp8/CMxq7Q4rNeKGg//vgzJxIrZtFzKZTI2ItEwm86HX64kHZMd3WFUz+wubq5plThS7PwAAAABJRU5ErkJggg=="},4345:function(t,e,a){"use strict";a.r(e);var i=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"faultreporting_add"},[i("div",{staticClass:"box first arrow"},[i("label",{staticClass:"row input_row",attrs:{for:"break_type"}},[i("div",{staticClass:"left"},[t._v("\n        故障类型:\n      ")]),i("div",{staticClass:"right",class:{placeholder:!this.formData.category}},[i("span",[t._v(t._s(this.formData.category?this.formData.category.break_type:"请选择"))]),i("img",{attrs:{src:a("2c45"),alt:""}})]),i("div",{staticClass:"input_box"},[i("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.category,expression:"formData.category"}],attrs:{name:"category",id:"break_type"},on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){var e="_value"in t?t._value:t.value;return e});t.$set(t.formData,"category",e.target.multiple?a:a[0])}}},[i("option",{attrs:{value:""}}),t._l(t.breakTypes,function(e){return i("option",{key:e.id,domProps:{value:e}},[t._v(t._s(e.break_type))])})],2)])]),i("div",{staticClass:"hr"}),i("label",{staticClass:"row input_row",attrs:{for:"device_name"}},[i("div",{staticClass:"left"},[t._v("\n        设备名称:\n      ")]),i("div",{staticClass:"right",class:{placeholder:!this.formData.deviceName}},[i("span",[t._v(t._s(this.formData.deviceName?this.formData.deviceName:"请输入设备名称"))]),i("img",{attrs:{src:a("2c45"),alt:""}})]),i("div",{staticClass:"input_box"},[i("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.deviceName,expression:"formData.deviceName"}],attrs:{type:"text",id:"device_name"},domProps:{value:t.formData.deviceName},on:{input:function(e){e.target.composing||t.$set(t.formData,"deviceName",e.target.value)}}})])]),i("div",{staticClass:"hr"}),i("label",{staticClass:"row input_row",attrs:{for:"device_no"}},[i("div",{staticClass:"left"},[t._v("\n        设备编号:\n      ")]),i("div",{staticClass:"right",class:{placeholder:!this.formData.deviceNo}},[i("span",[t._v(t._s(this.formData.deviceNo?this.formData.deviceNo:"请输入设备编号"))]),i("img",{attrs:{src:a("2c45"),alt:""}})]),i("div",{staticClass:"input_box"},[i("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.deviceNo,expression:"formData.deviceNo"}],attrs:{type:"text",id:"device_no"},domProps:{value:t.formData.deviceNo},on:{input:function(e){e.target.composing||t.$set(t.formData,"deviceNo",e.target.value)}}})])]),i("div",{staticClass:"hr"}),i("label",{staticClass:"row input_row",attrs:{for:"device_line"}},[i("div",{staticClass:"left"},[t._v("\n        所在线路:\n      ")]),i("div",{staticClass:"right",class:{placeholder:!this.formData.deviceLine}},[i("span",[t._v(t._s(this.formData.deviceLine?this.formData.deviceLine.name:"请选择"))]),i("img",{attrs:{src:a("2c45"),alt:""}})]),i("div",{staticClass:"input_box"},[i("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.deviceLine,expression:"formData.deviceLine"}],attrs:{name:"deviceLine",id:"device_line"},on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){var e="_value"in t?t._value:t.value;return e});t.$set(t.formData,"deviceLine",e.target.multiple?a:a[0])}}},[i("option",{attrs:{value:""}}),t._l(t.lines,function(e){return i("option",{key:e.id,domProps:{value:e}},[t._v(t._s(e.name))])})],2)])]),i("div",{staticClass:"hr"}),i("label",{staticClass:"row input_row",attrs:{for:"device_position"}},[i("div",{staticClass:"left"},[t._v("\n        所在位置:\n      ")]),i("div",{staticClass:"right",class:{placeholder:!this.formData.devicePosition}},[i("span",[t._v(t._s(this.formData.devicePosition?this.formData.devicePosition.name:"请选择"))]),i("img",{attrs:{src:a("2c45"),alt:""}})]),i("div",{staticClass:"input_box"},[i("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.devicePosition,expression:"formData.devicePosition"}],attrs:{name:"devicePosition",id:"device_position"},on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){var e="_value"in t?t._value:t.value;return e});t.$set(t.formData,"devicePosition",e.target.multiple?a:a[0])}}},[i("option",{attrs:{value:""}}),t._l(t.stations,function(e){return i("option",{key:e.id,domProps:{value:e}},[t._v(t._s(e.name))])})],2)])])]),i("div",{staticClass:"box second"},[i("div",{staticClass:"row"},[t._v("\n      故障描述:\n    ")]),i("div",{staticClass:"hr"}),i("div",{staticClass:"row textarea_box"},[i("textarea",{directives:[{name:"model",rawName:"v-model",value:t.formData.desc,expression:"formData.desc"}],attrs:{name:"",id:"",rows:"10",placeholder:"请输入故障描述"},domProps:{value:t.formData.desc},on:{input:function(e){e.target.composing||t.$set(t.formData,"desc",e.target.value)}}})])]),i("div",{staticClass:"box third"},[i("div",{staticClass:"row"},[t._v("\n      照片:\n    ")]),i("div",{staticClass:"hr"}),i("div",{staticClass:"row img_box"},[i("upload",{attrs:{max:9,handleClick:!0,size:"small",token:t.imgUpToken,uploadUrl:"http://up-z1.qiniu.com",images:t.formData.imgs},on:{"add-image":t.selectImg,"remove-image":t.rmImg}})],1)]),i("common-btn",{staticClass:"add_btn",on:{click:t.commitChange}},[t._v("确认提交")]),i("div",{staticClass:"blank"})],1)},s=[],o=a("badb"),n=a.n(o),r=(a("dc12"),{name:"FaultReportingAdd",data:function(){return{imgUpToken:"",lines:[],stations:[],breakTypes:[],formData:{category:"",deviceName:"",deviceNo:"",deviceLine:"",devicePosition:"",desc:"",imgs:[]}}},computed:{sendee:function(){if(this.formData.sendee&&this.formData.sendee.length>0)return this.formData.sendee.map(function(t){return t.name}).join(",")}},methods:{selectImg:function(){var t=this;dd.biz.util.uploadImage({compression:!1,quality:100,resize:100,stickers:{time:new Date},onSuccess:function(e){t.formData.imgs.push({url:e[0]})},onFail:function(t){alert(n()(t))}})},rmImg:function(){this.formData.imgs.splice(0,1)},commitChange:function(){var t=this;console.log(this.formData),this.$rpc.call("funenc_xa_station.break_submit","save_break_submit",[],{vals:{break_type:this.formData.category&&this.formData.category.id,equipment_name:this.formData.deviceName,equipment_number:this.formData.deviceNo,break_describe:this.formData.desc,line_id:this.formData.deviceLine&&this.formData.deviceLine.id,site_id:this.formData.devicePosition&&this.formData.devicePosition.id,url:n()(this.formData.imgs)}}).then(function(e){e&&t.$router.push({path:"/faultreporting"})}).catch(function(t){console.log(t),alert("提交失败")})},getLine:function(){var t=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_line_id",[],{}).then(function(e){t.lines=e}).catch(function(t){console.log(t),alert("获取线路失败")})},getSites:function(t){var e=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_sites",[],{line_id:t}).then(function(t){e.stations=t}).catch(function(t){console.log(t),alert("获取地址失败")})},getBreakType:function(){var t=this;this.$rpc.call("funenc_xa_staion.break_type_increase","get_break_type",[],{}).then(function(e){t.breakTypes=e,console.log(t.breakTypes)}).catch(function(t){console.log(t),alert("获取故障类型失败")})}},mounted:function(){this.getLine(),this.getBreakType()},watch:{"formData.deviceLine":{handler:function(t){this.getSites(t.id)}}}}),c=r,l=(a("ae40"),a("fc05")),m=Object(l["a"])(c,i,s,!1,null,"17bd656a",null);e["default"]=m.exports},8394:function(t,e,a){},ae40:function(t,e,a){"use strict";var i=a("8394"),s=a.n(i);s.a},dc12:function(t,e,a){var i=a("7847").f,s=Function.prototype,o=/^\s*function ([^ (]*)/,n="name";n in s||a("3016")&&i(s,n,{configurable:!0,get:function(){try{return(""+this).match(o)[1]}catch(t){return""}}})}}]);
//# sourceMappingURL=chunk-68346085.1813c95b.js.map