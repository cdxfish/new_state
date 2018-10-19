
console.log('2222')
DingTalkPC.error(function (err) {
            console.log(err)
        });

var page_origin =location.href.replace(location.hash, "");
console.log(page_origin)
$.ajax({
    url: "/dingtalk/auth_config/?url="+page_origin + "&account_code=001",
    type: 'GET',
    success: function (data) {
        var data = JSON.parse(data)
        DingTalkPC.config({
            agentId: 178652492,
            corpId: data.corp_id,
            timeStamp: data.timestamp,
            nonceStr: data.noncestr,
            signature: data.signature,
            jsApiList: [
                'runtime.info'
            ]
        });
        DingTalkPC.ready(function() {
//            debugger
            DingTalkPC.runtime.permission.requestAuthCode({
                corpId: data.corp_id,
                onSuccess: function(result) {

                    if(result.code){

                        console.log(result.code)
                        window.location.href= 'http://daily.cq.cq-tct.com:8088?code='+result.code+'&type=pc';
                    }else{
                        alert('授权失败,请联系管理员!')
                    }
                },
                onFail : function(err) {
                    console.log(err)
                }
            });
        });
}})