$(document).ready(function () {
var beginTime = 0;//执行onbeforeunload的开始时间
var differTime = 0;//时间差
window.onunload = function (){
        differTime = new Date().getTime() - beginTime;
        if(differTime <= 5) {
            Cookies.set('abc', '123');
        }else{
            console.log('页面正在刷新')
        }

    };
window.onbeforeunload = function (){
       beginTime = new Date().getTime();
    };

})
