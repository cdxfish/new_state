(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-743ca935"],{"278f":function(t,a,s){},4864:function(t,a,s){"use strict";var i=s("278f"),e=s.n(i);e.a},f6e0:function(t,a,s){"use strict";s.r(a);var i=function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",{staticClass:"kanban_detail"},[s("div",{staticClass:"box first"},[s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务发起人:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t.taskDetail.sender)+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务发起时间:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t.formatDateTime(t.taskDetail.originator_time))+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务开始时间:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t.formatDateTime(t.taskDetail.task_start_time))+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务结束时间:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t.formatDateTime(t.taskDetail.task_end_time))+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        优先级:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t._f("priority")(t.taskDetail.task_priority))+"\n      ")])]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[s("div",{staticClass:"left"},[t._v("\n        任务类型:\n      ")]),s("div",{staticClass:"right"},[t._v("\n        "+t._s(t.taskDetail.task_type_id)+"\n      ")])])]),s("div",{staticClass:"box second"},[s("div",{staticClass:"row"},[t._v("\n      任务接收人:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[t._v("\n      "+t._s(t.taskDetail.sendee?t.taskDetail.sendee.join("、"):"暂无")+"\n    ")])]),s("div",{staticClass:"box third"},[s("div",{staticClass:"row"},[t._v("\n      任务描述:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row"},[t._v("\n      "+t._s(t.taskDetail.task_describe)+"\n    ")])]),t.showComplateBtn?t._e():s("div",{staticClass:"box fourth"},[s("div",{staticClass:"row"},[t._v("\n      完成情况:\n    ")]),s("div",{staticClass:"table"},[t._m(0),t._l(t.taskDetail.complateInfo,function(a,i){return s("div",{key:a.id,staticClass:"trow even",class:i%2===0?"even":"odd"},[s("div",{staticClass:"tcol"},[t._v(t._s(a.name))]),s("div",{staticClass:"tcol"},[t._v(t._s(t.formatDateTime(a.complateTime)||"未完成"))]),s("div",{staticClass:"tcol link",class:{disabled:!a.complateTime},on:{click:function(s){t.showComplateDetail(a)}}},[t._v("查看详情")])])})],2)]),t.showComplateBtn&&"completed"!==t.taskDetail.receive_task_state?s("div",{staticClass:"box fifth"},[s("div",{staticClass:"row"},[t._v("\n      任务反馈:\n    ")]),s("div",{staticClass:"hr"}),s("div",{staticClass:"row textarea_box"},[s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.feedBackContent,expression:"feedBackContent"}],attrs:{name:"",id:"",rows:"10",placeholder:"请输入反馈内容"},domProps:{value:t.feedBackContent},on:{input:function(a){a.target.composing||(t.feedBackContent=a.target.value)}}})])]):t._e(),t.showComplateBtn&&"completed"!==t.taskDetail.receive_task_state?s("common-btn",{staticClass:"bottom_btn",on:{click:t.commitTask}},[t._v("确认完成")]):t._e(),s("div",{staticClass:"blank"}),t.isFeedBackShow?s("my-dialog",[s("div",{staticClass:"feedback_box"},[s("h3",[t._v("任务反馈")]),s("div",{staticClass:"content"},[s("p",[t._v(t._s(t.nowFeedBack||"暂无"))])]),s("common-btn",{on:{click:t.closeFeedBackDialog}},[t._v("关闭")])],1)]):t._e()],1)},e=[function(){var t=this,a=t.$createElement,s=t._self._c||a;return s("div",{staticClass:"trow odd"},[s("div",{staticClass:"tcol"},[t._v("任务完成人")]),s("div",{staticClass:"tcol"},[t._v("完成时间")]),s("div",{staticClass:"tcol"},[t._v("任务反馈")])])}],n="priority",c="intermediate",o="elementary",l={name:"KanbanDetail",data:function(){return{id:"",isFeedBackShow:!1,nowFeedBack:"",taskDetail:{},feedBackContent:""}},methods:{showComplateDetail:function(t){t.complateTime&&(this.nowFeedBack=t.feedback,this.isFeedBackShow=!0)},closeFeedBackDialog:function(){this.nowFeedBack="",this.isFeedBackShow=!1},formatDateTime:function(t){if(t)return this.$moment(t).add(8,"hour").format("YY-MM-DD HH:mm:ss")},getTaskDataDetail:function(t){var a=this;this.$rpc.call("funenc_xa_station.work_kanban","get_kanban_by_id",[],{id:t}).then(function(t){a.taskDetail=t}).catch(function(t){console.log(t),alert("获取任务详情出错，请刷新")})},commitTask:function(){var t=this;this.$rpc.call("funenc_xa_station.work_kanban","app_save_kanban_type",[],{taskid:this.id,feedBackContent:this.feedBackContent}).then(function(a){a&&t.$router.push("/kanban")}).catch(function(t){console.log(t),alert("确认完成出错，请重试")})}},computed:{showComplateBtn:function(){return"receive_task"===this.taskDetail.task_type}},filters:{priority:function(t){switch(t){case n:return"高";case c:return"中";case o:return"低";default:break}}},mounted:function(){this.id=this.$route.params.id,this.getTaskDataDetail(this.id)}},d=l,r=(s("4864"),s("2877")),v=Object(r["a"])(d,i,e,!1,null,"6c67db21",null);v.options.__file="Detail.vue";a["default"]=v.exports}}]);
//# sourceMappingURL=chunk-743ca935.e68627bf.js.map