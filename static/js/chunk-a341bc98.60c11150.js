(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-a341bc98"],{"2c45":function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAwCAYAAADgvwGgAAACYklEQVRYR73YP4jTYBjH8d/TJG1PNC4FpVUQ6tbNTt06FVNICkLd3FS4U+gkuvhvUjcF18Opa0MDbUcHhUPBG8RDELoWFxGcpOn5yFuuR9peat7kjdmahveT99umeRsCAMuyzFwudwWA5vv+/mAw+Cn2q96oXq+fNk3zFYAbAAjAW03T7rqu+005ZlnWBcMwvgA4ezT4IRF98n2/NRwOv6sEqdlsntd1fQ/ApZWBP/u+f200Go1VgVStVo1isXiLiJ4DOBMY+A+Ad5qm3VaVVHxGaLfbW9PptMPMz1ZmcQhgfzabOSqSzrHF1mq1HjDzQwCn0ki6hFmWlTMM4w6AJ2kkXcLSTrqGpZk0FEsjaSiWRtKNmOqkkTBVSSNhYoa1Wm2rUCh0iCj2hR8ZWyS1bfs+ET2Kc+FLY0mSSmNJksbC4iZNhMkmTYTJJk2M/SspM++Zpnm12+3+UoaFJWXm30R0z/O818qwsKTMzAB2J5PJjlKsUqlky+XyNoCXi7wCI6I34/F4WxkWyPgYgBnA1Gd0HKcD4Glg/Tn3mPmjrutN13V/JJ7ZSemOZiWWgl8BNDzPm4h9iTCRLpvN7jCzWCAdpwNw4pozERaWDsABEV3v9/tiZuLbON9iYTLpgutPaUz29zARJpsuFhY3nTSWJJ00liRdZExFukiYqnSRMFXpNmKq04ViaaQLxdJIt4almW4JE48mSqXSTQAv0vgfvYQ5jnMOwHsAl4NvhN0mVo6RekmNRuNiPp8/CMxq7Q4rNeKGg//vgzJxIrZtFzKZTI2ItEwm86HX64kHZMd3WFUz+wubq5plThS7PwAAAABJRU5ErkJggg=="},3060:function(t,e,a){},"3cf4":function(t,e,a){"use strict";var s=a("9184"),i=a.n(s);i.a},7050:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"kanban_add"},[s("div",{staticClass:"box first arrow"},[s("div",{staticClass:"row",on:{click:t.showSelcetSendee}},[s("div",{staticClass:"left"},[t._v("\n        任务接收人:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!t.sendee}},[s("span",[t._v(t._s(t.sendee?t.sendee:"请选择"))]),s("img",{attrs:{src:a("2c45"),alt:""}})])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务类型:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.category}},[s("span",[t._v(t._s(this.formData.category?this.formData.category.name:"请选择"))]),s("img",{attrs:{src:a("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.category,expression:"formData.category"}],attrs:{name:"category",id:"category"},on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){var e="_value"in t?t._value:t.value;return e});t.$set(t.formData,"category",e.target.multiple?a:a[0])}}},[s("option",{attrs:{value:""}}),t._l(t.category,function(e){return s("option",{key:e.id,domProps:{value:e}},[t._v(t._s(e.name))])})],2)])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        优先级:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.level}},[s("span",[t._v(t._s(this.formData.level?this.formData.level:"请选择"))]),s("img",{attrs:{src:a("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.formData.level,expression:"formData.level"}],attrs:{name:"level",id:"level"},on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){var e="_value"in t?t._value:t.value;return e});t.$set(t.formData,"level",e.target.multiple?a:a[0])}}},[s("option",{attrs:{value:""}}),s("option",{attrs:{value:"高"}},[t._v("高")]),s("option",{attrs:{value:"中"}},[t._v("中")]),s("option",{attrs:{value:"低"}},[t._v("低")])])])])]),s("div",{staticClass:"box second arrow"},[s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        开始时间:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.beginTime}},[s("span",[t._v(t._s(this.formData.beginTime?t.formatDateTime(this.formData.beginTime):"请选择开始时间"))]),s("img",{attrs:{src:a("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.beginTime,expression:"formData.beginTime"}],attrs:{type:"datetime-local"},domProps:{value:t.formData.beginTime},on:{input:function(e){e.target.composing||t.$set(t.formData,"beginTime",e.target.value)}}})])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        结束时间:\n      ")]),s("div",{staticClass:"right",class:{placeholder:!this.formData.deadLine}},[s("span",[t._v(t._s(this.formData.deadLine?t.formatDateTime(this.formData.deadLine):"请选择结束时间"))]),s("img",{attrs:{src:a("2c45"),alt:""}})]),s("div",{staticClass:"input_box"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.deadLine,expression:"formData.deadLine"}],attrs:{type:"datetime-local"},domProps:{value:t.formData.deadLine},on:{input:function(e){e.target.composing||t.$set(t.formData,"deadLine",e.target.value)}}})])])]),s("div",{staticClass:"box third"},[s("div",{staticClass:"row"},[t._v("\n      任务描述:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row textarea_box"},[s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.formData.desc,expression:"formData.desc"}],attrs:{name:"",id:"",rows:"10",placeholder:"请输入问题"},domProps:{value:t.formData.desc},on:{input:function(e){e.target.composing||t.$set(t.formData,"desc",e.target.value)}}})])]),s("common-btn",{staticClass:"add_btn",on:{click:t.commitChange}},[t._v("确认提交")]),s("div",{staticClass:"blank"}),t.isSelcetSendeeShow?s("my-dialog",[s("architecture",{on:{selectUser:t.selectUser}})],1):t._e()],1)},i=[],n=(a("7f7f"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"architecture"},[a("div",{staticClass:"scroll_content_box"},[t._l(t.showDepartment,function(e){return a("div",{key:e.id,staticClass:"box"},[a("ul",[a("tree",{attrs:{model:e},on:{selectUser:t.selectUser}})],1)])}),a("common-btn",{staticClass:"add_btn",on:{click:t.commitChange}},[t._v("确认选择")])],2)])}),r=[],o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"tree"},[s("li",{staticClass:"box"},[s("div",{staticClass:"row",style:{"text-indent":2*t.model.level+"em"},on:{click:function(e){t.toggle()}}},[t.isFolder?s("span",[t._v(" "+t._s(t.model.name))]):s("label",{staticClass:"label_box"},[s("input",{attrs:{type:"checkbox",name:"user",disabled:""},domProps:{checked:t.checked}}),s("img",{attrs:{src:t.model.avatar,alt:""}}),s("span",[t._v(t._s(t.model.name))]),s("span",[t._v(t._s(t.model.jobnumber))]),s("span",[t._v(t._s(t.model.position))])]),t.isFolder?s("span",{staticClass:"ricon"},[t.open?s("img",{staticClass:"xia",attrs:{src:a("865d"),alt:""}}):s("img",{staticClass:"zuo",attrs:{src:a("2c45"),alt:""}})]):t._e()]),s("div",{staticClass:"hr"}),t.isFolder?s("ul",{directives:[{name:"show",rawName:"v-show",value:t.open,expression:"open"}]},t._l(t.model.children,function(e,a){return s("tree",{key:a,attrs:{model:e},on:{selectUser:t.selectUser}})})):t._e()])])},c=[],l=(a("ac6a"),{name:"Tree",props:{model:Object},inject:["users"],data:function(){return{open:!1,checked:!1}},computed:{isFolder:function(){return this.model.children}},methods:{toggle:function(){var t=this;if(this.isFolder)0===this.model.children.length?this.getUser(this.model.id):this.open=!this.open;else{var e=this.users.filter(function(e){return e.id===t.model.id});if(0===e.length)this.users.push(this.model),this.checked=!0;else{var a=this.users.indexOf(e[0]);a>-1&&this.users.splice(a,1),this.checked=!1}this.$emit("selectUser",this.users)}},getUser:function(t){var e=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_users_by_department_id",[],{departmentid:t}).then(function(t){var a=[];t.forEach(function(t){a.push({name:t.name,id:t.id,departmentId:t.departmentId,jobnumber:t.jobnumber,avatar:t.avatar,position:t.position,isworker:!0,level:e.model.level+1,select:!1})}),e.$set(e.model,"children",a),e.open=!0}).catch(function(t){console.log(t)})},selectUser:function(){this.$emit("selectUser",this.users)}},mounted:function(){}}),d=l,m=(a("c43b"),a("2877")),u=Object(m["a"])(d,o,c,!1,null,"3951d392",null);u.options.__file="Tree.vue";var h=u.exports,v={name:"Architecture",components:{Tree:h},provide:{users:[]},data:function(){return{parentid:1,department:[],users:[]}},computed:{showDepartment:{get:function(){var t=JSON.parse(JSON.stringify(this.department));return this.getTree(t,this.parentid)}}},methods:{getTree:function(t){for(var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:1,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],s=arguments.length>3&&void 0!==arguments[3]?arguments[3]:0,i=0;i<t.length;i++)t[i]["parentid"]===e&&(t[i]["children"]=[],t[i]["level"]=s,a.push(t[i]),this.getTree(t,t[i]["departmentId"],t[i]["children"],s+1));return a},getDeparment:function(){var t=this;this.$rpc.call("cdtct_dingtalk.cdtct_dingtalk_department","get_xa_departments",[],{}).then(function(e){t.department=e.departments,t.parentid=e.root_department}).catch(function(t){console.log(t)})},selectUser:function(t){this.users=t},commitChange:function(){this.$emit("selectUser",this.users)}},mounted:function(){this.getDeparment()}},f=v,p=(a("ab01"),Object(m["a"])(f,n,r,!1,null,"4f1fa7ee",null));p.options.__file="Architecture.vue";var g=p.exports,_="priority",A="intermediate",C="elementary",b={name:"KanbanAdd",components:{Architecture:g},data:function(){return{isSelcetSendeeShow:!1,category:[],formData:{sendee:[],category:"",level:"",beginTime:"",deadLine:"",desc:""}}},computed:{sendee:function(){if(this.formData.sendee&&this.formData.sendee.length>0)return this.formData.sendee.map(function(t){return t.name}).join(",")}},methods:{showSelcetSendee:function(){this.isSelcetSendeeShow=!0},getPriority:function(t){switch(t){case"高":return _;case"中":return A;case"低":return C;default:break}},formatDateTime:function(t){if(t)return this.$moment(t).format("YY-MM-DD HH:mm:ss")},commitChange:function(){var t=this;console.log(this.formData);var e=this.formData.sendee.map(function(t){return t.id});this.$rpc.call("funenc_xa_station.work_kanban","app_save_work_kanban",[],{ids:e,task_type_id:this.formData.category.id,task_priority:this.getPriority(this.formData.level),task_start_time:this.formData.beginTime,task_end_time:this.formData.deadLine,task_describe:this.formData.desc}).then(function(e){e&&t.$router.push({path:"/kanban"})}).catch(function(t){console.log(t)})},getCategory:function(){var t=this;this.$rpc.call("funenc_xa_station.task_type","get_type_all",[],{}).then(function(e){t.category=e}).catch(function(t){console.log(t)})},selectUser:function(t){this.formData.sendee=t,this.isSelcetSendeeShow=!1}},mounted:function(){this.getCategory()}},D=b,w=(a("3cf4"),Object(m["a"])(D,s,i,!1,null,"b3f1bd86",null));w.options.__file="Add.vue";e["default"]=w.exports},"7f7f":function(t,e,a){var s=a("86cc").f,i=Function.prototype,n=/^\s*function ([^ (]*)/,r="name";r in i||a("9e1e")&&s(i,r,{configurable:!0,get:function(){try{return(""+this).match(n)[1]}catch(t){return""}}})},"865d":function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAVCAYAAAAuJkyQAAACc0lEQVRIS82VO48SYRSG3zODwEig0Ci2JharcXV/gfsDjBY2XhJ0tSBkuAdMjLHYYtcCws2J1GghiVu4pT9h7TZmt7GzMRoDDQ0DzHfMR8AMLMThZnbKyZlv3u88530P4ZQ9dMr0oC9I1/UrmqbdBrBfKBS+/0+R2Wz2smVZ9wB8LpVKxxQOh8/6/X6DiJ4x85EQ4lGpVDoCwKsWlkqlrqqqWieimwA+NZvNJ7S9ve1utVovALwkojPM/MWyLL1cLh+uUlAymbzhcrkqRHQLQI+ZjUaj8aqPLB6PX3C73bJL9wFYzPyVmR8Ui8VvqxCVyWSuAfgA4DoRqcz8sdfrJSqVyq+/Qx0KhXzBYPAdM98ddOpYCPFw2fjsmJi5y8z7zWbzca1Wa8vLj7gsGo2e93g8u0S0NRB1YFlWdFn4BpjKRLQ5wFTvdDrPDcP4PSRxwvaRSOSiz+d7I/ExswVgKfiGnRliEkLstdvtRLVa/Wkfi4k5NMQH4A4ANzMvhG8Spm63GzIMwxyf0anBmE6nzymKsgvg6SLuS6fT64qiSDdNxfTPDg0L7PjmcV8mk1kDUAewLt00DZNjQbJwXvdJMUQkxWxMctO0OHG0y6T7vF7vjlN8A0xlAJtEJHPthJsWEjRLeMZisTWv11tnZseYZkJmL5Z7LxAIvLe5b2T3zYtpbkHywwn4DoQQEQBCURS5fvpuksNsmuZI6DlZQ45maPygCeF5SERg5g3pJgB7RJTI5/MjobcyQXb3DfHJd7O4aeGhnnSADE9VVV8D2GJmRdrcNM2sfTc56cpCMzT+A13XL2maFgWgqKr6NpfL/ZhVhL3+D9V9p4CMdTdGAAAAAElFTkSuQmCC"},"8e0a":function(t,e,a){},9184:function(t,e,a){},ab01:function(t,e,a){"use strict";var s=a("3060"),i=a.n(s);i.a},c43b:function(t,e,a){"use strict";var s=a("8e0a"),i=a.n(s);i.a}}]);
//# sourceMappingURL=chunk-a341bc98.60c11150.js.map