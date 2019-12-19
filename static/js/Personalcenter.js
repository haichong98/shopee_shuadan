$(function (){
    $("#file").change(function(){
        var upload_file= this.files[0];
        form_data = new FormData;
        form_data.append("files",upload_file);
        $.ajax({
                url:'http://127.0.0.1:8000/Imges/',
                type:'post',
                method: "post",
                contentType: false,        // 告诉jQuery不要去设置Content-Type请求头
                processData: false,        // 告诉jQuery不要去处理发送的数据
                data: form_data,
                dataType :'json',
                success: function(data){
                    if (data.res != 200) {
                        layer.msg("登入失效,重新登入", {time: 1000,end: function (){
                           $(location).attr('href', 'http://127.0.0.1:8000/login/');}
                        });
                    } else {
                        layer.msg("头像更换成功,刷新页面", {time: 1000,end: function (){
                           $(location).attr('href', 'http://127.0.0.1:8000/Personalcenter/');}
                        });
                    }
                }, error: function(data){
                    layer.msg("头像上传失败", {time: 1000});
                }
            });
        });

    //显示修改密码框
    $(".gengai").bind('click',function(){
        $("#gengai").css('display','block');
    });
    //ajax 验证旧密码并进行验证
    $('#genbutton').bind('click',function(){
        var new_password = $("#new_password").val();
        var old_password = $("#old_password").val();
        var re_n = /[^\d]/g;
        var re_t = /[^a-zA-Z]/g;
            if (old_password == '' || old_password == undefined) {
                layer.msg("请填旧密码", {time: 1000});
                return false;
            }
            if (new_password == '' || new_password == undefined) {
                layer.msg("请填新密码", {time: 1000});
                return false;
            } else if ($.trim($("#new_password").val()).length==0) {
                layer.msg("不能为空", {time: 1000});
                return false;
            } else if (new_password.length < 6 || new_password.length > 16) {
                layer.msg("长度应为6-16个字符", {time: 1000});
                return false;
            } else if (!re_n.test(new_password)) {
                layer.msg("不能全部为数字", {time: 1000});
                return false;
            } else if (!re_t.test(new_password)) {
                layer.msg("不能全部为字母", {time: 1000});
                return false;
            }
            $.ajax({
                url:'http://127.0.0.1:8000/verifypassword/',
                type:'post',
                data:{'old_password':old_password,'new_password':new_password},
                dataType :'json',
                success : function(data){
                    if (data.res != 200) {
                        layer.msg("旧密码不正确", {time: 1000});
                    } else {
                        layer.alert('修改密码成功,请重新登入',{icon:1, title:'提示',end: function (){
                           $(location).attr('href', 'http://127.0.0.1:8000/login/');
                        }
                        });
                    }
                },
                error: function (data) {
                    layer.msg('请求异常，请刷新页面重试', {time: 1000});
                }
                // 请求成功才开始倒计时
            });

    });
});