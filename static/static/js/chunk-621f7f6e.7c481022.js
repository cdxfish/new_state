(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-621f7f6e"],{"0ad0":function(t,a,e){"use strict";var s=e("240e"),i=e.n(s);i.a},"240e":function(t,a,e){},"2c45":function(t,a){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAwCAYAAADgvwGgAAACYklEQVRYR73YP4jTYBjH8d/TJG1PNC4FpVUQ6tbNTt06FVNICkLd3FS4U+gkuvhvUjcF18Opa0MDbUcHhUPBG8RDELoWFxGcpOn5yFuuR9peat7kjdmahveT99umeRsCAMuyzFwudwWA5vv+/mAw+Cn2q96oXq+fNk3zFYAbAAjAW03T7rqu+005ZlnWBcMwvgA4ezT4IRF98n2/NRwOv6sEqdlsntd1fQ/ApZWBP/u+f200Go1VgVStVo1isXiLiJ4DOBMY+A+Ad5qm3VaVVHxGaLfbW9PptMPMz1ZmcQhgfzabOSqSzrHF1mq1HjDzQwCn0ki6hFmWlTMM4w6AJ2kkXcLSTrqGpZk0FEsjaSiWRtKNmOqkkTBVSSNhYoa1Wm2rUCh0iCj2hR8ZWyS1bfs+ET2Kc+FLY0mSSmNJksbC4iZNhMkmTYTJJk2M/SspM++Zpnm12+3+UoaFJWXm30R0z/O818qwsKTMzAB2J5PJjlKsUqlky+XyNoCXi7wCI6I34/F4WxkWyPgYgBnA1Gd0HKcD4Glg/Tn3mPmjrutN13V/JJ7ZSemOZiWWgl8BNDzPm4h9iTCRLpvN7jCzWCAdpwNw4pozERaWDsABEV3v9/tiZuLbON9iYTLpgutPaUz29zARJpsuFhY3nTSWJJ00liRdZExFukiYqnSRMFXpNmKq04ViaaQLxdJIt4almW4JE48mSqXSTQAv0vgfvYQ5jnMOwHsAl4NvhN0mVo6RekmNRuNiPp8/CMxq7Q4rNeKGg//vgzJxIrZtFzKZTI2ItEwm86HX64kHZMd3WFUz+wubq5plThS7PwAAAABJRU5ErkJggg=="},b783:function(t,a,e){"use strict";e.r(a);var s=function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",{staticClass:"apanage_add"},[s("div",{staticClass:"box first arrow"},[s("label",{staticClass:"row input_row",attrs:{for:"break_type"}},[s("div",{staticClass:"left"},[t._v("\n        检查岗位:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.post}},[s("span",[t._v(t._s(t.showPostCheck))]),s("img",{attrs:{src:e("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.post,expression:"formData.post"}],attrs:{name:"post",id:"break_type"},on:{change:function(a){var e=Array.prototype.filter.call(a.target.options,function(t){return t.selected}).map(function(t){var a="_value"in t?t._value:t.value;return a});t.$set(t.formData,"post",a.target.multiple?e:e[0])}}},[s("option",{attrs:{value:""}}),s("option",{attrs:{value:"guard"}},[t._v("保安")]),s("option",{attrs:{value:"check"}},[t._v("安检")]),s("option",{attrs:{value:"clean"}},[t._v("保洁")])])])]),s("div",{staticClass:"hr"}),s("label",{staticClass:"row input_row",attrs:{for:"basis"}},[s("div",{staticClass:"left"},[t._v("\n        参考依据:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.basis}},[s("span",[t._v(t._s(this.formData.basis?this.formData.basis:"请输入参考依据"))]),s("img",{attrs:{src:e("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.basis,expression:"formData.basis"}],attrs:{type:"text",id:"basis"},domProps:{value:t.formData.basis},on:{input:function(a){a.target.composing||t.$set(t.formData,"basis",a.target.value)}}})])]),s("div",{staticClass:"hr"}),s("label",{staticClass:"row input_row",attrs:{for:"score"}},[s("div",{staticClass:"left"},[t._v("\n        考核分值:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.score}},[s("span",[t._v(t._s(this.formData.score?this.formData.score:"请输入考核分值"))]),s("img",{attrs:{src:e("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.score,expression:"formData.score"}],attrs:{type:"number",id:"score"},domProps:{value:t.formData.score},on:{input:function(a){a.target.composing||t.$set(t.formData,"score",a.target.value)}}})])]),s("div",{staticClass:"hr"}),s("label",{staticClass:"row input_row",attrs:{for:"deviceLine"}},[s("div",{staticClass:"left"},[t._v("\n        所在线路:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.deviceLine}},[s("span",[t._v(t._s(this.formData.deviceLine?this.formData.deviceLine.name:"请选择"))]),s("img",{attrs:{src:e("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.deviceLine,expression:"formData.deviceLine"}],attrs:{name:"deviceLine",id:"deviceLine"},on:{change:function(a){var e=Array.prototype.filter.call(a.target.options,function(t){return t.selected}).map(function(t){var a="_value"in t?t._value:t.value;return a});t.$set(t.formData,"deviceLine",a.target.multiple?e:e[0])}}},[s("option",{attrs:{value:""}}),t._l(t.lines,function(a){return s("option",{key:a.id,domProps:{value:a}},[t._v(t._s(a.name))])})],2)])]),s("div",{staticClass:"hr"}),s("label",{staticClass:"row input_row",attrs:{for:"devicePosition"}},[s("div",{staticClass:"left"},[t._v("\n        所在位置:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.devicePosition}},[s("span",[t._v(t._s(this.formData.devicePosition?this.formData.devicePosition.name:"请选择"))]),s("img",{attrs:{src:e("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.devicePosition,expression:"formData.devicePosition"}],attrs:{name:"devicePosition",id:"devicePosition"},on:{change:function(a){var e=Array.prototype.filter.call(a.target.options,function(t){return t.selected}).map(function(t){var a="_value"in t?t._value:t.value;return a});t.$set(t.formData,"devicePosition",a.target.multiple?e:e[0])}}},[s("option",{attrs:{value:""}}),t._l(t.stations,function(a){return s("option",{key:a.id,domProps:{value:a}},[t._v(t._s(a.name))])})],2)])])]),s("div",{staticClass:"box second"},[s("div",{staticClass:"row"},[t._v("\n      检查情况:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row textarea_box"},[s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.formData.desc,expression:"formData.desc"}],attrs:{name:"",id:"desc",rows:"5",placeholder:"请输入检查情况"},domProps:{value:t.formData.desc},on:{input:function(a){a.target.composing||t.$set(t.formData,"desc",a.target.value)}}})])]),s("div",{staticClass:"box second"},[s("div",{staticClass:"row"},[t._v("\n      发现问题:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row textarea_box"},[s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.formData.question,expression:"formData.question"}],attrs:{name:"",id:"",rows:"5",placeholder:"请输入问题"},domProps:{value:t.formData.question},on:{input:function(a){a.target.composing||t.$set(t.formData,"question",a.target.value)}}})])]),s("div",{staticClass:"box second"},[s("div",{staticClass:"row"},[t._v("\n      备注:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row textarea_box"},[s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.formData.mark,expression:"formData.mark"}],attrs:{name:"",id:"",rows:"5",placeholder:"请输入备注"},domProps:{value:t.formData.mark},on:{input:function(a){a.target.composing||t.$set(t.formData,"mark",a.target.value)}}})])]),s("div",{staticClass:"box third"},[s("div",{staticClass:"row"},[t._v("\n      照片:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row img_box"},[s("upload",{attrs:{max:9,handleClick:!0,size:"small",token:t.imgUpToken,uploadUrl:"http://up-z1.qiniu.com",images:this.formData.imgs},on:{"add-image":t.selectImg,"remove-image":t.rmImg}})],1)]),s("common-btn",{staticClass:"add_btn",on:{click:t.commitChange}},[t._v("确认提交")]),s("div",{staticClass:"blank"})],1)},i=[],o=(e("cadf"),e("551c"),e("097d"),{name:"ApanageAdd",data:function(){return{imgUpToken:"cJqhgC9wZVkfNJEKq73x5ZCKsnLzIeEOKbVLvWD7:axqBqV5JMVpDHEhCiwEZNI03KLA=:eyJzY29wZSI6IndkYXRhIiwiZGVhZGxpbmUiOjE1NDMzNzU3MjJ9",lines:[],stations:[],formData:{post:"",basis:"",score:"",deviceLine:null,devicePosition:null,desc:"",question:"",mark:"",imgs:[]}}},computed:{showPostCheck:function(){switch(this.formData.post){case"guard":return"保安";case"check":return"安检";case"clean":return"保洁";default:return"请选择"}}},methods:{selectImg:function(){var t=this;dd.biz.util.uploadImage({compression:!1,quality:100,resize:100,stickers:{time:new Date},onSuccess:function(a){t.formData.imgs.push({url:a[0]})},onFail:function(t){alert(JSON.stringify(t))}})},rmImg:function(){this.formData.imgs.splice(0,1)},getLine:function(){var t=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_line_id",[],{}).then(function(a){t.lines=a}).catch(function(t){console.log(t),alert("获取线路失败")})},getSites:function(t){var a=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_sites",[],{line_id:t}).then(function(t){a.stations=t}).catch(function(t){console.log(t),alert("获取地址失败")})},commitChange:function(){var t=this;this.$rpc.call("funenc_xa_station.belong_to_management","save_belong_to_management",[],{vals:{post_check:this.formData.post,reference_according:this.formData.basis,check_score:parseInt(this.formData.score),line_id:this.formData.deviceLine&&this.formData.deviceLine.id,site_id:this.formData.devicePosition&&this.formData.devicePosition.id,find_problem:this.formData.question,check_state:this.formData.desc,note:this.formData.mark,imgs:JSON.stringify(this.formData.imgs)}}).then(function(a){a&&t.$router.push({path:"/apanage"})}).catch(function(t){console.log(t),alert("提交失败")})}},mounted:function(){this.getLine()},watch:{"formData.deviceLine":{handler:function(t){this.getSites(t.id)}}}}),n=o,r=(e("0ad0"),e("2877")),c=Object(r["a"])(n,s,i,!1,null,"88c58b86",null);c.options.__file="Add.vue";a["default"]=c.exports}}]);
//# sourceMappingURL=chunk-621f7f6e.7c481022.js.map