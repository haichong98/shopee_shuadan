$(function (){
    var code_id = $("#token").val();
    if (code_id == 1){
        layer.msg("账号密码不正确", {time: 1500});
    }
});