$(function (){
    $(".Features").bind('click',function(){
        var html_text = $(this).find('p').html();
        //点击退出
        if (html_text == "退出" ){
        // window.location.href = "http://127.0.0.1:8000/login/";
            $(location).attr('href', 'http://127.0.0.1:8000/dropout/');
        } else if (html_text=="首页"){
            $(location).attr('href', 'http://127.0.0.1:8000/');
        }else if (html_text=="账单"){
            $(location).attr('href', 'http://127.0.0.1:8000/Bill');
        }else if (html_text=="个人中心"){
            $(location).attr('href', 'http://127.0.0.1:8000/Personalcenter');
        }else if (html_text=="钱包"){
            $(location).attr('href', 'http://127.0.0.1:8000/wallet/');
        }
    });
});