(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4d8ceae8"],{"289b":function(t,s,a){"use strict";var i=a("e32b"),n=a.n(i);n.a},"7d582":function(t,s,a){"use strict";a.r(s);var i=function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"detail"},[a("div",{staticClass:"top box"},[a("div",{staticClass:"row"},[a("div",{staticClass:"left"},[t._v("\n        站点信息:\n      ")]),a("div",{staticClass:"right"},[t._v("\n        "+t._s(t.changeApplicctionData.line)+" "+t._s(t.changeApplicctionData.station)+"\n      ")])]),a("div",{staticClass:"hr"}),a("div",{staticClass:"row"},[a("div",{staticClass:"left"},[t._v("\n        个人班次:\n      ")]),a("div",{staticClass:"right"},[t.isOrigin?a("span",[t._v("\n          "+t._s(t._f("moment")(t.changeApplicctionData.originDate,"YYYY-MM-DD"))+" "+t._s(t.changeApplicctionData.originDON)+" ("+t._s(t.changeApplicctionData.originTime)+")\n        ")]):a("span",[t._v("\n          "+t._s(t._f("moment")(t.changeApplicctionData.changeDate,"YYYY-MM-DD"))+" "+t._s(t.changeApplicctionData.changeDON)+" ("+t._s(t.changeApplicctionData.changeTime)+")\n        ")])])]),a("div",{staticClass:"hr"}),a("div",{staticClass:"row"},[a("div",{staticClass:"left"},[t._v("\n        换班对象:\n      ")]),a("div",{staticClass:"right"},[t.isOrigin?a("span",[t._v("\n          "+t._s(t.changeApplicctionData.originUser)+"("+t._s(t.changeApplicctionData.originUserJobNum)+")\n        ")]):a("span",[t._v("\n          "+t._s(t.changeApplicctionData.changeUser)+"("+t._s(t.changeApplicctionData.changeUserJobNum)+")\n        ")])])]),a("div",{staticClass:"hr"}),a("div",{staticClass:"row"},[a("div",{staticClass:"left"},[t._v("\n        换班班次:\n      ")]),a("div",{staticClass:"right"},[t.isOrigin?a("span",[t._v("\n          "+t._s(t._f("moment")(t.changeApplicctionData.changeDate,"YYYY-MM-DD"))+" "+t._s(t.changeApplicctionData.changeDON)+" ("+t._s(t.changeApplicctionData.changeTime)+")\n        ")]):a("span",[t._v("\n          "+t._s(t._f("moment")(t.changeApplicctionData.originDate,"YYYY-MM-DD"))+" "+t._s(t.changeApplicctionData.originDON)+" ("+t._s(t.changeApplicctionData.originTime)+")\n        ")])])])]),a("div",{staticClass:"middle box"},[a("div",{staticClass:"row"},[t._v("\n      换班原因:\n    ")]),a("div",{staticClass:"hr"}),a("div",{staticClass:"row"},[t._v("\n      "+t._s(t.changeApplicctionData.changeReason)+"\n    ")])]),a("div",{staticClass:"bottom box"},[a("div",{staticClass:"row"},[t._v("\n     状态:\n    ")]),a("div",{staticClass:"hr"}),a("div",{staticClass:"line_box"},[a("steps",{staticClass:"step_line",attrs:{"line-data":t.lineData}})],1)]),t.isOrigin||"待确认"!==t.changeApplicctionData.status?t._e():a("div",{staticClass:"button_box"},[a("button",{on:{click:function(s){return t.commitHandle("同意")}}},[t._v("同意")]),a("div",{staticClass:"black_div"}),a("button",{staticClass:"gray",on:{click:function(s){return t.commitHandle("拒绝")}}},[t._v("拒绝")])]),a("div",{staticClass:"blank"})])},n=[],e=function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"step"},[a("ul",[a("li",[a("div",{staticClass:"l pass"}),a("div",{staticClass:"r"},[a("div",{staticClass:"h"},[t._v("\n          发起\n        ")]),a("div",{staticClass:"c"},[t._v("\n          "+t._s(t.lineData.originUser)+" "+t._s(t.lineData.sendTime)+"\n        ")])])]),a("li",[a("div",{staticClass:"l",class:{pass:t.nowStep>1}}),a("div",{staticClass:"r"},[a("div",{staticClass:"h",class:t.nowStep<2.6?t._statusColor(t.lineData.status):"tongguo",domProps:{textContent:t._s(t.nowStep<2.6?t.lineData.status:"已通过")}}),a("div",{staticClass:"c",class:t.nowStep<2.6?t._statusColor(t.lineData.status):"tongguo"},[t._v("\n          "+t._s(t.lineData.changeUser)+" "+t._s(t.lineData.comfirmTime||"无")+"\n        ")])])]),a("li",[a("div",{staticClass:"l",class:{pass:t.nowStep>2.5}}),t.nowStep>2.5?a("div",{staticClass:"r"},[a("div",{staticClass:"h",class:t._statusColor(t.lineData.status)},[t._v("\n          "+t._s(t.lineData.status)+"\n        ")]),a("div",{staticClass:"c",class:t._statusColor(t.lineData.status)},[t._v("\n          "+t._s(t.lineData.passUser||"无")+" "+t._s(t.lineData.passTime||"无")+"\n        ")])]):t._e()])]),a("div",{staticClass:"time_bar"}),a("div",{staticClass:"time_bar_green",style:t.greenBar})])},c=[],o={name:"Steps",props:{lineData:{type:Object,default:function(){return{sponsorsUser:"李四",startTime:"2018-03-15 22:00",comfirmUser:"张三",comfirmTime:"2018-03-15 22:00",passUser:"wangwu",passTime:"2018-03-15 22:00",status:"已通过"}}}},computed:{nowStep:function(){return"待确认"===this.lineData.status?1:"已拒绝"===this.lineData.status?2:"待审批"===this.lineData.status?2.5:3},greenBar:function(){return this.nowStep<2?{height:"25%"}:this.nowStep<2.5?{height:"50%"}:this.nowStep<3?{height:"70%"}:{height:"80%"}}},methods:{_statusColor:function(t){switch(t){case"待确认":return"queren";case"待审批":return"shenpi";case"已拒绝":return"jujue";case"已驳回":return"bohui";case"已通过":return"tongguo";default:break}}}},l=o,r=(a("289b"),a("fc05")),h=Object(r["a"])(l,e,c,!1,null,"4d19925d",null),p=h.exports,g={name:"CDetail",components:{Steps:p},data:function(){return{id:"",jobNum:"Q001234",changeApplicctionData:{id:1,line:"一号线",station:"后卫寨",originDate:"2018-10-11",originDON:"夜",originTime:"18:00-06:00",originUser:"李四",originUserJobNum:"Q003333",changeDate:"2018-10-10",changeDON:"白",changeTime:"09:00-18:00",changeUser:"zhangsna",changeUserJobNum:"Q001234",changeReason:"家里有急事，需要进行换班，希望能够同意",passUser:"王五",sendTime:"2018-03-15 22:00",comfirmTime:"2018-03-15 22:00",passTime:"2018-03-15 22:00",status:"已通过"}}},computed:{isOrigin:function(){return this.changeApplicctionData.originUserJobNum===this.jobNum},lineData:function(){return{originUser:this.changeApplicctionData.originUser,sendTime:this.changeApplicctionData.sendTime,changeUser:this.changeApplicctionData.changeUser,comfirmTime:this.changeApplicctionData.comfirmTime,passUser:this.changeApplicctionData.passUser,passTime:this.changeApplicctionData.passTime,status:this.changeApplicctionData.status}}},methods:{getShiftsDataDetail:function(t){var s=this;this.$rpc.call("funenc_xa_station.change_shifts","get_change_shifts_by_id",[],{id:t}).then(function(t){s.changeApplicctionData=t}).catch(function(t){console.log(t)})},commitHandle:function(t){var s=this;this.$rpc.call("funenc_xa_station.change_shifts","save_state",[],{id:this.id,states:t}).then(function(t){console.log(t),t&&s.getShiftsDataDetail(s.id)}).catch(function(t){console.log(t)})}},mounted:function(){this.id=this.$route.params.id;var t=JSON.parse(sessionStorage.getItem("userInfo"));this.jobNum=t&&t.jobnumber,this.getShiftsDataDetail(this.id)}},u=g,d=(a("fecb"),Object(r["a"])(u,i,n,!1,null,"94b583a0",null));s["default"]=d.exports},a1be:function(t,s,a){},e32b:function(t,s,a){},fecb:function(t,s,a){"use strict";var i=a("a1be"),n=a.n(i);n.a}}]);
//# sourceMappingURL=chunk-4d8ceae8.4803d60b.js.map